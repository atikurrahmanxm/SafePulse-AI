"""SSRF-safe Smart URL Security Analyzer with local heuristics and DNS SPF/DMARC checks."""

from __future__ import annotations

import ipaddress
import re
import socket
import ssl
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import dns.exception
import dns.resolver
import httpx

from ..config import settings
from ..ml.predictor import classify_risk_band


PRIVATE_HOSTNAMES = {"localhost", "localhost.localdomain", "ip6-localhost", "metadata.google.internal"}
PRIVATE_SUFFIXES = (".local", ".internal", ".localhost", ".lan", ".home", ".arpa")

SUSPICIOUS_TLDS = {
    "xyz", "top", "click", "gq", "ml", "cf", "tk", "ga", "pw", "icu",
    "buzz", "work", "life", "space", "site", "shop", "club", "info", "ru",
}
URL_SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "rb.gy", "cutt.ly", "is.gd", "shorturl.at",
}
BRAND_KEYWORDS = {
    "sbi", "hdfc", "icici", "axis", "kotak", "canara", "paytm", "phonepe", "gpay",
    "razorpay", "gst", "incometax", "epfo", "microsoft", "office365", "google", "gmail",
    "amazon", "flipkart", "bluedart", "indiapost", "fedex", "dtdc", "meta", "whatsapp",
    "docusign", "zoho", "tally", "shopify",
}
OFFICIAL_SAFE_ALLOWLIST = {
    "onlinesbi.sbi", "sbi.co.in", "hdfcbank.com", "icicibank.com", "axisbank.com",
    "gst.gov.in", "incometax.gov.in", "epfindia.gov.in", "cert-in.org.in", "cybercrime.gov.in",
    "google.com", "accounts.google.com", "microsoft.com", "login.microsoftonline.com",
    "amazon.in", "amazon.com", "flipkart.com", "razorpay.com", "paytm.com", "zoho.com",
}


class SSRFBlockedError(Exception):
    """Raised when a submitted URL targets localhost, private/internal networks, or unsafe schemes."""


def _is_forbidden_ip(ip_obj: ipaddress._BaseAddress) -> bool:
    if isinstance(ip_obj, ipaddress.IPv6Address) and ip_obj.ipv4_mapped:
        return _is_forbidden_ip(ip_obj.ipv4_mapped)
    return (
        ip_obj.is_private
        or ip_obj.is_loopback
        or ip_obj.is_link_local
        or ip_obj.is_multicast
        or ip_obj.is_reserved
        or ip_obj.is_unspecified
    )


def _try_parse_obfuscated_ipv4(host: str) -> Optional[ipaddress.IPv4Address]:
    """Parse octal (0177.0.0.1), hex (0x7f.0.0.1 / 0x7f000001), or shorthand IPv4 notation."""
    parts = host.split(".")
    if not (1 <= len(parts) <= 4):
        return None
    if any(not p for p in parts):
        return None
    nums: List[int] = []
    for part in parts:
        try:
            if part.startswith(("0x", "0X")):
                val = int(part, 16)
            elif len(part) > 1 and part.startswith("0") and all(c in "01234567" for c in part):
                val = int(part, 8)
            elif part.isdigit():
                val = int(part, 10)
            else:
                return None
        except ValueError:
            return None
        if val < 0:
            return None
        nums.append(val)

    # POSIX inet_aton rules: last part absorbs remaining bytes (e.g. 127.1 or single 32-bit int)
    if len(nums) == 1:
        if nums[0] > 0xFFFFFFFF:
            return None
        packed = nums[0]
    else:
        for octet in nums[:-1]:
            if octet > 255:
                return None
        shift = 8 * (4 - len(nums) + 1)
        if nums[-1] >= (1 << shift):
            return None
        packed = nums[-1]
        for idx, octet in enumerate(nums[:-1]):
            packed |= octet << (8 * (3 - idx))
    return ipaddress.IPv4Address(packed)


