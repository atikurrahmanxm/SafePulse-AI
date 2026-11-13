"""Governance controls, subscription plans, and future integration catalog for SafePulse AI."""

from __future__ import annotations

from typing import Any, Dict, List


SUBSCRIPTION_PLANS: Dict[str, Dict[str, Any]] = {
    "free": {
        "key": "free",
        "name": "Free SME Starter",
        "monthly_scan_quota": 50,
        "max_workspaces": 2,
        "features": [
            "AI Phishing & URL Scanner (50 scans/month)",
            "10-Domain Business Health Assessment",
            "Guided 6-Phase Incident Playbooks",
            "PDF Report Exports",
        ],
    },
    "pro_sme": {
        "key": "pro_sme",
        "name": "Pro SME Shield (Architecture Ready)",
        "monthly_scan_quota": 500,
        "max_workspaces": 10,
        "features": [
            "500 Phishing & URL scans/month",
            "Multi-Branch Workspace Management",
            "Team MFA & Awareness Tracking",
            "Monthly Executive PDF Reports",
        ],
    },
    "enterprise_ready": {
        "key": "enterprise_ready",
        "name": "Multi-Tenant Enterprise (Architecture Ready)",
        "monthly_scan_quota": 5000,
        "max_workspaces": 50,
        "features": [
            "5,000 scans/month + API Access",
            "Workspace & M365 Connector Readiness",
            "Custom Webhook Alerting",
            "Dedicated Audit Trail Retention",
        ],
    },
}


