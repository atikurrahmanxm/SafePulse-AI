"""10-domain Small Business Security Health Check aligned with CERT-In MSME guidance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class AssessmentQuestion:
    key: str
    domain: str
    domain_label_en: str
    domain_label_bn: str
    weight: int
    prompt_en: str
    prompt_bn: str
    guidance_en: str
    guidance_bn: str
    recommendation_en: str
    recommendation_bn: str


ASSESSMENT_QUESTIONS: List[AssessmentQuestion] = [
    AssessmentQuestion(
        key="passwords",
        domain="passwords",
        domain_label_en="Password Security",
        domain_label_bn="পাসওয়ার্ড নিরাপত্তা",
        weight=10,
        prompt_en="Do all business accounts (email, banking, POS, social media) use unique, strong passwords (12+ characters) managed safely?",
        prompt_bn="ব্যবসার সব অ্যাকাউন্টে (ইমেইল, ব্যাংকিং, POS, সোশ্যাল মিডিয়া) কি আলাদা ও শক্তিশালী পাসওয়ার্ড (১২+ অক্ষর) ব্যবহার করা হয়?",
        guidance_en="CERT-In MSME Guidance: Avoid reusing passwords across billing, email, and bank portals.",
        guidance_bn="CERT-In পরামর্শ: একই পাসওয়ার্ড একাধিক ব্যবসায়িক পোর্টালে ব্যবহার করবেন না।",
        recommendation_en="Enforce unique 12+ character passphrases across all business portals and adopt a password manager.",
        recommendation_bn="সব ব্যবসায়িক অ্যাকাউন্টে ১২+ অক্ষরের আলাদা পাসওয়ার্ড এবং পাসওয়ার্ড ম্যানেজার ব্যবহার শুরু করুন।",
    ),
    AssessmentQuestion(
        key="mfa",
        domain="mfa",
        domain_label_en="Multi-Factor Authentication",
        domain_label_bn="মাল্টি-ফ্যাক্টর অথেনটিকেশন (MFA)",
        weight=14,
        prompt_en="Is Multi-Factor Authentication (MFA / 2FA app or hardware key) enabled on business email, banking, GST, and admin portals?",
        prompt_bn="ব্যবসায়িক ইমেইল, ব্যাংকিং, GST এবং অ্যাডমিন পোর্টালে কি MFA / ২-স্তরের নিরাপত্তা চালু আছে?",
        guidance_en="MFA blocks over 99% of automated password-stuffing and credential phishing takeovers.",
        guidance_bn="পাসওয়ার্ড ফাঁস হলেও MFA অ্যাকাউন্ট দখল হওয়া থেকে রক্ষা করে।",
        recommendation_en="Enable authenticator-app MFA immediately on primary email, payment gateways, and accounting tools.",
        recommendation_bn="প্রাথমিক ইমেইল, পেমেন্ট ড্যাশবোর্ড ও অ্যাকাউন্টিং টুলে অবিলম্বে অথেনটিকেটর অ্যাপ ভিত্তিক MFA চালু করুন।",
    ),
    AssessmentQuestion(
        key="email_security",
        domain="email_security",
        domain_label_en="Email Security",
        domain_label_bn="ইমেইল নিরাপত্তা",
        weight=10,
        prompt_en="Does your business email use spam/phishing filtering, SPF/DMARC records (if custom domain), and staff verification before opening attachments?",
        prompt_bn="আপনার ব্যবসার ইমেইলে কি স্প্যাম/ফিশিং ফিল্টার, SPF/DMARC এবং অ্যাটাচমেন্ট খোলার আগে যাচাই করার নিয়ম আছে?",
        guidance_en="Most SMB breaches and fake-invoice scams enter through business email.",
        guidance_bn="অধিকাংশ সাইবার আক্রমণ ও ভুয়া ইনভয়েস প্রতারণা ইমেইলের মাধ্যমে আসে।",
        recommendation_en="Enable strict phishing filtering and configure SPF, DKIM, and DMARC records on your business domain.",
        recommendation_bn="ইমেইলে কঠোর ফিশিং ফিল্টার চালু করুন এবং কাস্টম ডোমেইনে SPF, DKIM ও DMARC কনফিগার করুন।",
    ),
    AssessmentQuestion(
        key="access_control",
        domain="access_control",
        domain_label_en="Employee Access Permissions",
        domain_label_bn="কর্মীদের অ্যাক্সেস নিয়ন্ত্রণ",
        weight=10,
        prompt_en="Do staff members have individual accounts with least-privilege access, and are former employees' logins revoked immediately?",
        prompt_bn="কর্মীদের কি আলাদা লগইন ও প্রয়োজনের সীমিত অ্যাক্সেস আছে এবং চাকরি ছাড়লে কি সাথে সাথে অ্যাক্সেস বাতিল করা হয়?",
        guidance_en="Shared logins prevent accountability and keep ex-staff able to access customer or financial data.",
        guidance_bn="শেয়ার করা লগইন ঝুঁকিপূর্ণ; প্রাক্তন কর্মীদের অ্যাক্সেস সাথে সাথে বন্ধ করা জরুরি।",
        recommendation_en="Eliminate shared admin logins, assign role-based permissions, and create an offboarding revocation checklist.",
        recommendation_bn="শেয়ার করা অ্যাডমিন লগইন বন্ধ করে আলাদা ইউজার অ্যাকাউন্ট ও অফবোর্ডিং চেকলিস্ট চালু করুন।",
    ),
    AssessmentQuestion(
        key="updates",
        domain="updates",
        domain_label_en="Software Updates",
        domain_label_bn="সফটওয়্যার আপডেট",
        weight=10,
        prompt_en="Are operating systems, web browsers, billing/POS software, and accounting tools updated automatically or monthly?",
        prompt_bn="কম্পিউটার, মোবাইল, ব্রাউজার, বিলিং/POS এবং অ্যাকাউন্টিং সফটওয়্যার কি নিয়মিত আপডেট করা হয়?",
        guidance_en="Unpatched software is a primary entry vector for ransomware and credential stealers.",
        guidance_bn="পুরনো ও আপডেটহীন সফটওয়্যার র‍্যানসমওয়্যার আক্রমণের প্রধান কারণ।",
        recommendation_en="Turn on automatic OS, browser, and antivirus updates on all billing counters and office laptops.",
        recommendation_bn="সব বিলিং কম্পিউটার ও অফিস ল্যাপটপে স্বয়ংক্রিয় OS, ব্রাউজার ও অ্যান্টিভাইরাস আপডেট চালু করুন।",
    ),
    AssessmentQuestion(
        key="backups",
        domain="backups",
        domain_label_en="Data Backup",
        domain_label_bn="ডেটা ব্যাকআপ",
        weight=12,
        prompt_en="Are critical billing, Tally/accounting, and customer records backed up automatically to an offline or immutable cloud location (3-2-1 rule) and tested?",
        prompt_bn="গুরুত্বপূর্ণ বিলিং, হিসাব এবং গ্রাহকের ডেটা কি নিয়মিত অফলাইন বা ক্লাউডে নিরাপদ ব্যাকআপ রাখা ও পরীক্ষা করা হয়?",
        guidance_en="Backups connected permanently to the billing PC can also be encrypted by ransomware.",
        guidance_bn="বিলিং পিসির সাথে সবসময় যুক্ত থাকা পেনড্রাইভ র‍্যানসমওয়্যারে আক্রান্ত হতে পারে; আলাদা অফলাইন/ক্লাউড ব্যাকআপ রাখুন।",
        recommendation_en="Implement automated daily backups with at least one disconnected/immutable copy and test restoration monthly.",
        recommendation_bn="দৈনিক স্বয়ংক্রিয় ব্যাকআপ এবং অন্তত একটি বিচ্ছিন্ন অফলাইন বা ইমিউটেবল ক্লাউড ব্যাকআপ চালু করুন।",
    ),
    AssessmentQuestion(
        key="data_protection",
        domain="data_protection",
        domain_label_en="Sensitive Data Protection",
        domain_label_bn="সংবেদনশীল তথ্য সুরক্ষা",
        weight=8,
        prompt_en="Are customer records, prescriptions/invoices, Aadhaar/PAN copies, and financial files encrypted and restricted from personal WhatsApp/USB sharing?",
        prompt_bn="গ্রাহকের তথ্য, বিল, PAN/আধার কপি ও আর্থিক ফাইল কি সুরক্ষিত রাখা হয় এবং ব্যক্তিগত হোয়াটসঅ্যাপ বা USB-তে পাঠানো সীমিত?",
        guidance_en="CERT-In MSME Guidance: Minimize storing unnecessary ID copies and avoid unencrypted spreadsheets on shared counters.",
        guidance_bn="অপ্রয়োজনীয় ID কপি সংরক্ষণ কমিয়ে আনুন এবং শেয়ার করা কম্পিউটারে এনক্রিপশন ব্যবহার করুন।",
        recommendation_en="Enable full-disk encryption (BitLocker/FileVault) and restrict exporting customer lists to personal devices.",
        recommendation_bn="ডিভাইসে ডিস্ক এনক্রিপশন চালু করুন এবং ব্যক্তিগত ডিভাইসে গ্রাহক ডেটা কপি করা বন্ধ করুন।",
    ),
    AssessmentQuestion(
        key="device_security",
        domain="device_security",
        domain_label_en="Device Security",
        domain_label_bn="ডিভাইস নিরাপত্তা",
        weight=8,
        prompt_en="Do all shop PCs, POS terminals, and work phones have screen locks, endpoint protection/antivirus, and disabled unknown app sideloading?",
        prompt_bn="দোকানের পিসি, POS মেশিন ও কাজের ফোনে কি স্ক্রিন লক, অ্যান্টিভাইরাস এবং অজানা APK ইনস্টলেশন বন্ধ আছে?",
        guidance_en="Malicious APK files shared over WhatsApp are a major infection source for Indian small businesses.",
        guidance_bn="হোয়াটসঅ্যাপে আসা অজানা APK ফাইল ছোট ব্যবসার ফোনের জন্য বড় হুমকি।",
        recommendation_en="Enable auto-lock (<5 min), built-in/reputable endpoint antivirus, and block unknown APK sideloading on business phones.",
        recommendation_bn="স্বয়ংক্রিয় স্ক্রিন লক, অ্যান্টিভাইরাস চালু রাখুন এবং ব্যবসার ফোনে অজানা APK ইনস্টল বন্ধ করুন।",
    ),
    AssessmentQuestion(
        key="wifi_security",
        domain="wifi_security",
        domain_label_en="Wi-Fi Security",
        domain_label_bn="ওয়াই-ফাই নিরাপত্তা",
        weight=8,
        prompt_en="Does your business Wi-Fi use WPA2/WPA3 encryption, a changed router admin password, and a separate guest network for visitors?",
        prompt_bn="ব্যবসার ওয়াই-ফাইতে কি WPA2/WPA3 এনক্রিপশন, পরিবর্তিত রাউটার অ্যাডমিন পাসওয়ার্ড এবং অতিথিদের জন্য আলাদা নেটওয়ার্ক আছে?",
        guidance_en="Default router passwords let nearby attackers intercept traffic or alter DNS settings.",
        guidance_bn="ডিফল্ট রাউটার পাসওয়ার্ড থাকলে হ্যাকাররা সহজেই নেটওয়ার্কে প্রবেশ করতে পারে।",
        recommendation_en="Change default router admin credentials, enforce WPA2/WPA3, and isolate billing POS devices from customer Wi-Fi.",
        recommendation_bn="রাউটারের ডিফল্ট পাসওয়ার্ড পরিবর্তন করুন, WPA2/WPA3 ব্যবহার করুন এবং গ্রাহক ও বিলিং নেটওয়ার্ক আলাদা রাখুন।",
    ),
    AssessmentQuestion(
        key="incident_readiness",
        domain="incident_readiness",
        domain_label_en="Incident Response Preparedness",
        domain_label_bn="সাইবার ঘটনা মোকাবেলা প্রস্তুতি",
        weight=10,
        prompt_en="Does your team have an emergency checklist (bank fraud numbers, helpline 1930, IT contact) and know how to report suspicious links or payments?",
        prompt_bn="সাইবার প্রতারণা বা সন্দেহজনক কিছু হলে করণীয় চেকলিস্ট (ব্যাংক ফ্রড নম্বর, হেল্পলাইন ১৯৩০) কি আপনার টিমের জানা আছে?",
        guidance_en="CERT-In MSME Guidance: Rapid reporting within the 'golden hour' greatly improves financial fraud recovery.",
        guidance_bn="প্রতারণার প্রথম ঘণ্টার মধ্যে ১৯৩০ নম্বরে জানালে টাকা ফেরত পাওয়ার সম্ভাবনা অনেক বাড়ে।",
        recommendation_en="Keep CyberShield Incident Playbooks accessible to all staff and post bank freeze + 1930 helpline contacts at the counter.",
        recommendation_bn="সব কর্মীকে ১৯৩০ হেল্পলাইন ও ব্যাংকের জরুরি ফ্রড নম্বরের তালিকা দিন এবং ইনসিডেন্ট চেকলিস্ট অনুশীলন করুন।",
    ),
]

ANSWER_MULTIPLIERS = {
    "yes": 1.0,
    "partial": 0.5,
    "no": 0.0,
}


def classify_security_health(score: int) -> str:
    if score < 30:
        return "Critical"
    if score < 50:
        return "Weak"
    if score < 70:
        return "Moderate"
    if score < 85:
        return "Good"
    return "Strong"


def get_questionnaire(language: str = "en") -> List[Dict[str, Any]]:
    return [
        {
            "key": q.key,
            "domain": q.domain,
            "domain_label": q.domain_label_bn if language == "bn" else q.domain_label_en,
            "weight": q.weight,
            "prompt": q.prompt_bn if language == "bn" else q.prompt_en,
            "guidance": q.guidance_bn if language == "bn" else q.guidance_en,
        }
        for q in ASSESSMENT_QUESTIONS
    ]


def evaluate_assessment(answers: Dict[str, str], language: str = "en") -> Dict[str, Any]:
    total_weight = sum(q.weight for q in ASSESSMENT_QUESTIONS)
    earned_weight = 0.0
    category_scores: Dict[str, int] = {}
    weak_areas: List[str] = []
    critical_gaps: List[str] = []
    recommendations: List[Dict[str, Any]] = []
    answer_rows: List[Dict[str, Any]] = []

    for q in ASSESSMENT_QUESTIONS:
        raw_ans = (answers.get(q.key) or "no").strip().lower()
        if raw_ans not in ANSWER_MULTIPLIERS:
            raise ValueError(f"Invalid answer '{raw_ans}' for '{q.key}'. Expected 'yes', 'partial', or 'no'.")

        mult = ANSWER_MULTIPLIERS[raw_ans]
        points = round(q.weight * mult)
        earned_weight += q.weight * mult
        domain_pct = int(round(mult * 100))

        domain_label = q.domain_label_bn if language == "bn" else q.domain_label_en
        category_scores[q.key] = domain_pct

        answer_rows.append(
            {
                "question_key": q.key,
                "domain": q.domain,
                "answer_value": raw_ans,
                "score_awarded": points,
                "max_score": q.weight,
            }
        )

        if raw_ans == "no":
            critical_gaps.append(domain_label)
            weak_areas.append(domain_label)
            recommendations.append(
                {
                    "domain": q.key,
                    "domain_label": domain_label,
                    "priority": "Critical" if q.weight >= 10 else "High",
                    "action": q.recommendation_bn if language == "bn" else q.recommendation_en,
                }
            )
        elif raw_ans == "partial":
            weak_areas.append(domain_label)
            recommendations.append(
                {
                    "domain": q.key,
                    "domain_label": domain_label,
                    "priority": "Medium",
                    "action": q.recommendation_bn if language == "bn" else q.recommendation_en,
                }
            )

    overall_score = max(0, min(100, int(round((earned_weight / total_weight) * 100))))
    security_category = classify_security_health(overall_score)

    priority_rank = {"Critical": 0, "High": 1, "Medium": 2}
    recommendations.sort(key=lambda r: priority_rank.get(r["priority"], 3))

    return {
        "overall_score": overall_score,
        "security_category": security_category,
        "category_scores": category_scores,
        "weak_areas": weak_areas,
        "critical_gaps": critical_gaps,
        "recommendations": recommendations,
        "answer_rows": answer_rows,
    }

