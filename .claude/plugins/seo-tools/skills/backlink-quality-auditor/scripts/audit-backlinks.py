#!/usr/bin/env python3
"""
Backlink Quality Auditor — offline audit of GSC top-linking-sites CSV export.

Usage:
    python3 audit-backlinks.py \
        --sites <top-linking-sites.csv> \
        [--anchors <top-linking-text.csv>] \
        [--my-domain <example.com>] \
        --out <output_dir>

Output files in <output_dir>:
    audit-report.json   — structured data for LLM synthesis
    disavow.txt         — Google Disavow Tool format
    toxic-domains.csv   — flagged domains for user review
"""
import argparse, csv, json, os, re, sys
from collections import Counter
from pathlib import Path


# =============================================================================
# Toxic detection criteria
# =============================================================================

SPAM_TLDS = {
    ".tk", ".ml", ".ga", ".cf", ".gq",  # free TLDs
    ".xyz", ".top", ".click", ".loan", ".work", ".date",
    ".racing", ".accountant", ".faith", ".review", ".bid",
    ".stream", ".download", ".science", ".party", ".trade",
}

FOREIGN_TLDS_RISK = {
    ".ru", ".cn", ".pl", ".ro", ".su", ".kz", ".by",
    ".ir", ".ua", ".rs",
}

CASINO_ADULT_KEYWORDS = {
    "casino", "poker", "betting", "gambling", "slot", "bet365",
    "viagra", "cialis", "porn", "xxx", "adult", "escort",
    "loan", "payday", "forex", "crypto-pump",
    "ca-do", "ca-cuoc", "sex", "khieu-dam",
}

FOREIGN_KEYWORDS_IN_DOMAIN = {
    # Cyrillic transliteration patterns common in Russian/Bulgarian spam
    "site", "shop", "store",
}

COMMERCIAL_SPAM_ANCHORS = {
    "casino", "poker", "viagra", "cialis", "loan", "payday loan",
    "betting", "porn", "escort", "ca cuoc", "ca do", "sex shop",
    "buy now", "click here cheap", "free download",
}

GENERIC_ANCHORS = {
    "click here", "here", "this site", "this page", "website",
    "link", "url", "read more", "more info", "source",
    "tại đây", "ở đây", "xem thêm", "trang này", "đường dẫn", "nguồn",
}

# Patterns
RE_AUTOGEN_DOMAIN = re.compile(r"^[a-z0-9]{12,}\.|^\w*\d{4,}\w*\.")
RE_FOREIGN_SCRIPT = re.compile(r"[Ѐ-ӿ一-鿿぀-ヿ]")
RE_DIRECTORY_PATTERN = re.compile(
    r"(directory|listing|submit|catalog|bookmark)",
    re.IGNORECASE,
)
RE_PBN_INDICATOR = re.compile(
    r"(blog\d+\.|wp\d+\.|news\d+\.|site\d+\.)",
    re.IGNORECASE,
)


# =============================================================================
# CSV parsing (handles GSC localization VN/EN)
# =============================================================================

SITE_COLUMN_CANDIDATES = [
    "Top linking sites", "Trang web liên kết hàng đầu", "Trang web có liên kết",
    "Site", "Domain", "Linking site", "Trang web",
]
COUNT_COLUMN_CANDIDATES = [
    "Pages", "Số trang", "Số liên kết", "Links", "Incoming links",
    "Số trang có liên kết", "Liên kết đến",
]
ANCHOR_COLUMN_CANDIDATES = [
    "Top linking text", "Văn bản liên kết hàng đầu", "Anchor text",
    "Text", "Văn bản", "Anchor",
]
ANCHOR_COUNT_CANDIDATES = [
    "Number of sites", "Số trang web", "Sites", "Count", "Số lượng",
]


def read_csv_smart(path):
    """Read CSV trying multiple encodings."""
    for enc in ["utf-8-sig", "utf-8", "cp1252", "latin-1"]:
        try:
            with open(path, "r", encoding=enc, newline="") as f:
                rows = list(csv.reader(f))
            return rows, enc
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Cannot decode {path} with any common encoding")


def find_column_index(header, candidates):
    """Find index of first matching column (case-insensitive, exact match)."""
    header_lower = [h.strip().lower() for h in header]
    for cand in candidates:
        if cand.lower() in header_lower:
            return header_lower.index(cand.lower())
    return None


def parse_sites_csv(path):
    rows, enc = read_csv_smart(path)
    if not rows:
        return [], None
    header = rows[0]
    site_idx = find_column_index(header, SITE_COLUMN_CANDIDATES)
    count_idx = find_column_index(header, COUNT_COLUMN_CANDIDATES)
    if site_idx is None:
        site_idx = 0
    sites = []
    for row in rows[1:]:
        if not row or len(row) <= site_idx:
            continue
        domain = row[site_idx].strip().lower()
        if not domain:
            continue
        # Strip http(s):// and trailing slash
        domain = re.sub(r"^https?://", "", domain).split("/")[0]
        count = 0
        if count_idx is not None and len(row) > count_idx:
            try:
                count = int(re.sub(r"[^\d]", "", row[count_idx]) or "0")
            except ValueError:
                count = 0
        sites.append({"domain": domain, "link_count": count})
    return sites, header