DEFAULT_CONTROLS: List[Dict[str, str]] = [
    # Backup Monitoring Checklist
    {
        "category": "backup",
        "control_key": "backup_321_copy",
        "title_en": "Maintain an offline / air-gapped weekly billing & GST backup",
        "title_bn": "প্রতি সপ্তাহে বিলিং ও GST ডেটার একটি অফলাইন ব্যাকআপ রাখুন",
        "guidance_en": "Copy Tally, pharmacy POS, and invoice databases to an external drive disconnected after backup so ransomware cannot encrypt it.",
        "guidance_bn": "Tally বা বিলিং ডেটা একটি আলাদা হার্ড ড্রাইভে কপি করে সেটি পিসি থেকে খুলে রাখুন যাতে র‍্যানসমওয়্যার ক্ষতি করতে না পারে।",
        "priority": "Critical",
    },
    {
        "category": "backup",
        "control_key": "backup_restore_test",
        "title_en": "Verify backup restore test once every month",
        "title_bn": "প্রতি মাসে একবার ব্যাকআপ রিস্টোর পরীক্ষা করুন",
        "guidance_en": "A backup that has never been tested may fail during an emergency. Open at least 2 backed-up files on another computer monthly.",
        "guidance_bn": "ব্যাকআপ ঠিকমতো কাজ করছে কিনা তা মাসে একবার অন্য কম্পিউটারে খুলে যাচাই করুন।",
        "priority": "High",
    },
    {
        "category": "backup",
        "control_key": "backup_cloud_sync",
        "title_en": "Protect cloud backup account with MFA and version history",
        "title_bn": "ক্লাউড ব্যাকআপ অ্যাকাউন্টে 2FA এবং ভার্সন হিস্ট্রি চালু রাখুন",
        "guidance_en": "Ensure Google Drive / OneDrive backup folders require 2FA and keep 30-day file version history enabled.",
        "guidance_bn": "Google Drive বা OneDrive ব্যাকআপে ২-ধাপ যাচাইকরণ (MFA) চালু রাখুন।",
        "priority": "Medium",
    },
    # Software Update Tracking Checklist
    {
        "category": "updates",
        "control_key": "updates_os_monthly",
        "title_en": "Install Windows / macOS security patches across all billing PCs",
        "title_bn": "সব বিলিং কম্পিউটারে Windows / OS সিকিউরিটি আপডেট ইনস্টল করুন",
        "guidance_en": "Confirm every shop counter PC and owner laptop has automatic OS security updates applied within 7 days of release.",
        "guidance_bn": "দোকানের সব কম্পিউটারে স্বয়ংক্রিয় নিরাপত্তা আপডেট চালু আছে কিনা মাসে একবার যাচাই করুন।",
        "priority": "High",
    },
    {
        "category": "updates",
        "control_key": "updates_browser_restart",
        "title_en": "Keep Chrome / Edge & PDF readers updated on office systems",
        "title_bn": "Chrome / Edge ব্রাউজার ও PDF রিডার নিয়মিত আপডেট রাখুন",
        "guidance_en": "Restart browsers weekly to apply critical zero-day web security fixes before opening banking or GST portals.",
        "guidance_bn": "ব্যাংকিং বা GST পোর্টাল ব্যবহারের আগে ব্রাউজার আপডেট ও রিস্টার্ট করুন।",
        "priority": "Medium",
    },
    {
        "category": "updates",
        "control_key": "updates_router_firmware",
        "title_en": "Verify shop Wi-Fi router firmware & change default admin password",
        "title_bn": "দোকানের Wi-Fi রাউটারের ডিফল্ট পাসওয়ার্ড পরিবর্তন ও ফার্মওয়্যার চেক করুন",
        "guidance_en": "Disable remote router admin access and keep separate guest Wi-Fi for customers away from POS/billing devices.",
        "guidance_bn": "গ্রাহকদের জন্য আলাদা গেস্ট Wi-Fi রাখুন এবং রাউটারের অ্যাডমিন পাসওয়ার্ড পরিবর্তন করুন।",
        "priority": "High",
    },
    # Business Security Policies
    {
        "category": "policy",
        "control_key": "policy_upi_payment_verify",
        "title_en": "Two-person phone verification policy for bank/UPI detail changes",
        "title_bn": "ব্যাংক বা UPI পরিবর্তনের আগে কল করে যাচাই করার নীতি",
        "guidance_en": "Require staff to call suppliers on a previously saved number before transferring Rs 5,000+ or updating vendor bank accounts.",
        "guidance_bn": "নতুন ব্যাংক অ্যাকাউন্ট বা বড় অঙ্কের পেমেন্টের আগে পূর্বপরিচিত নম্বরে ফোন করে নিশ্চিত হওয়ার নিয়ম চালু করুন।",
        "priority": "Critical",
    },
    {
        "category": "policy",
        "control_key": "policy_no_otp_sharing",
        "title_en": "Zero OTP / AnyDesk / Screen-Share staff policy",
        "title_bn": "কর্মীদের জন্য OTP ও AnyDesk স্ক্রিন-শেয়ার নিষিদ্ধ নীতি",
        "guidance_en": "Post a visible counter notice reminding staff never to share OTP/UPI PIN or install remote access apps on unsolicited support calls.",
        "guidance_bn": "কাউন্টারে নোটিশ রাখুন: অচেনা কলের নির্দেশে কখনোই OTP বা AnyDesk শেয়ার করা যাবে না।",
        "priority": "Critical",
    },
    {
        "category": "policy",
        "control_key": "policy_least_privilege",
        "title_en": "Separate staff POS accounts from owner administrator logins",
        "title_bn": "কর্মীদের POS অ্যাকাউন্ট ও মালিকের অ্যাডমিন অ্যাকাউন্ট আলাদা রাখা",
        "guidance_en": "Remove shared admin passwords and revoke former employee access on the same day they leave.",
        "guidance_bn": "কর্মীদের আলাদা ইউজার অ্যাকাউন্ট দিন এবং কেউ কাজ ছেড়ে দিলে সেদিনই অ্যাক্সেস বন্ধ করুন।",
        "priority": "High",
    },
    # Security Improvement Roadmap
    {
        "category": "roadmap",
        "control_key": "roadmap_mfa_100",
        "title_en": "Achieve 100% 2FA/MFA coverage on business email, banking & accounting",
        "title_bn": "ব্যবসায়িক ইমেইল ও ব্যাংকিংয়ে ১০০% 2FA/MFA চালু করা",
        "guidance_en": "Track every staff email/portal account in the Team & MFA Directory until 100% adoption is reached.",
        "guidance_bn": "টিম ডিরেক্টরি ব্যবহার করে সব কর্মীর অ্যাকাউন্টে 2FA নিশ্চিত করুন।",
        "priority": "Critical",
    },
    {
        "category": "roadmap",
        "control_key": "roadmap_email_spf_dmarc",
        "title_en": "Publish SPF & DMARC records for primary business email domain",
        "title_bn": "ব্যবসায়িক ইমেইল ডোমেইনের জন্য SPF ও DMARC রেকর্ড যোগ করা",
        "guidance_en": "Prevents attackers from spoofing your business domain to scam your customers and partners.",
        "guidance_bn": "গ্রাহকদের কাছে আপনার কোম্পানির নামে ভুয়া ইমেইল যাওয়া বন্ধ করতে DNS-এ SPF/DMARC সেট করুন।",
        "priority": "High",
    },
    {
        "category": "roadmap",
        "control_key": "roadmap_quarterly_drill",
        "title_en": "Run quarterly 15-minute staff phishing drill & incident table-top",
        "title_bn": "প্রতি ৩ মাসে ১৫ মিনিটের ফিশিং ও ইনসিডেন্ট ড্রিল পরিচালনা",
        "guidance_en": "Use SafePulse AI Training Simulations and Helpline 1930 walkthrough with counter and billing teams.",
        "guidance_bn": "প্রতি তিন মাসে কর্মীদের নিয়ে SafePulse AI প্রশিক্ষণ ও ১৯৩০ হেল্পলাইন রিহার্সাল করুন।",
        "priority": "Medium",
    },
]