def _extract_registrable_domain(host: str) -> str:
    parts = [p for p in host.split(".") if p]
    if len(parts) <= 2:
        return host
    # Handle common two-level ccSLDs like .co.in, .gov.in, .co.uk
    if len(parts[-1]) == 2 and parts[-2] in {"co", "gov", "org", "ac", "net", "edu"} and len(parts) >= 3:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def _safe_dns_lookup(domain: str) -> Dict[str, Any]:
    """Perform safe, read-only DNS TXT/A checks without contacting the target web server."""
    resolver = dns.resolver.Resolver(configure=True)
    resolver.timeout = 1.5
    resolver.lifetime = 2.5

    result: Dict[str, Any] = {
        "queried_domain": domain,
        "a_records": [],
        "spf_present": False,
        "spf_record": None,
        "dmarc_present": False,
        "dmarc_record": None,
        "dns_status": "checked",
        "resolved_private_ip": False,
    }

    try:
        answers = resolver.resolve(domain, "A")
        ips = [rdata.to_text() for rdata in answers]
        result["a_records"] = ips[:5]
        for ip_str in ips:
            try:
                if _is_forbidden_ip(ipaddress.ip_address(ip_str)):
                    result["resolved_private_ip"] = True
            except ValueError:
                pass
    except (dns.exception.DNSException, Exception):
        result["dns_status"] = "unavailable_or_nxdomain"

    root_domain = _extract_registrable_domain(domain)
    try:
        txt_answers = resolver.resolve(root_domain, "TXT")
        for rdata in txt_answers:
            txt_val = "".join(s.decode("utf-8", errors="ignore") for s in rdata.strings)
            if txt_val.lower().startswith("v=spf1"):
                result["spf_present"] = True
                result["spf_record"] = txt_val[:220]
                break
    except (dns.exception.DNSException, Exception):
        pass

    try:
        dmarc_answers = resolver.resolve(f"_dmarc.{root_domain}", "TXT")
        for rdata in dmarc_answers:
            txt_val = "".join(s.decode("utf-8", errors="ignore") for s in rdata.strings)
            if "v=dmarc1" in txt_val.lower():
                result["dmarc_present"] = True
                result["dmarc_record"] = txt_val[:220]
                break
    except (dns.exception.DNSException, Exception):
        pass

    return result


def _safe_tls_cert_lookup(host: str, a_records: List[str], port: Optional[int]) -> Dict[str, Any]:
    """Safely inspect public TLS X.509 certificate metadata ONLY after SSRF IP checks pass (zero HTTP traffic)."""
    target_port = port or 443
    if not a_records:
        return {"tls_status": "not_checked_no_dns_a"}
    candidate_ip = a_records[0]
    try:
        if _is_forbidden_ip(ipaddress.ip_address(candidate_ip)):
            return {"tls_status": "blocked_private_ip"}
    except ValueError:
        return {"tls_status": "invalid_resolved_ip"}

    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((candidate_ip, target_port), timeout=1.8) as raw_sock:
            with ctx.wrap_socket(raw_sock, server_hostname=host) as tls_sock:
                cert = tls_sock.getpeercert() or {}
                issuer_parts = dict(x[0] for x in cert.get("issuer", ()) if x)
                subject_parts = dict(x[0] for x in cert.get("subject", ()) if x)
                return {
                    "tls_status": "valid_certificate_read",
                    "issuer_org": issuer_parts.get("organizationName") or issuer_parts.get("commonName"),
                    "subject_cn": subject_parts.get("commonName"),
                    "not_after": cert.get("notAfter"),
                    "san_count": len(cert.get("subjectAltName", ())),
                }
    except ssl.SSLCertVerificationError as exc:
        return {"tls_status": "verification_warning", "detail": str(exc)[:140]}
    except Exception:
        return {"tls_status": "unavailable_or_timeout"}