def parse_anchors_csv(path):
    rows, enc = read_csv_smart(path)
    if not rows:
        return [], None
    header = rows[0]
    anchor_idx = find_column_index(header, ANCHOR_COLUMN_CANDIDATES)
    count_idx = find_column_index(header, ANCHOR_COUNT_CANDIDATES)
    if anchor_idx is None:
        anchor_idx = 0
    anchors = []
    for row in rows[1:]:
        if not row or len(row) <= anchor_idx:
            continue
        text = row[anchor_idx].strip()
        if not text:
            continue
        count = 1
        if count_idx is not None and len(row) > count_idx:
            try:
                count = int(re.sub(r"[^\d]", "", row[count_idx]) or "1")
            except ValueError:
                count = 1
        anchors.append({"anchor": text, "count": count})
    return anchors, header


# =============================================================================
# Toxic scoring
# =============================================================================

def get_tld(domain):
    """Return TLD including dot — handles multi-level like .co.uk."""
    parts = domain.split(".")
    if len(parts) >= 2:
        return "." + parts[-1].lower()
    return ""


def score_domain(domain, my_domain=None):
    """Return (toxic_score, flags[]) — score 0-10."""
    flags = []
    score = 0
    domain_lower = domain.lower()

    # Skip own domain
    if my_domain and my_domain.lower() in domain_lower:
        return 0, ["internal"]

    tld = get_tld(domain_lower)

    # 1. TLD spam
    if tld in SPAM_TLDS:
        flags.append("tld_spam")
        score += 4

    # 2. Foreign TLD risk
    if tld in FOREIGN_TLDS_RISK:
        flags.append("foreign_tld")
        score += 2

    # 3. Casino/adult/loan keywords in domain
    for kw in CASINO_ADULT_KEYWORDS:
        if kw in domain_lower:
            flags.append("casino_adult_kw")
            score += 5
            break

    # 4. Autogen pattern (random chars/numbers)
    if RE_AUTOGEN_DOMAIN.match(domain_lower):
        flags.append("autogen_pattern")
        score += 3

    # 5. Free subdomain platforms (blogspot etc — context-dependent, mild flag)
    free_platforms = ["blogspot.", "wordpress.com", "weebly.com", "wix.com"]
    for p in free_platforms:
        if p in domain_lower:
            flags.append("free_subdomain")
            score += 1
            break

    # 6. Directory/submission pattern in domain
    if RE_DIRECTORY_PATTERN.search(domain_lower):
        flags.append("directory_pattern")
        score += 2

    # 7. PBN-style numbered subdomain
    if RE_PBN_INDICATOR.search(domain_lower):
        flags.append("pbn_indicator")
        score += 3

    # 8. Foreign script in domain (rare since IDN, but check)
    if RE_FOREIGN_SCRIPT.search(domain):
        flags.append("foreign_script")
        score += 2

    return min(score, 10), flags


def classify(score):
    if score == 0:
        return "clean"
    if score < 4:
        return "suspicious"
    return "toxic"


# =============================================================================
# Anchor analysis
# =============================================================================

def categorize_anchor(text, my_brand_kw=None):
    t = text.lower().strip()

    # Naked URL
    if re.match(r"^https?://", t) or re.match(r"^www\.", t):
        return "naked_url"

    # Spam commercial
    for kw in COMMERCIAL_SPAM_ANCHORS:
        if kw in t:
            return "spam"

    # Foreign script
    if RE_FOREIGN_SCRIPT.search(text):
        return "foreign"

    # Generic
    if t in GENERIC_ANCHORS or any(g == t for g in GENERIC_ANCHORS):
        return "generic"

    # Branded (if brand provided)
    if my_brand_kw and my_brand_kw.lower() in t:
        return "branded"

    # Default: partial-match keyword
    return "keyword"