INTEGRATION_CATALOG: List[Dict[str, Any]] = [
    {
        "provider_key": "google_safe_browsing",
        "name": "Google Safe Browsing Threat Intel",
        "category": "Threat Intelligence API",
        "description": "Augments local lexical & DNS URL scoring with Google Safe Browsing reputation lookups when GOOGLE_SAFE_BROWSING_API_KEY is configured on the server.",
        "config_hint": "Managed via server environment variable GOOGLE_SAFE_BROWSING_API_KEY.",
        "supports_live_env": True,
    },
    {
        "provider_key": "email_imap_monitor",
        "name": "Email Security Monitoring (IMAP / Forwarding)",
        "category": "Email Security",
        "description": "Integration-ready connector architecture for forwarding suspicious customer/vendor emails into SafePulse AI triage queues (requires OAuth/IMAP gateway setup in production).",
        "config_hint": "Target triage mailbox (e.g., security-triage@yourdomain.in)",
        "supports_live_env": False,
    },
    {
        "provider_key": "google_workspace",
        "name": "Google Workspace Directory & MFA Sync",
        "category": "Identity & Workspace",
        "description": "Integration-ready adapter to sync staff roster and 2-Step Verification enrollment status via Google Workspace Admin SDK OAuth.",
        "config_hint": "Workspace domain (e.g., yourbusiness.in)",
        "supports_live_env": False,
    },
    {
        "provider_key": "microsoft_365",
        "name": "Microsoft 365 Defender & Entra ID",
        "category": "Identity & Workspace",
        "description": "Integration-ready adapter for M365 tenant MFA posture and Exchange phishing quarantine alerts via Microsoft Graph API.",
        "config_hint": "Tenant domain (e.g., yourbusiness.onmicrosoft.com)",
        "supports_live_env": False,
    },
    {
        "provider_key": "webhook_notifications",
        "name": "Business Alert Notifications (Webhook / Slack / WhatsApp)",
        "category": "Alerting & Notifications",
        "description": "Integration-ready alert destination for Critical Risk phishing/URL findings and newly opened high-severity incidents.",
        "config_hint": "Destination channel label or HTTPS webhook path (secret stored server-side)",
        "supports_live_env": False,
    },
    {
        "provider_key": "cloud_backup_monitor",
        "name": "Cloud Backup Status Connector",
        "category": "Resilience & Backup",
        "description": "Architecture hook for receiving backup completion heartbeats from Tally/cloud backup agents. Until connected, verify backups manually in Governance Controls.",
        "config_hint": "Backup job identifier or vault name",
        "supports_live_env": False,
    },
]

