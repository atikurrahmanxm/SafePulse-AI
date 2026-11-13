"""Explainable phishing prediction combining TF-IDF + Logistic Regression with transparent heuristics."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .trainer import get_model_and_metrics


@dataclass(frozen=True)
class HeuristicRule:
    category: str
    pattern: str
    weight: int
    reason_en: str
    reason_bn: str


HEURISTIC_RULES: List[HeuristicRule] = [
    HeuristicRule(
        "urgency_pressure",
        r"\b(within\s+\d+\s*(?:hours?|hrs?|minutes?|mins?)|immediately|urgent|final notice|suspended|deactivated|blocked tonight|action required|face deletion|legal action|disconnection notice|last warning)\b",
        16,
        "Uses high-pressure urgency or threat of account/service suspension to rush decisions.",
        "দ্রুত সিদ্ধান্ত নিতে বাধ্য করার জন্য অ্যাকাউন্ট বা পরিষেবা বন্ধের জরুরি হুমকি বা চাপ ব্যবহার করা হয়েছে।",
    ),
    HeuristicRule(
        "credential_or_otp_request",
        r"\b(enter\s+(?:your\s+)?(?:otp|pin|upi\s*pin|mpin|cvv|password)|share\s+(?:your\s+)?(?:otp|pin|password|aadhaar|pan)|verify\s+(?:your\s+)?(?:credentials|login|password|account)|submit\s+otp|atm\s*pin|netbanking\s+password|transaction\s+pin|sign\s+in\s+(?:now|immediately|with\s+email\s+password))\b",
        24,
        "Requests sensitive credentials, OTP, PIN, CVV, or banking login details — legitimate institutions never ask for these via links or chat.",
        "সংবেদনশীল পাসওয়ার্ড, OTP, PIN, CVV বা ব্যাংকিং তথ্য চাওয়া হয়েছে — বৈধ প্রতিষ্ঠান কখনোই লিঙ্ক বা চ্যাটের মাধ্যমে এগুলো চায় না।",
    ),
    HeuristicRule(
        "suspicious_payment_or_upi_scam",
        r"\b(upi\s*pin\s*to\s*(?:receive|refund|claim)|enter\s+upi\s*pin|gift\s*vouchers?|gift\s*cards?|processing\s+(?:fee|charge)|file\s+charge|registration\s+fee|redelivery\s+fee|alternate\s+account|new\s+beneficiary\s+account|remit\s+rs|crypto|send\s+voucher\s+codes)\b",
        22,
        "Contains suspicious payment instructions (e.g., entering UPI PIN to receive money, gift cards, advance fees, or sudden bank account changes).",
        "সন্দেহজনক পেমেন্ট নির্দেশনা রয়েছে (যেমন টাকা পাওয়ার জন্য UPI PIN দেওয়া, গিফট কার্ড, অগ্রিম ফি, বা হঠাৎ ব্যাংক অ্যাকাউন্ট পরিবর্তন)।",
    ),
    HeuristicRule(
        "impersonation_authority",
        r"\b(sbi|hdfc|icici|axis\s*bank|kotak|canara|bank\s+of\s+baroda|income\s+tax|gstin|gstr|epfo|fssai|cyber\s*cell|microsoft\s*365|google\s*workspace|meta\s*business|bluedart|india\s*post|fedex|dtdc|paytm\s*business|phonepe|razorpay|amazon\s*seller|flipkart\s*seller)\b",
        8,
        "References a high-trust bank, government portal, courier, or business platform commonly impersonated in SME scams.",
        "ব্যাংক, সরকারি পোর্টাল, কুরিয়ার বা ব্যবসায়িক প্ল্যাটফর্মের নাম উল্লেখ করা হয়েছে যা প্রায়ই স্ক্যামে নকল করা হয়।",
    ),
    HeuristicRule(
        "remote_access_or_malware",
        r"\b(anydesk|teamviewer|quicksupport|screen\s*sharing|\.apk\b|\.exe\b|\.zip\.exe|enable\s+macros|setup\.exe|download\s+.*player)\b",
        25,
        "Asks to install remote-access software, APK files, executables, or macro-enabled attachments.",
        "রিমোট-অ্যাক্সেস অ্যাপ, APK ফাইল, এক্সিকিউটেবল ফাইল বা ম্যাক্রো চালু করার অনুরোধ করা হয়েছে।",
    ),
    HeuristicRule(
        "suspicious_link_or_shortener",
        r"(https?://\d{1,3}(?:\.\d{1,3}){3}[^\s]*|https?://(?:bit\.ly|tinyurl\.com|t\.co|rb\.gy|cutt\.ly)/[^\s]+|https?://[^\s]*\.(?:xyz|top|click|gq|ml|cf|pw|icu|buzz|work|life|space|site|shop|club|online)\b[^\s]*)",
        22,
        "Includes a suspicious URL pattern (raw IP address, link shortener, or high-abuse disposable top-level domain).",
        "সন্দেহজনক URL রয়েছে (সরাসরি IP ঠিকানা, লিঙ্ক শর্টনার, বা ঝুঁকিপূর্ণ ডোমেইন এক্সটেনশন)।",
    ),
    HeuristicRule(
        "secrecy_or_bypass",
        r"\b(do\s+not\s+call\s+me|keep\s+this\s+confidential|do\s+not\s+discuss|stuck\s+in\s+a\s+.*meeting|changed\s+my\s+mobile\s+number|new\s+whatsapp\s+number)\b",
        18,
        "Uses secrecy or unavailability excuses ('do not call me', 'new WhatsApp number') typical of CEO/owner impersonation scams.",
        "গোপনীয়তা বা ফোন না করার অজুহাত ('ফোন করবেন না', 'নতুন হোয়াটসঅ্যাপ নম্বর') ব্যবহার করা হয়েছে, যা মালিকের ছদ্মবেশী স্ক্যামের লক্ষণ।",
    ),
]

BENIGN_PROTECTIVE_PATTERN = re.compile(
    r"\b(never\s+share\s+(?:this\s+)?otp|do\s+not\s+share\s+(?:this\s+)?(?:otp|pin|code)|never\s+ask[s]?\s+(?:for\s+)?(?:otp|pin|password|upi\s*pin)|no\s+action\s+is\s+(?:needed|required)|no\s+additional\s+payment\s+is\s+required)\b",
    re.IGNORECASE,
)


def classify_risk_band(score: int) -> str:
    if score <= 24:
        return "Low Risk"
    if score <= 49:
        return "Moderate Risk"
    if score <= 74:
        return "High Risk"
    return "Critical Risk"


def analyze_message(
    message: str,
    channel: str = "email",
    sender_hint: Optional[str] = None,
    language: str = "en",
) -> Dict[str, Any]:
    pipeline, _metrics = get_model_and_metrics()
    combined_input = f"{message} {sender_hint or ''}".strip()

    ml_prob = float(pipeline.predict_proba([combined_input])[0][1])

    # Extract transparent heuristic matches and exact character offsets in `message`
    highlighted: List[Dict[str, Any]] = []
    matched_categories: set[str] = set()
    heuristic_points = 0
    reasons_en: List[str] = []
    reasons_bn: List[str] = []

    for rule in HEURISTIC_RULES:
        regex = re.compile(rule.pattern, re.IGNORECASE)
        matches = list(regex.finditer(message))
        if matches:
            if rule.category not in matched_categories:
                matched_categories.add(rule.category)
                heuristic_points += rule.weight
                reasons_en.append(rule.reason_en)
                reasons_bn.append(rule.reason_bn)
            for m in matches[:4]:
                highlighted.append(
                    {
                        "phrase": message[m.start(): m.end()],
                        "category": rule.category,
                        "weight": rule.weight,
                        "start": m.start(),
                        "end": m.end(),
                    }
                )

    # Check sender hint mismatch / suspicious sender domain
    if sender_hint:
        sh = sender_hint.lower()
        if any(tok in sh for tok in ("@gmail.com", "@yahoo.com", "@outlook.com")) and any(
            brand in message.lower()
            for brand in ("sbi", "hdfc", "icici", "gst", "income tax", "microsoft", "razorpay", "epfo")
        ):
            heuristic_points += 18
            reasons_en.append(
                f"Sender hint '{sender_hint}' uses a free webmail address while claiming to represent an official institution."
            )
            reasons_bn.append(
                f"প্রেরকের ঠিকানা '{sender_hint}' একটি সাধারণ ফ্রি ইমেইল, কিন্তু বার্তাটি সরকারি বা বড় প্রতিষ্ঠানের দাবি করছে।"
            )

    # Protective benign phrasing check (e.g. "Never share OTP with anyone")
    has_protective_warning = bool(BENIGN_PROTECTIVE_PATTERN.search(message))
    if has_protective_warning and "credential_or_otp_request" not in matched_categories:
        heuristic_points = max(0, heuristic_points - 18)
        reasons_en.append(
            "Contains explicit anti-scam warning advising the recipient never to share OTP/PINs."
        )
        reasons_bn.append(
            "বার্তায় স্পষ্টভাবে OTP বা PIN কারো সাথে শেয়ার না করার সতর্কবার্তা রয়েছে।"
        )

    # Deduplicate overlapping highlight spans cleanly (prefer higher weight, earlier start)
    highlighted.sort(key=lambda item: (item["start"], -item["weight"], -(item["end"] - item["start"])))
    merged_highlights: List[Dict[str, Any]] = []
    for item in highlighted:
        if not merged_highlights or item["start"] >= merged_highlights[-1]["end"]:
            merged_highlights.append(item)

    # Combine calibrated ML probability (60%) + capped heuristic evidence (40%)
    capped_heuristics = min(heuristic_points, 70)
    # If protective phrasing is present without malicious URL/credential ask, dampen false positive
    effective_ml = ml_prob * (0.55 if (has_protective_warning and capped_heuristics <= 10) else 1.0)

    blended_score = round((effective_ml * 62.0) + (min(capped_heuristics, 65) / 65.0 * 38.0))
    # Strong multi-signal override when both ML and multiple severe heuristics fire
    if effective_ml >= 0.72 and capped_heuristics >= 35:
        blended_score = max(blended_score, 78)
    elif capped_heuristics >= 40 and effective_ml >= 0.50:
        blended_score = max(blended_score, 72)

    risk_score = max(0, min(100, int(blended_score)))
    risk_category = classify_risk_band(risk_score)

    # Calibrated confidence reflects distance from 0.5 decision boundary and signal agreement
    token_count = len(message.split())
    margin = abs(effective_ml - 0.5) * 2.0  # 0..1
    agreement_bonus = 0.12 if (
        (effective_ml >= 0.6 and capped_heuristics >= 16)
        or (effective_ml <= 0.35 and capped_heuristics == 0)
    ) else -0.08
    length_factor = 1.0 if token_count >= 12 else 0.78
    raw_conf = (0.50 + 0.40 * margin + agreement_bonus) * length_factor
    model_confidence = round(max(0.35, min(0.97, raw_conf)), 2)

    if effective_ml >= 0.60:
        reasons_en.insert(
            0,
            f"TF-IDF + Logistic Regression classifier flagged scam language patterns (ML probability {effective_ml * 100:.1f}%).",
        )
        reasons_bn.insert(
            0,
            f"মেশিন লার্নিং মডেল বার্তাটিতে ফিশিং বা প্রতারণামূলক ভাষার ধরন শনাক্ত করেছে (ML সম্ভাবনা {effective_ml * 100:.1f}%)।",
        )
    elif not reasons_en:
        reasons_en.append(
            f"No high-risk phishing heuristics triggered; ML classifier probability is low ({effective_ml * 100:.1f}%)."
        )
        reasons_bn.append(
            f"কোনো উচ্চ-ঝুঁকির ফিশিং সংকেত পাওয়া যায়নি এবং ML মডেলে ঝুঁকির সম্ভাবনা কম ({effective_ml * 100:.1f}%)।"
        )

    recommendations = _build_recommendations(risk_category, matched_categories, channel, language)

    tactic_catalog = {
        "urgency_pressure": ("Urgency & Fear Manipulation", "জরুরি চাপ ও ভীতি প্রদর্শন", "high"),
        "credential_or_otp_request": ("Credential / OTP Harvesting", "পাসওয়ার্ড ও OTP চুরি", "critical"),
        "suspicious_payment_or_upi_scam": ("Financial / UPI Fraud Lure", "আর্থিক ও UPI প্রতারণার ফাঁদ", "critical"),
        "impersonation_authority": ("Authority / Brand Impersonation", "পরিচিত প্রতিষ্ঠান বা ব্যাংকের ছদ্মবেশ", "high"),
        "remote_access_or_malware": ("Remote Access / Malware Delivery", "রিমোট অ্যাক্সেস বা ম্যালওয়্যার", "critical"),
        "suspicious_link_or_shortener": ("Deceptive Link / Disposable TLD", "সন্দেহজনক লিঙ্ক বা শর্টনার", "high"),
        "secrecy_or_bypass": ("Secrecy & Verification Bypass", "গোপনীয়তা ও যাচাই এড়ানো", "high"),
    }
    social_engineering_tactics: List[Dict[str, Any]] = []
    for cat in matched_categories:
        label_en, label_bn, sev = tactic_catalog.get(
            cat, (cat.replace("_", " ").title(), cat.replace("_", " ").title(), "medium")
        )
        matches_for_cat = [h["phrase"] for h in merged_highlights if h["category"] == cat]
        social_engineering_tactics.append(
            {
                "category": cat,
                "label": label_bn if language == "bn" else label_en,
                "severity": sev,
                "match_count": len(matches_for_cat),
                "evidence_examples": matches_for_cat[:3],
            }
        )

    return {
        "channel": channel,
        "sender_hint": sender_hint,
        "message_excerpt": (message[:210] + "...") if len(message) > 210 else message,
        "raw_message": message,
        "risk_score": risk_score,
        "risk_category": risk_category,
        "ml_probability": round(effective_ml, 4),
        "model_confidence": model_confidence,
        "highlighted_phrases": merged_highlights,
        "social_engineering_tactics": social_engineering_tactics,
        "reasons": reasons_bn if language == "bn" else reasons_en,
        "recommendations": recommendations,
    }


def _build_recommendations(
    risk_category: str,
    categories: set[str],
    channel: str,
    language: str,
) -> List[str]:
    if language == "bn":
        if risk_category in ("High Risk", "Critical Risk"):
            recs = [
                "এই বার্তার কোনো লিঙ্কে ক্লিক করবেন না এবং কোনো অ্যাটাচমেন্ট বা APK ফাইল ডাউনলোড করবেন না।",
                "কখনোই OTP, UPI PIN, ATM PIN বা পাসওয়ার্ড শেয়ার করবেন না — টাকা পাওয়ার জন্য কখনোই UPI PIN লাগে না।",
                "ব্যাংক, সাপ্লায়ার বা অফিসের অফিসিয়াল নম্বর বা পূর্বপরিচিত নম্বরে সরাসরি ফোন করে যাচাই করুন।",
            ]
            if "remote_access_or_malware" in categories:
                recs.append("AnyDesk বা TeamViewer-এর মতো রিমোট-অ্যাক্সেস অ্যাপ ইনস্টল করবেন না এবং স্ক্রিন শেয়ার করবেন না।")
            if channel == "email":
                recs.append("এই ইমেইলটি ফিশিং হিসেবে রিপোর্ট করুন এবং সাইবার ক্রাইম হেল্পলাইন ১৯৩০ বা cybercrime.gov.in-এ জানান।")
            return recs
        if risk_category == "Moderate Risk":
            return [
                "লিঙ্কে ক্লিক করার আগে প্রেরকের আসল ইমেইল ডোমেইন বা ফোন নম্বর ভালোভাবে যাচাই করুন।",
                "কোনো পেমেন্ট বা অ্যাকাউন্ট পরিবর্তনের আগে আলাদা বিশ্বস্ত চ্যানেল থেকে নিশ্চিত হয়ে নিন।",
            ]
        return [
            "বার্তাটিতে বড় কোনো ফিশিং সংকেত পাওয়া যায়নি, তবে পেমেন্ট বা লগইনের ক্ষেত্রে সবসময় অফিসিয়াল অ্যাপ বা ওয়েবসাইট ব্যবহার করুন।",
        ]

    if risk_category in ("High Risk", "Critical Risk"):
        recs = [
            "Do not click any links, scan QR codes, or download attachments from this message.",
            "Never share OTP, UPI PIN, CVV, or passwords — receiving money never requires entering a UPI PIN.",
            "Verify the request independently by calling the bank, vendor, or colleague on a previously known trusted phone number.",
        ]
        if "remote_access_or_malware" in categories:
            recs.append("Do not install AnyDesk, TeamViewer, or unknown APK files, and never grant remote screen access.")
        if "suspicious_payment_or_upi_scam" in categories:
            recs.append("Freeze any pending bank transfer with your accounts team until out-of-band voice verification is completed.")
        recs.append(
            "If anyone in your business already clicked or shared credentials, immediately open the CyberShield Incident Response Center and report financial fraud on India helpline 1930 / cybercrime.gov.in."
        )
        return recs

    if risk_category == "Moderate Risk":
        return [
            "Treat this message with caution and inspect the exact sender email domain or phone number.",
            "Navigate directly to the official website or app by typing its address yourself instead of using embedded links.",
            "Confirm any financial or account update through a second trusted channel.",
        ]

    return [
        "No strong phishing indicators were detected, though automated tools cannot guarantee 100% safety.",
        "Continue verifying unexpected payment requests via phone and keep MFA enabled on business accounts.",
    ]