def analyze_anchors(anchors, my_brand_kw=None):
    if not anchors:
        return None
    total = sum(a["count"] for a in anchors)
    enriched = []
    cat_counter = Counter()
    for a in anchors:
        cat = categorize_anchor(a["anchor"], my_brand_kw)
        cat_counter[cat] += a["count"]
        enriched.append({
            "anchor": a["anchor"],
            "count": a["count"],
            "category": cat,
            "pct": round(a["count"] * 100 / total, 2) if total else 0,
        })

    # Over-optimization check: keyword (non-branded, non-generic) > 30%
    keyword_pct = round(cat_counter.get("keyword", 0) * 100 / total, 2) if total else 0
    over_opt_threshold = 30.0
    for e in enriched:
        e["over_optimized"] = (
            e["category"] == "keyword" and e["pct"] > 10
        )

    distribution = {
        cat: {
            "count": cat_counter[cat],
            "pct": round(cat_counter[cat] * 100 / total, 2) if total else 0,
        }
        for cat in ["branded", "keyword", "generic", "naked_url", "foreign", "spam"]
    }
    enriched.sort(key=lambda x: -x["count"])
    return {
        "total_anchors": total,
        "distribution": distribution,
        "over_optimized_warning": keyword_pct > over_opt_threshold,
        "keyword_pct": keyword_pct,
        "top_anchors": enriched[:50],
    }


# =============================================================================
# Disavow file generator
# =============================================================================

DISAVOW_HEADER = """# Disavow file generated by backlink-quality-auditor
# Generated: {date}
# Total domains: {total}
#
# Upload to: https://search.google.com/search-console/disavow-links-tool
# WARNING: Only disavow domains you are CERTAIN are harmful.
# Wrong disavow can drop rankings.
#
"""


def generate_disavow(toxic_domains, output_path):
    from datetime import datetime
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(DISAVOW_HEADER.format(
            date=datetime.now().strftime("%Y-%m-%d"),
            total=len(toxic_domains),
        ))
        for d in toxic_domains:
            f.write(f"domain:{d['domain']}\n")


# =============================================================================
# Main
# =============================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sites", required=True, help="GSC top-linking-sites CSV")
    ap.add_argument("--anchors", help="GSC top-linking-text CSV (optional)")
    ap.add_argument("--my-domain", help="Your domain (to exclude internal)")
    ap.add_argument("--my-brand", help="Brand keyword for anchor categorization")
    ap.add_argument("--out", required=True, help="Output directory")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Parse sites
    if not os.path.exists(args.sites):
        print(json.dumps({"error": f"Sites CSV not found: {args.sites}"}))
        sys.exit(1)

    sites, sites_header = parse_sites_csv(args.sites)
    if not sites:
        print(json.dumps({"error": "No sites parsed from CSV"}))
        sys.exit(1)

    # Score each domain
    scored = []
    for s in sites:
        score, flags = score_domain(s["domain"], args.my_domain)
        s["toxic_score"] = score
        s["flags"] = flags
        s["status"] = classify(score)
        scored.append(s)

    # Summary
    total = len(scored)
    clean = sum(1 for s in scored if s["status"] == "clean")
    suspicious = sum(1 for s in scored if s["status"] == "suspicious")
    toxic = sum(1 for s in scored if s["status"] == "toxic")

    toxic_domains = [s for s in scored if s["status"] == "toxic"]
    suspicious_domains = [s for s in scored if s["status"] == "suspicious"]
    toxic_domains.sort(key=lambda x: -x["toxic_score"])
    suspicious_domains.sort(key=lambda x: -x["toxic_score"])

    # Flag breakdown
    flag_counter = Counter()
    for s in scored:
        for f in s["flags"]:
            if f != "internal":
                flag_counter[f] += 1

    # Anchor analysis
    anchor_analysis = None
    if args.anchors and os.path.exists(args.anchors):
        anchors, _ = parse_anchors_csv(args.anchors)
        anchor_analysis = analyze_anchors(anchors, args.my_brand)

    # Build report
    report = {
        "summary": {
            "total_domains": total,
            "clean": clean,
            "clean_pct": round(clean * 100 / total, 2) if total else 0,
            "suspicious": suspicious,
            "suspicious_pct": round(suspicious * 100 / total, 2) if total else 0,
            "toxic": toxic,
            "toxic_pct": round(toxic * 100 / total, 2) if total else 0,
        },
        "flag_breakdown": dict(flag_counter.most_common()),
        "toxic_domains": toxic_domains,
        "suspicious_domains": suspicious_domains,
        "anchor_analysis": anchor_analysis,
        "input_files": {
            "sites_csv": args.sites,
            "anchors_csv": args.anchors,
        },
    }

    # Write outputs
    report_path = out_dir / "audit-report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    disavow_path = out_dir / "disavow.txt"
    generate_disavow(toxic_domains, disavow_path)

    csv_path = out_dir / "toxic-domains.csv"
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["domain", "link_count", "toxic_score", "status", "flags"])
        for s in toxic_domains + suspicious_domains:
            w.writerow([
                s["domain"], s["link_count"], s["toxic_score"],
                s["status"], ",".join(s["flags"]),
            ])

    # Print summary
    print(json.dumps({
        "ok": True,
        "report": str(report_path),
        "disavow": str(disavow_path),
        "toxic_csv": str(csv_path),
        "summary": report["summary"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