def _check_optional_safe_browsing(url: str) -> Optional[Dict[str, Any]]:
    """Optional external reputation check only when API key is explicitly configured."""
    api_key = settings.google_safe_browsing_api_key
    if not api_key:
        return None
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {"clientId": "cybershield-ai", "clientVersion": "1.0.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }
    try:
        with httpx.Client(timeout=3.0) as client:
            resp = client.post(endpoint, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                matches = data.get("matches", [])
                return {"checked": True, "flagged": bool(matches), "matches": matches}
    except Exception:
        return {"checked": False, "flagged": False, "matches": []}
    return None


def analyze_url(raw_url: str, language: str = "en") -> Dict[str, Any]:
    candidate = raw_url.strip()
    if "://" not in candidate:
        # Reject obviously dangerous schemes like javascript: or data: before prefixing
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", candidate):
            scheme_only = candidate.split(":", 1)[0].lower()
            raise SSRFBlockedError(
                f"Blocked unsupported or unsafe URL scheme '{scheme_only}:'. Only http:// and https:// are permitted."
            )
        candidate = f"https://{candidate}"

    parsed = urlparse(candidate)
    scheme = (parsed.scheme or "").lower()
    if scheme not in {"http", "https"}:
        raise SSRFBlockedError(
            f"Blocked URL scheme '{scheme or 'unknown'}'. Only http and https URLs can be analyzed."
        )

    if not parsed.netloc or not parsed.hostname:
        raise ValueError("Invalid URL syntax: missing valid hostname.")

    host = parsed.hostname.lower().strip(".")
    if not host or len(host) > 253:
        raise ValueError("Invalid hostname in submitted URL.")

    # SSRF Protection: block localhost, internal domains, and private/loopback/metadata IPs
    if host in PRIVATE_HOSTNAMES or host.endswith(PRIVATE_SUFFIXES):
        raise SSRFBlockedError(
            f"SSRF protection blocked internal/localhost hostname '{host}'. CyberShield AI only analyzes public web addresses."
        )

    is_ip_literal = False
    try:
        ip_obj = ipaddress.ip_address(host)
        is_ip_literal = True
        if _is_forbidden_ip(ip_obj):
            raise SSRFBlockedError(
                f"SSRF protection blocked private, loopback, or reserved IP address '{host}'."
            )
    except ValueError:
        obfuscated_ip = _try_parse_obfuscated_ipv4(host)
        if obfuscated_ip is not None:
            is_ip_literal = True
            if _is_forbidden_ip(obfuscated_ip):
                raise SSRFBlockedError(
                    f"SSRF protection blocked obfuscated private/loopback IP address '{host}' ({obfuscated_ip})."
                )

    # Syntax & hostname validation for non-IP hostnames
    if not is_ip_literal and "." not in host:
        raise SSRFBlockedError(
            f"SSRF protection blocked single-label internal hostname '{host}'."
        )

    indicators: List[Dict[str, Any]] = []
    score = 0

    def add_indicator(code: str, label_en: str, label_bn: str, severity: str, detail_en: str, detail_bn: str, impact: int):
        nonlocal score
        score += impact
        indicators.append(
            {
                "code": code,
                "label": label_bn if language == "bn" else label_en,
                "severity": severity,
                "detail": detail_bn if language == "bn" else detail_en,
                "score_impact": impact,
            }
        )

    # 1. Scheme check (explicitly note HTTPS != safe)
    if scheme == "http":
        add_indicator(
            "no_https",
            "Unencrypted HTTP Protocol",
            "এনক্রিপশনহীন HTTP সংযোগ",
            "medium",
            "The URL uses plain HTTP without TLS encryption; credentials or forms submitted here can be intercepted.",
            "URL-টি সাধারণ HTTP ব্যবহার করছে (HTTPS নয়); এতে পাঠানো তথ্য মাঝপথে চুরি হতে পারে।",
            16,
        )
    else:
        add_indicator(
            "uses_https",
            "Uses HTTPS (Not Proof of Safety)",
            "HTTPS ব্যবহৃত হয়েছে (কিন্তু এটি নিরাপত্তার গ্যারান্টি নয়)",
            "info",
            "HTTPS encrypts transit traffic, but attackers routinely register free TLS certificates on phishing domains. HTTPS alone never proves legitimacy.",
            "HTTPS শুধুমাত্র ডেটা ট্রান্সফার এনক্রিপ্ট করে; ফিশিং সাইটেও আজকাল ফ্রি HTTPS থাকে, তাই শুধু HTTPS দেখে নিরাপদ ভাববেন না।",
            0,
        )

    # 2. Raw IP address URL
    if is_ip_literal:
        add_indicator(
            "raw_ip_url",
            "Public IP Address Used Instead of Domain",
            "ডোমেইনের বদলে সরাসরি IP ঠিকানা ব্যবহৃত হয়েছে",
            "high",
            "Legitimate businesses rarely ask customers or staff to log in via a raw IP address URL.",
            "বৈধ প্রতিষ্ঠান সাধারণত গ্রাহক বা কর্মীদের সরাসরি IP ঠিকানার লিঙ্কে লগইন করতে বলে না।",
            30,
        )

    # 3. Deceptive @ userinfo or double-slash redirect pattern
    if parsed.username or "@" in parsed.netloc:
        add_indicator(
            "userinfo_obfuscation",
            "Deceptive '@' Credential Prefix",
            "প্রতারণামূলক '@' অক্ষর ব্যবহার",
            "critical",
            "Contains '@' in the authority section, a classic trick to make users think they are visiting the text before '@' while the browser navigates to the host after '@'.",
            "URL-এ '@' ব্যবহার করা হয়েছে যাতে ব্যবহারকারী ভুল ডোমেইনকে আসল মনে করে।",
            34,
        )

    if "//" in (parsed.path or "") or re.search(r"(redirect=|next=|url=|return_to=|goto=)", parsed.query or "", re.I):
        add_indicator(
            "open_redirect_param",
            "Suspicious Redirect Parameter in URL",
            "URL-এ সন্দেহজনক রিডাইরেক্ট প্যারামিটার",
            "medium",
            "The URL contains redirect parameters or nested '//' paths that can forward visitors to an untrusted third-party site.",
            "URL-এ রিডাইরেক্ট প্যারামিটার রয়েছে যা ভিজিটরকে অন্য কোনো অজানা সাইটে পাঠিয়ে দিতে পারে।",
            14,
        )

    # 4. Punycode / IDN homograph check
    if "xn--" in host:
        add_indicator(
            "punycode_idn",
            "Punycode Internationalized Domain (Homograph Risk)",
            "Punycode ডোমেইন (নকল অক্ষরের ঝুঁকি)",
            "high",
            "Contains 'xn--' Punycode encoding, which can visually imitate trusted brand names using lookalike Unicode characters.",
            "ডোমেইনে 'xn--' এনকোডিং রয়েছে যা দেখতে আসল ব্র্যান্ডের মতো নকল ডোমেইন তৈরিতে ব্যবহৃত হতে পারে।",
            24,
        )

    # 5. Excessive subdomains & deceptive brand placement
    labels = host.split(".")
    tld = labels[-1]
    registrable = _extract_registrable_domain(host)
    if len(labels) >= 4:
        add_indicator(
            "excessive_subdomains",
            f"Excessive Subdomains ({len(labels)} levels)",
            f"অতিরিক্ত সাব-ডোমেইন ({len(labels)} স্তর)",
            "medium",
            "Long subdomain chains (e.g., sbi-login.security-check.example.xyz) often hide the true registrable domain.",
            "অনেকগুলো সাব-ডোমেইন ব্যবহার করে আসল ডোমেইনটি আড়াল করার চেষ্টা করা হয়ে থাকতে পারে।",
            16,
        )

    if tld in SUSPICIOUS_TLDS:
        add_indicator(
            "high_risk_tld",
            f"High-Abuse Top-Level Domain (.{tld})",
            f"ঝুঁকিপূর্ণ ডোমেইন এক্সটেনশন (.{tld})",
            "medium",
            f"The .{tld} extension has elevated abuse rates in disposable phishing and scam campaigns.",
            f".{tld} এক্সটেনশনটি প্রায়ই স্বল্পমেয়াদী ফিশিং ও স্ক্যাম ক্যাম্পেইনে ব্যবহৃত হয়।",
            15,
        )

    if host in URL_SHORTENERS or registrable in URL_SHORTENERS:
        add_indicator(
            "url_shortener",
            "URL Shortener Hides Final Destination",
            "শর্টনার লিঙ্ক আসল গন্তব্য গোপন করছে",
            "high",
            "Shortened links conceal the true destination domain and bypass quick visual inspection. CyberShield AI does not follow redirects to protect the server.",
            "লিঙ্ক শর্টনার আসল ওয়েবসাইটের ঠিকানা লুকিয়ে রাখে; নিরাপত্তার জন্য সার্ভার এই লিঙ্ক অনুসরণ করে না।",
            22,
        )

    # Check brand impersonation outside official allowlist
    if registrable not in OFFICIAL_SAFE_ALLOWLIST:
        matched_brands = [b for b in BRAND_KEYWORDS if b in host]
        if matched_brands:
            add_indicator(
                "brand_impersonation",
                f"Potential Brand Impersonation ({', '.join(matched_brands[:3])})",
                f"ব্র্যান্ডের ছদ্মবেশী নাম ({', '.join(matched_brands[:3])})",
                "high",
                f"Hostname references '{matched_brands[0]}' on an unverified registrable domain '{registrable}'.",
                f"অযাচাইকৃত ডোমেইন '{registrable}'-এ '{matched_brands[0]}' নাম ব্যবহার করা হয়েছে।",
                28,
            )

    # 6. Unusual URL length, suspicious characters, non-standard port
    if len(candidate) > 100:
        add_indicator(
            "long_url",
            f"Unusually Long URL ({len(candidate)} chars)",
            f"অস্বাভাবিক দীর্ঘ URL ({len(candidate)} অক্ষর)",
            "low",
            "Excessively long URLs are commonly used to push deceptive domains or tracking tokens off-screen on mobile devices.",
            "অতিরিক্ত লম্বা URL মোবাইলের স্ক্রিনে আসল ডোমেইন আড়াল করতে ব্যবহৃত হয়।",
            10,
        )

    if parsed.port and parsed.port not in (80, 443):
        add_indicator(
            "non_standard_port",
            f"Non-Standard Web Port (:{parsed.port})",
            f"অস্বাভাবিক পোর্ট নম্বর (:{parsed.port})",
            "medium",
            "Standard business web portals operate on ports 80/443; unusual ports can indicate compromised or rogue servers.",
            "বৈধ ব্যবসায়িক সাইট সাধারণত ৮০ বা ৪৪৩ পোর্ট ব্যবহার করে; অস্বাভাবিক পোর্ট ঝুঁকিপূর্ণ হতে পারে।",
            14,
        )

    suspicious_path_tokens = re.findall(
        r"(login|verify|kyc|unlock|update|password|signin|wallet|upi|refund|billing|appeal|\.apk|\.exe)",
        f"{parsed.path} {parsed.query}",
        re.I,
    )
    if suspicious_path_tokens and registrable not in OFFICIAL_SAFE_ALLOWLIST:
        unique_tokens = sorted({t.lower() for t in suspicious_path_tokens})[:4]
        add_indicator(
            "sensitive_path_keywords",
            f"Sensitive Action Keywords in Path ({', '.join(unique_tokens)})",
            f"পাথে সংবেদনশীল শব্দ ({', '.join(unique_tokens)})",
            "medium",
            "Path/query requests login, KYC, payment, or executable download actions on an unverified domain.",
            "অযাচাইকৃত ডোমেইনের লিঙ্কে লগইন, KYC, পেমেন্ট বা ডাউনলোড সংক্রান্ত শব্দ রয়েছে।",
            14,
        )

    # 7. Safe DNS analysis (A, SPF, DMARC) — never execute HTTP request to target
    dns_records: Dict[str, Any] = {"dns_status": "skipped_ip_literal"}
    if not is_ip_literal:
        dns_records = _safe_dns_lookup(host)
        if dns_records.get("resolved_private_ip"):
            raise SSRFBlockedError(
                f"SSRF protection blocked '{host}' because DNS resolved to a private or reserved IP address."
            )
        if not dns_records.get("spf_present") and not dns_records.get("dmarc_present") and registrable not in OFFICIAL_SAFE_ALLOWLIST:
            add_indicator(
                "missing_email_auth_dns",
                "Domain Lacks SPF and DMARC DNS Records",
                "ডোমেইনে SPF ও DMARC DNS রেকর্ড নেই",
                "low",
                "Neither SPF nor DMARC records were found for the root domain. While many small domains lack DMARC, combined with other signals this increases impersonation risk.",
                "মূল ডোমেইনে SPF বা DMARC রেকর্ড পাওয়া যায়নি। ছোট সাইটে কখনো নাও থাকতে পারে, তবে অন্যান্য সংকেতের সাথে এটি ঝুঁকি বাড়ায়।",
                8,
            )

    # 8. Safe Read-Only TLS certificate metadata (HTTPS only, after SSRF IP validation)
    tls_info: Dict[str, Any] = {"tls_status": "skipped_http_or_ip"}
    if scheme == "https" and not is_ip_literal and not dns_records.get("resolved_private_ip"):
        tls_info = _safe_tls_cert_lookup(host, dns_records.get("a_records") or [], parsed.port)
        if tls_info.get("tls_status") == "verification_warning":
            add_indicator(
                "tls_cert_warning",
                "TLS Certificate Verification Warning",
                "TLS সার্টিফিকেট যাচাই সতর্কতা",
                "high",
                f"Certificate handshake raised a trust/hostname warning: {tls_info.get('detail', 'untrusted chain')}",
                "ওয়েবসাইটের SSL/TLS সার্টিফিকেটে ত্রুটি বা বিশ্বাসযোগ্যতার সমস্যা পাওয়া গেছে।",
                20,
            )

    # 9. Optional external reputation API check if configured
    reputation_source = "local-static-and-dns-engine"
    ext_rep = _check_optional_safe_browsing(candidate)
    safe_browsing_flagged = False
    if ext_rep and ext_rep.get("checked"):
        reputation_source = "local-engine + google-safe-browsing"
        if ext_rep.get("flagged"):
            safe_browsing_flagged = True
            add_indicator(
                "safe_browsing_flagged",
                "Flagged by Google Safe Browsing",
                "Google Safe Browsing দ্বারা ঝুঁকিপূর্ণ হিসেবে চিহ্নিত",
                "critical",
                "External reputation lookup matched this URL against known malware/social-engineering threat lists.",
                "বাহ্যিক থ্রেট ডাটাবেসে এই URL-টি ম্যালওয়্যার বা ফিশিং হিসেবে তালিকাভুক্ত আছে।",
                45,
            )

    risk_score = max(0, min(100, int(score)))
    risk_category = classify_risk_band(risk_score)
    if risk_score >= 75 or safe_browsing_flagged:
        verdict_classification = "Malicious"
    elif risk_score >= 25:
        verdict_classification = "Suspicious"
    elif registrable in OFFICIAL_SAFE_ALLOWLIST or (
        dns_records.get("dns_status") == "checked"
        and (dns_records.get("spf_present") or dns_records.get("dmarc_present"))
        and tls_info.get("tls_status") == "valid_certificate_read"
    ):
        verdict_classification = "Safe-Looking"
    else:
        verdict_classification = "Unknown"

    if language == "bn":
        if risk_score <= 24:
            explanation = (
                f"'{host}' বিশ্লেষণে বড় কোনো ফিশিং প্যাটার্ন পাওয়া যায়নি, তবে এই ফলাফল সাইটটি সম্পূর্ণ নিরাপদ তা প্রমাণ করে না (Unknown vs Safe)। "
                "কোনো বাহ্যিক রেপুটেশন API না থাকায় এটি কেবল স্থানীয় সিনট্যাক্স ও DNS যাচাইয়ের ওপর ভিত্তি করে তৈরি।"
            )
        else:
            explanation = (
                f"'{host}' URL-টিতে একাধিক ঝুঁকিপূর্ণ সংকেত শনাক্ত হয়েছে (স্কোর {risk_score}/100)। "
                "সার্ভার সুরক্ষার (SSRF প্রতিরোধ) জন্য CyberShield AI এই ওয়েবসাইটটি কখনোই ওপেন বা ডাউনলোড করে না।"
            )
        recs = [
            "সন্দেহজনক লিঙ্কে কখনোই ব্যাংকিং পাসওয়ার্ড, OTP বা কার্ডের তথ্য দেবেন না।",
            "HTTPS লক আইকন থাকা মানেই ওয়েবসাইট নিরাপদ নয় — মূল ডোমেইন নাম (শেষের দুটি অংশ) মিলিয়ে দেখুন।",
            "গুরুত্বপূর্ণ লগইনের জন্য লিঙ্কে ক্লিক না করে ব্রাউজারে নিজে অফিসিয়াল ওয়েবসাইট টাইপ করুন।",
        ]
    else:
        if risk_score <= 24:
            explanation = (
                f"Static URL and DNS inspection for '{host}' found no high-risk phishing indicators. "
                "Important: 'Low Risk' means no local red flags were detected — NOT a guarantee that the site is safe "
                "(unknown vs. verified safe). CyberShield AI never fetches or executes submitted URLs to prevent SSRF."
            )
        else:
            explanation = (
                f"Static URL and DNS inspection for '{host}' detected {len([i for i in indicators if i['score_impact'] > 0])} "
                f"risk indicator(s) yielding a score of {risk_score}/100 ({risk_category}). "
                "To prevent SSRF and malware exposure, CyberShield AI never visits, downloads, or executes the target URL."
            )
        recs = [
            "Do not enter passwords, OTPs, UPI PINs, or payment details on unverified domains.",
            "Remember: HTTPS padlock only encrypts transit — attackers also use HTTPS on phishing domains.",
            "Visit banks, tax portals, and payment dashboards by typing the official domain directly or using bookmarks.",
        ]
        if not settings.google_safe_browsing_api_key:
            recs.append(
                "Note: External threat-intelligence API keys are not configured, so analysis relies on CyberShield AI's local heuristic and DNS engine."
            )

    return {
        "submitted_url": candidate,
        "normalized_host": host,
        "scheme": scheme,
        "risk_score": risk_score,
        "risk_category": risk_category,
        "verdict_classification": verdict_classification,
        "indicators": indicators,
        "dns_records": dns_records,
        "tls_info": tls_info,
        "reputation_source": reputation_source,
        "technical_explanation": explanation,
        "recommendations": recs,
    }
