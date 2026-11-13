"""Guided Cyber Incident Response playbooks for small businesses (7 scenarios, 6 phases)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class StepDef:
    phase: str
    title_en: str
    title_bn: str
    guidance_en: str
    guidance_bn: str


@dataclass(frozen=True)
class ScenarioDef:
    key: str
    title_en: str
    title_bn: str
    severity: str
    summary_en: str
    summary_bn: str
    steps: List[StepDef]


PHASES = [
    "Immediate Actions",
    "Containment Steps",
    "Account Protection",
    "Evidence Preservation",
    "Recovery Guidance",
    "Reporting Recommendations",
]


def _build_steps(specific_steps: List[StepDef]) -> List[StepDef]:
    return specific_steps


INCIDENT_SCENARIOS: Dict[str, ScenarioDef] = {
    "suspicious_email": ScenarioDef(
        key="suspicious_email",
        title_en="Suspicious Email Received",
        title_bn="সন্দেহজনক ইমেইল পাওয়া গেছে",
        severity="Medium",
        summary_en="An employee or owner received an unexpected email asking for urgent payment, login verification, or attachment download.",
        summary_bn="কর্মী বা মালিকের কাছে জরুরি পেমেন্ট, লগইন যাচাই বা অ্যাটাচমেন্ট ডাউনলোডের সন্দেহজনক ইমেইল এসেছে।",
        steps=[
            StepDef(
                "Immediate Actions",
                "Stop all interaction with the email",
                "ইমেইলটির সাথে সব ধরনের ইন্টারঅ্যাকশন বন্ধ করুন",
                "Do not reply, click links, download attachments, or call phone numbers listed inside the email.",
                "ইমেইলে উত্তর দেবেন না, কোনো লিঙ্কে ক্লিক করবেন না এবং কোনো ফাইল ডাউনলোড করবেন না।",
            ),
            StepDef(
                "Containment Steps",
                "Alert staff and isolate the message",
                "কর্মীদের সতর্ক করুন এবং মেসেজটি আলাদা করুন",
                "Check if the same email was sent to other team members and warn everyone at the counter/office immediately.",
                "অন্য কোনো কর্মীর কাছেও একই ইমেইল এসেছে কি না দেখুন এবং সবাইকে সতর্ক করুন।",
            ),
            StepDef(
                "Account Protection",
                "Verify sender out-of-band and check rules",
                "অন্য মাধ্যমে প্রেরক যাচাই করুন",
                "If the email claims to be a supplier or bank, call their previously saved official number. Check email forwarding rules if anyone opened it.",
                "ইমেইলটি ব্যাংক বা সাপ্লায়ারের দাবি করলে আগে থেকে সংরক্ষিত অফিসিয়াল নম্বরে কল করে যাচাই করুন।",
            ),
            StepDef(
                "Evidence Preservation",
                "Save the email headers and screenshot",
                "ইমেইলের হেডার ও স্ক্রিনশট সংরক্ষণ করুন",
                "Keep a copy of the sender address, subject line, and full email headers before deleting from the primary inbox.",
                "ডিলিট করার আগে প্রেরকের আসল ইমেইল ঠিকানা, সাবজেক্ট ও স্ক্রিনশট সংরক্ষণ করুন।",
            ),
            StepDef(
                "Recovery Guidance",
                "Mark as phishing and block sender domain",
                "ইমেইলটি ফিশিং হিসেবে মার্ক ও ব্লক করুন",
                "Use your email provider's 'Report Phishing' button and block the sender address for your organization.",
                "ইমেইল প্রোভাইডারের 'Report Phishing' অপশন ব্যবহার করুন এবং প্রেরককে ব্লক করুন।",
            ),
            StepDef(
                "Reporting Recommendations",
                "Report impersonation campaigns if targeted",
                "টার্গেটেড আক্রমণ হলে রিপোর্ট করুন",
                "Forward brand/bank impersonation lures to the genuine bank's phishing desk or report at cybercrime.gov.in if financial loss was attempted.",
                "ব্যাংক বা সরকারি প্রতিষ্ঠানের নাম নকল করলে সংশ্লিষ্ট প্রতিষ্ঠানের ফ্রড ডেস্কে বা cybercrime.gov.in-এ জানান।",
            ),
        ],
    ),
    "phishing_link_clicked": ScenarioDef(
        key="phishing_link_clicked",
        title_en="Phishing Link Clicked",
        title_bn="ফিশিং লিঙ্কে ক্লিক করা হয়েছে",
        severity="High",
        summary_en="Someone opened a suspicious link and may have typed a password, OTP, or downloaded a file.",
        summary_bn="কেউ একটি সন্দেহজনক লিঙ্কে ক্লিক করেছেন এবং পাসওয়ার্ড বা OTP দিয়ে থাকতে পারেন।",
        steps=[
            StepDef(
                "Immediate Actions",
                "Disconnect device from Wi-Fi/mobile data if download started",
                "ফাইল ডাউনলোড হলে সাথে সাথে ইন্টারনেট সংযোগ বিচ্ছিন্ন করুন",
                "If an APK or executable file downloaded or ran, turn off Wi-Fi/hotspot immediately to stop background data theft.",
                "যদি কোনো APK বা সফটওয়্যার ডাউনলোড হয়ে থাকে, তবে সাথে সাথে ডিভাইসের Wi-Fi ও মোবাইল ডেটা বন্ধ করুন।",
            ),
            StepDef(
                "Containment Steps",
                "Terminate active browser sessions",
                "সক্রিয় ব্রাউজার সেশন বন্ধ করুন",
                "Close the suspicious webpage immediately and clear browser cookies/sessions for any account entered on that page.",
                "সন্দেহজনক পেজটি বন্ধ করুন এবং সেখানে কোনো অ্যাকাউন্ট ব্যবহার করলে সব সেশন থেকে লগ-আউট করুন।",
            ),
            StepDef(
                "Account Protection",
                "Reset passwords and revoke active sessions from a clean device",
                "নিরাপদ ডিভাইস থেকে পাসওয়ার্ড পরিবর্তন ও MFA চালু করুন",
                "Using a separate, clean phone/PC, change the password of the exposed account (and any account reusing that password), sign out all devices, and enable MFA.",
                "অন্য একটি নিরাপদ ডিভাইস থেকে পাসওয়ার্ড পরিবর্তন করুন, সব ডিভাইস থেকে সেশন বাতিল করুন এবং MFA চালু করুন।",
            ),
            StepDef(
                "Evidence Preservation",
                "Record URL, time, and actions taken",
                "লিঙ্ক, সময় এবং কী তথ্য দেওয়া হয়েছে তা লিখে রাখুন",
                "Note down the exact URL clicked, time of click, and whether passwords, card details, or OTPs were entered.",
                "কখন কোন লিঙ্কে ক্লিক হয়েছে এবং কোনো পাসওয়ার্ড বা OTP দেওয়া হয়েছে কি না তা নোট করুন।",
            ),
            StepDef(
                "Recovery Guidance",
                "Run full antivirus/malware scan",
                "ডিভাইসে পূর্ণাঙ্গ অ্যান্টিভাইরাস স্ক্যান করুন",
                "Run a full scan with Windows Security / reputable endpoint antivirus before reconnecting the machine to billing/POS networks.",
                "বিলিং নেটওয়ার্কে পুনরায় যুক্ত করার আগে ডিভাইসে সম্পূর্ণ অ্যান্টিভাইরাস স্ক্যান চালান।",
            ),
            StepDef(
                "Reporting Recommendations",
                "Alert bank & helpline 1930 if financial info entered",
                "আর্থিক তথ্য দিলে সাথে সাথে ব্যাংক ও ১৯৩০ নম্বরে জানান",
                "If banking credentials, PIN, or OTP were entered, immediately call your bank's fraud desk and dial 1930 (India Cyber Crime Helpline).",
                "ব্যাংকিং তথ্য, PIN বা OTP দিয়ে থাকলে অবিলম্বে ব্যাংকের ফ্রড হেল্পলাইন এবং ১৯৩০ নম্বরে কল করুন।",
            ),
        ],
    ),
    "bec_compromised": ScenarioDef(
        key="bec_compromised",
        title_en="Business Email Compromised (BEC)",
        title_bn="ব্যবসায়িক ইমেইল হ্যাক হয়েছে (BEC)",
        severity="Critical",
        summary_en="Unauthorized login, suspicious sent emails, or hidden inbox forwarding rules detected on a business mailbox.",
        summary_bn="ব্যবসায়িক ইমেইলে অজানা লগইন, অচেনা পাঠানো ইমেইল বা গোপন ফরওয়ার্ডিং নিয়ম দেখা গেছে।",
        steps=[
            StepDef(
                "Immediate Actions",
                "Lock mailbox and revoke all active sessions",
                "মেইলবক্সের সব সেশন বাতিল ও পাসওয়ার্ড রিসেট করুন",
                "From admin console or account security page, force sign-out of all sessions and set a fresh, unique 14+ character password.",
                "অ্যাকাউন্ট সিকিউরিটি সেটিংস থেকে সব ডিভাইস থেকে সাইন-আউট করুন এবং নতুন শক্তিশালী পাসওয়ার্ড দিন।",
            ),
            StepDef(
                "Containment Steps",
                "Inspect and remove unauthorized inbox/forwarding rules",
                "ইমেইলের গোপন ফরওয়ার্ডিং ও ফিল্টার নিয়ম মুছে ফেলুন",
                "Attackers routinely add silent forwarding or auto-delete rules so owners miss replies. Check Settings -> Forwarding / Filters and remove unknown rules.",
                "হ্যাকাররা প্রায়ই গোপন ইমেইল ফরওয়ার্ডিং বা অটো-ডিলিট ফিল্টার সেট করে; সেটিংস থেকে অজানা নিয়ম মুছুন।",
            ),
            StepDef(
                "Account Protection",
                "Enforce App-based MFA & review OAuth apps",
                "অ্যাপ-ভিত্তিক MFA চালু ও থার্ড-পার্টি অ্যাপ পরীক্ষা করুন",
                "Enable authenticator-app MFA on the compromised mailbox and remove unknown connected third-party apps or app passwords.",
                "অথেনটিকেটর অ্যাপ MFA চালু করুন এবং যুক্ত থাকা অজানা থার্ড-পার্টি অ্যাপ অ্যাক্সেস সরিয়ে দিন।",
            ),
            StepDef(
                "Evidence Preservation",
                "Export login IP history and sent folder logs",
                "লগইন IP ইতিহাস ও Sent ফোল্ডারের রেকর্ড সংরক্ষণ করুন",
                "Screenshot recent sign-in activity (IP, location, timestamp) and save copies of any fraudulent emails sent to vendors or customers.",
                "সন্দেহজনক লগইন IP, সময় এবং আপনার ঠিকানা থেকে পাঠানো ভুয়া ইমেইলের কপি সংরক্ষণ করুন।",
            ),
            StepDef(
                "Recovery Guidance",
                "Warn vendors and customers about fake bank changes",
                "সাপ্লায়ার ও গ্রাহকদের ভুয়া পেমেন্ট নির্দেশনা সম্পর্কে সতর্ক করুন",
                "Call key suppliers and clients who received emails recently to confirm no payments were redirected to attacker bank accounts.",
                "সাম্প্রতিক সময়ে যাদের ইমেইল পাঠানো হয়েছে, তাদের ফোন করে কোনো ব্যাংক অ্যাকাউন্ট পরিবর্তনের অনুরোধ বিশ্বাস না করতে বলুন।",
            ),
            StepDef(
                "Reporting Recommendations",
                "File formal complaint on cybercrime.gov.in & CERT-In",
                "cybercrime.gov.in ও CERT-In-এ অভিযোগ দায়ের করুন",
                "Report business email compromise on cybercrime.gov.in and notify affected partners in writing.",
                "cybercrime.gov.in পোর্টালে রিপোর্ট করুন এবং ক্ষতিগ্রস্ত ব্যবসায়িক পার্টনারদের লিখিতভাবে জানান।",
            ),
        ],
    ),
    "social_media_compromised": ScenarioDef(
        key="social_media_compromised",
        title_en="Social Media / WhatsApp Business Compromised",
        title_bn="সোশ্যাল মিডিয়া বা হোয়াটসঅ্যাপ বিজনেস হ্যাক হয়েছে",
        severity="High",
        summary_en="Your shop Facebook, Instagram, or WhatsApp Business account is posting scam links or messaging contacts for money.",
        summary_bn="আপনার দোকানের ফেসবুক, ইনস্টাগ্রাম বা হোয়াটসঅ্যাপ থেকে পরিচিতদের কাছে টাকা চেয়ে মেসেজ যাচ্ছে।",
        steps=[
            StepDef(
                "Immediate Actions",
                "Warn customers & contacts via alternate channel",
                "অন্য মাধ্যমে গ্রাহক ও পরিচিতদের দ্রুত সতর্ক করুন",
                "Send a broadcast/SMS or post from a personal/verified secondary channel telling contacts not to send money or codes.",
                "ব্যক্তিগত ফোন বা অন্য চ্যানেল থেকে পরিচিত ও গ্রাহকদের জানান যেন কোনো টাকা বা OTP না দেন।",
            ),
            StepDef(
                "Containment Steps",
                "Remove unauthorized linked devices or page admins",
                "অজানা লিঙ্কড ডিভাইস বা পেজ অ্যাডমিন সরিয়ে দিন",
                "For WhatsApp, open Linked Devices and log out all unknown sessions. For Meta/Instagram, remove unrecognized Business Manager admins.",
                "হোয়াটসঅ্যাপে Linked Devices থেকে অজানা ডিভাইস লগ-আউট করুন এবং ফেসবুক/ইনস্টাগ্রাম থেকে অজানা অ্যাডমিন সরান।",
            ),
            StepDef(
                "Account Protection",
                "Re-verify SIM/account and enable Two-Step PIN",
                "Two-Step Verification PIN চালু ও পাসওয়ার্ড পরিবর্তন করুন",
                "Trigger official account recovery inside WhatsApp / Meta Accounts Center, change linked email password, and enable 2-step verification PIN.",
                "অফিসিয়াল অ্যাকাউন্ট রিকভারি ব্যবহার করুন, যুক্ত ইমেইলের পাসওয়ার্ড বদলান এবং ২-স্তরের PIN চালু করুন।",
            ),
            StepDef(
                "Evidence Preservation",
                "Capture screenshots of scam messages and attacker handles",
                "স্ক্যাম মেসেজ ও হ্যাকারের তথ্যের স্ক্রিনশট রাখুন",
                "Save screenshots of fraudulent posts, UPI IDs, or phone numbers used by attackers before deleting them.",
                "প্রতারকদের ব্যবহৃত UPI আইডি, ফোন নম্বর ও ভুয়া পোস্টের স্ক্রিনশট সংরক্ষণ করুন।",
            ),
            StepDef(
                "Recovery Guidance",
                "Audit ad accounts and connected payment cards",
                "বিজ্ঞাপন অ্যাকাউন্ট ও যুক্ত কার্ড পরীক্ষা করুন",
                "Check Meta Ads Manager for unauthorized ad spend and temporarily pause/replace any linked debit or credit card if needed.",
                "Meta Ads Manager-এ অজানা কোনো বিজ্ঞাপনের খরচ হয়েছে কি না দেখুন এবং প্রয়োজনে কার্ড ব্লক করুন।",
            ),
            StepDef(
                "Reporting Recommendations",
                "Submit platform hijack report & cybercrime complaint",
                "প্ল্যাটফর্ম সাপোর্ট ও সাইবার ক্রাইম পোর্টালে রিপোর্ট করুন",
                "Use official Meta/WhatsApp hacked-account support channels (note: SafePulse AI cannot recover accounts directly) and file a police/cybercrime report if contacts lost money.",
                "অফিসিয়াল WhatsApp/Meta হেল্প সেন্টারে রিপোর্ট করুন (SafePulse AI সরাসরি অ্যাকাউন্ট ফেরত দিতে পারে না) এবং আর্থিক ক্ষতি হলে ১৯৩০-এ জানান।",
            ),
        ],
    ),
    "suspicious_transaction": ScenarioDef(
        key="suspicious_transaction",
        title_en="Suspicious Financial Transaction / UPI Fraud",
        title_bn="সন্দেহজনক আর্থিক লেনদেন বা UPI প্রতারণা",
        severity="Critical",
        summary_en="An unauthorized bank debit, UPI transfer, or payment to a suspected scammer just occurred.",
        summary_bn="অননুমোদিত ব্যাংক ডেবিট, UPI ট্রান্সফার বা সন্দেহজনক প্রতারকের কাছে টাকা চলে গেছে।",
        steps=[
            StepDef(
                "Immediate Actions",
                "Call India Cyber Crime Helpline 1930 IMMEDIATELY (Golden Hour)",
                "সাথে সাথে জাতীয় সাইবার ক্রাইম হেল্পলাইন ১৯৩০-এ কল করুন",
                "Dial 1930 immediately (or submit at cybercrime.gov.in) with transaction UTR/RRN to attempt freezing funds before scammers withdraw them.",
                "টাকা তোলার আগেই অ্যাকাউন্ট ফ্রিজ করার চেষ্টার জন্য অবিলম্বে ১৯৩০ নম্বরে কল করুন এবং UTR/RRN নম্বর দিন।",
            ),
            StepDef(
                "Containment Steps",
                "Freeze bank account / block UPI & cards",
                "ব্যাংক অ্যাকাউন্ট, UPI ও কার্ড সাময়িকভাবে ব্লক করুন",
                "Call your bank's 24x7 fraud hotline to block compromised debit/credit cards, netbanking, or UPI IDs immediately.",
                "ব্যাংকের ২৪x৭ ফ্রড হেল্পলাইনে কল করে ডেবিট/ক্রেডিট কার্ড, নেটব্যাংকিং বা UPI সাময়িকভাবে বন্ধ করুন।",
            ),
            StepDef(
                "Account Protection",
                "Change banking PINs and email passwords",
                "ব্যাংকিং পাসওয়ার্ড, MPIN ও যুক্ত ইমেইল পরিবর্তন করুন",
                "Reset netbanking passwords, UPI PINs, and the password of the email/phone linked to bank alerts from a clean device.",
                "নিরাপদ ডিভাইস থেকে নেটব্যাংকিং পাসওয়ার্ড, UPI PIN এবং ব্যাংকের সাথে যুক্ত ইমেইলের পাসওয়ার্ড পরিবর্তন করুন।",
            ),
            StepDef(
                "Evidence Preservation",
                "Collect UTR, bank statement, and chat logs",
                "UTR নম্বর, ব্যাংক স্টেটমেন্ট ও চ্যাটের প্রমাণ সংগ্রহ করুন",
                "Download transaction receipt showing UTR/Reference ID, timestamp, recipient UPI/account, and screenshot all SMS/WhatsApp chats.",
                "লেনদেনের UTR নম্বর, সময়, প্রাপকের UPI/অ্যাকাউন্ট তথ্য এবং স্ক্যামারের চ্যাটের স্ক্রিনশট সংরক্ষণ করুন।",
            ),
            StepDef(
                "Recovery Guidance",
                "Visit bank branch for written chargeback/dispute form",
                "ব্যাংকের শাখায় লিখিত অভিযোগ ও ডিসপিউট ফর্ম জমা দিন",
                "Submit a formal written fraud dispute with your bank within 24–72 hours along with the 1930 / cybercrime acknowledgement number.",
                "১৯৩০ বা cybercrime.gov.in-এর রেফারেন্স নম্বরসহ ব্যাংকের শাখায় লিখিত অভিযোগ জমা দিন।",
            ),
            StepDef(
                "Reporting Recommendations",
                "Keep acknowledgment ID for police & bank follow-up",
                "থানা ও ব্যাংকের ফলোআপের জন্য অভিযোগ নম্বর সংরক্ষণ করুন",
                "Track your complaint status on cybercrime.gov.in and provide the acknowledgement slip to your local police station if requested.",
                "cybercrime.gov.in-এ অভিযোগের অগ্রগতি দেখুন এবং প্রয়োজনে নিকটস্থ থানায় কপি জমা দিন।",
            ),
        ],
    ),
    "ransomware_suspected": ScenarioDef(
        key="ransomware_suspected",
        title_en="Ransomware or Malware Suspected",
        title_bn="র‍্যানসমওয়্যার বা ম্যালওয়্যার সন্দেহ",
        severity="Critical",
        summary_en="Files on a billing PC or server have strange extensions, ransom notes appeared, or unknown software is encrypting data.",
        summary_bn="বিলিং পিসি বা সার্ভারে ফাইল খুলছে না, ফাইলের নাম বদলে গেছে বা মুক্তিপণের বার্তা দেখা যাচ্ছে।",
        steps=[
            StepDef(
                "Immediate Actions",
                "Unplug network cable, disable Wi-Fi, and disconnect external drives",
                "সাথে সাথে নেটওয়ার্ক কেবল, Wi-Fi ও পেনড্রাইভ খুলে ফেলুন",
                "Isolate the infected PC from the shop LAN/Wi-Fi and unplug USB backup drives immediately to prevent lateral spread. Do NOT pay ransom.",
                "সংক্রমণ ছড়ানো ঠেকাতে পিসির ইন্টারনেট, LAN এবং পেনড্রাইভ/হার্ডড্রাইভ সাথে সাথে বিচ্ছিন্ন করুন। কোনো মুক্তিপণ দেবেন না।",
            ),
            StepDef(
                "Containment Steps",
                "Shut down or isolate other shared billing machines",
                "একই নেটওয়ার্কের অন্যান্য কম্পিউটার পরীক্ষা ও আলাদা করুন",
                "Disconnect shared network folders and verify whether other counter PCs show renamed files or high disk activity.",
                "শেয়ার করা ফোল্ডার বন্ধ করুন এবং দোকানের অন্য পিসিতে অস্বাভাবিক ফাইল পরিবর্তন হয়েছে কি না দেখুন।",
            ),
            StepDef(
                "Account Protection",
                "Rotate business passwords from an uninfected device",
                "অন্য নিরাপদ ডিভাইস থেকে সব ব্যবসার পাসওয়ার্ড বদলান",
                "Assume credentials cached in browsers on the infected PC may be stolen; reset email, banking, and cloud passwords from a clean phone/laptop.",
                "আক্রান্ত পিসির ব্রাউজারে সেভ করা পাসওয়ার্ড চুরি হতে পারে; নিরাপদ ডিভাইস থেকে সব পাসওয়ার্ড পরিবর্তন করুন।",
            ),
            StepDef(
                "Evidence Preservation",
                "Photograph ransom note & keep encrypted samples",
                "মুক্তিপণের বার্তা ও আক্রান্ত ফাইলের ছবি/নমুনা রাখুন",
                "Do NOT format the drive immediately if you need forensic/legal help; photograph the ransom note and record exact file extensions.",
                "ফরেনসিক বা আইনি সহায়তার প্রয়োজনে সাথে সাথে ড্রাইভ ফরম্যাট করবেন না; স্ক্রিনের ছবি ও ফাইলের এক্সটেনশন লিখে রাখুন।",
            ),
            StepDef(
                "Recovery Guidance",
                "Rebuild OS clean and restore from verified offline backups",
                "অফলাইন ব্যাকআপ থেকে ডেটা পুনরুদ্ধার ও সিস্টেম রি-ইনস্টল করুন",
                "SafePulse AI cannot decrypt files or remove ransomware automatically. Engage a qualified IT technician to wipe/reinstall the OS and restore clean backups.",
                "SafePulse AI স্বয়ংক্রিয়ভাবে ফাইল ডিক্রিপ্ট বা ম্যালওয়্যার দূর করতে পারে না; দক্ষ IT বিশেষজ্ঞের সাহায্যে OS রি-ইনস্টল করে নিরাপদ ব্যাকআপ রিস্টোর করুন।",
            ),
            StepDef(
                "Reporting Recommendations",
                "Report to CERT-In and cybercrime.gov.in",
                "CERT-In এবং cybercrime.gov.in-এ রিপোর্ট করুন",
                "Report ransomware incidents to CERT-In (incident@cert-in.org.in) and check 'No More Ransom' project for known free decryptors.",
                "ঘটনাটি CERT-In ও cybercrime.gov.in-এ রিপোর্ট করুন এবং পরিচিত ডিক্রিপ্টরের জন্য 'No More Ransom' পোর্টাল দেখুন।",
            ),
        ],
    ),
    "sensitive_data_exposure": ScenarioDef(
        key="sensitive_data_exposure",
        title_en="Sensitive Customer or Business Data Exposed",
        title_bn="গ্রাহক বা ব্যবসার সংবেদনশীল তথ্য ফাঁস হয়েছে",
        severity="High",
        summary_en="Customer records, invoices, IDs, or private spreadsheets were accidentally emailed publicly, lost on a device, or leaked.",
        summary_bn="গ্রাহকের তথ্য, বিল, আইডি বা গুরুত্বপূর্ণ ফাইল ভুল করে বাইরে চলে গেছে বা ডিভাইস হারিয়ে গেছে।",
        steps=[
            StepDef(
                "Immediate Actions",
                "Revoke public link or lock lost device remotely",
                "পাবলিক শেয়ার লিঙ্ক বন্ধ করুন বা হারানো ডিভাইস লক করুন",
                "If shared via Google Drive/OneDrive link, set permissions to Restricted immediately. If a laptop/phone was lost, trigger remote lock/wipe.",
                "ক্লাউড ড্রাইভের লিঙ্ক ভুল করে পাবলিক হলে সাথে সাথে বন্ধ করুন; ডিভাইস হারালে রিমোট লক বা ওয়াইপ করুন।",
            ),
            StepDef(
                "Containment Steps",
                "Assess exactly what records and fields were exposed",
                "ঠিক কোন কোন তথ্য ফাঁস হয়েছে তা নির্ণয় করুন",
                "List whether names, phone numbers, medical/pharmacy bills, GST records, or payment details were included.",
                "ফাঁস হওয়া ফাইলে গ্রাহকের নাম, ফোন নম্বর, প্রেসক্রিপশন বা আর্থিক তথ্য ছিল কি না তা তালিকাভুক্ত করুন।",
            ),
            StepDef(
                "Account Protection",
                "Rotate API keys, shared passwords, and access tokens",
                "যুক্ত পাসওয়ার্ড ও অ্যাক্সেস কী পরিবর্তন করুন",
                "If spreadsheets or backups contained saved logins, GST portal credentials, or API keys, rotate every exposed credential immediately.",
                "ফাঁস হওয়া ফাইলে কোনো পাসওয়ার্ড বা API কী থাকলে সেগুলো সাথে সাথে পরিবর্তন করুন।",
            ),
            StepDef(
                "Evidence Preservation",
                "Preserve access logs and recipient details",
                "অ্যাক্সেস লগ ও প্রাপকের তথ্য সংরক্ষণ করুন",
                "Download drive access logs or email delivery receipts showing who viewed or received the exposed file.",
                "ফাইলটি কে দেখেছে বা পেয়েছে তার অ্যাক্সেস লগ বা ইমেইল রেকর্ড সংরক্ষণ করুন।",
            ),
            StepDef(
                "Recovery Guidance",
                "Notify affected individuals & tighten sharing controls",
                "ক্ষতিগ্রস্তদের সতর্ক করুন এবং ফাইল শেয়ারিং নীতি কঠোর করুন",
                "Inform affected customers/staff transparently if high-risk identity/financial data was exposed so they watch for follow-on scams.",
                "গুরুত্বপূর্ণ তথ্য ফাঁস হলে গ্রাহক বা কর্মীদের সতর্ক করুন যেন তারা সম্ভাব্য প্রতারণামূলক কল থেকে সাবধান থাকেন।",
            ),
            StepDef(
                "Reporting Recommendations",
                "Follow CERT-In reporting obligations if critical breach",
                "গুরুতর তথ্য ফাঁসের ক্ষেত্রে CERT-In-এ রিপোর্ট করুন",
                "Under India's CERT-In directions / DPDP expectations, document the timeline and report significant data breaches to CERT-In.",
                "গুরুতর ডেটা লঙ্ঘনের ক্ষেত্রে ঘটনার সময়সূচি নথিভুক্ত করে CERT-In-এ রিপোর্ট করুন।",
            ),
        ],
    ),
}


def list_scenarios(language: str = "en") -> List[Dict[str, Any]]:
    return [
        {
            "key": s.key,
            "title": s.title_bn if language == "bn" else s.title_en,
            "severity": s.severity,
            "summary": s.summary_bn if language == "bn" else s.summary_en,
            "steps_count": len(s.steps),
        }
        for s in INCIDENT_SCENARIOS.values()
    ]


def get_scenario_steps(scenario_key: str, language: str = "en") -> ScenarioDef:
    if scenario_key not in INCIDENT_SCENARIOS:
        raise ValueError(f"Unknown incident scenario '{scenario_key}'.")
    return INCIDENT_SCENARIOS[scenario_key]

