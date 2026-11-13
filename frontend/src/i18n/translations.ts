export type Language = "en" | "bn";

export const translations = {
  en: {
    brand: "SafePulse AI",
    tagline: "Smart Cybersecurity. Simple Protection. Safer Businesses.",
    nav: {
      overview: "Overview",
      phishing: "Phishing Detector",
      urlScanner: "URL Security Scanner",
      breachMonitor: "Data Breach Monitor",
      assessment: "Business Security Assessment",
      governance: "Governance & Team Posture",
      incidents: "Incident Response Center",
      awareness: "Employee Awareness",
      history: "Scan History",
      reports: "Reports Center",
      settings: "Settings",
      docs: "Help & Documentation",
      logout: "Sign Out",
    },
    topbar: {
      searchPlaceholder: "Quick jump to tool or page...",
      demoBadge: "Demo Mode",
      notifications: "Security Alerts",
      noAlerts: "No active high-risk alerts right now.",
      languageLabel: "Language",
    },
    landing: {
      heroHeadline: "Your Business Deserves Better Cyber Protection.",
      heroSub:
        "Detect phishing and scam messages, inspect suspicious URLs safely, measure your business security posture, and follow step-by-step incident response — built for shops, pharmacies, startups, and SMEs.",
      getStarted: "Get Started",
      exploreFeatures: "Explore Features",
      tryDemo: "Launch Interactive Demo",
    },
    dashboard: {
      securityScore: "Business Security Score",
      totalAnalyses: "Total Threat Analyses",
      highRiskFindings: "High-Risk Findings",
      completedAssessments: "Completed Assessments",
      quickActions: "Quick Actions",
      analyzeMessage: "Analyze Suspicious Message",
      scanUrl: "Scan Website URL",
      startAssessment: "Start Security Assessment",
      reportIncident: "Report a Cyber Incident",
      emptyTitle: "Welcome to SafePulse AI",
      emptyDesc:
        "Your workspace is ready. Run your first phishing check, scan a suspicious URL, or complete the 10-point Business Security Health Check to populate live telemetry.",
      monthlyReport: "Download Monthly Report (PDF)",
      improvementTitle: "Security Improvement Progress",
      vectorBreakdown: "Threat Vector Distribution",
      planUsage: "Monthly Scan Quota",
    },
    governance: {
      title: "Security Governance, Team & Roadmap",
      subtitle:
        "Track staff MFA adoption, software updates, offline backups, security policies, and prioritized hardening steps without exaggerated monitoring claims.",
      manualNotice:
        "Self-Attested Governance Tracking: Status reflects controls logged by your business owner or IT lead. SafePulse AI does not run background agents on employee endpoints.",
    },
    phishing: {
      title: "AI Phishing & Scam Detector",
      subtitle:
        "Analyze emails, SMS, and WhatsApp messages using TF-IDF + Logistic Regression and transparent social-engineering rules.",
      channelLabel: "Message Channel",
      senderLabel: "Sender Email or Phone (Optional)",
      messageLabel: "Paste Suspicious Message",
      analyzeBtn: "Analyze Message",
      analyzing: "Analyzing Threat Signals...",
      samplesLabel: "Load Demo Sample Scenario",
      highlightedTitle: "Suspicious Phrases Highlighted",
      reasonsTitle: "Why This Was Flagged",
      actionsTitle: "Recommended Security Actions",
      downloadPdf: "Download PDF Report",
      mlMetricsTab: "ML Model & Held-Out Evaluation",
      riskBandNote:
        "Application risk bands: 0–24 Low, 25–49 Moderate, 50–74 High, 75–100 Critical (not universal standards).",
    },
    url: {
      title: "Smart URL Security Analyzer",
      subtitle:
        "Inspect website links for typosquatting, obfuscation, unsafe schemes, and DNS email authentication (SPF/DMARC) without visiting the page.",
      inputLabel: "Website or Link URL",
      scanBtn: "Scan URL Safely",
      scanning: "Inspecting URL & DNS...",
      httpsNote:
        "Important: HTTPS (padlock) only encrypts transit traffic — phishing sites also use HTTPS. Low risk means no local red flags, not verified safe.",
      ssrfNote:
        "SSRF Protection Active: Localhost, private IPs, and target content execution are strictly blocked.",
    },
    breaches: {
      title: "Data Breach & Credential Exposure Monitor",
      subtitle:
        "Detect if your business email, cashier logins, or supplier credentials were leaked in known vendor database breaches.",
      inputLabel: "Business Email Address or Domain",
      inputPlaceholder: "e.g., owner@pharmacy.in, billing@store.com",
      scanBtn: "Check Breach Exposure",
      scanning: "Searching Breach Repositories...",
      demoBtn: "Load Demo Exposure Sample",
      detectedTitle: "Exposed Incidents Identified",
      noBreachesTitle: "All Clear — No Public Exposures Detected",
      dataClassesTitle: "Compromised Data Categories",
      remediationTitle: "Immediate Containment Actions",
      downloadPdf: "Download Breach Assessment PDF",
      disclaimer:
        "SafePulse AI inspects offline threat intelligence benchmark logs. It does not store, request, or expose plaintext passwords.",
    },
    assessment: {
      title: "Business Security Health Check",
      subtitle:
        "10-domain small business security assessment aligned with practical CERT-In MSME recommendations.",
      submitBtn: "Calculate & Save Security Score",
      updateBtn: "Update Assessment",
      weakAreas: "Weak Areas",
      criticalGaps: "Critical Gaps",
      actionPlan: "Prioritized Action Plan",
      yes: "Yes (Fully Implemented)",
      partial: "Partial",
      no: "No (Not Yet)",
    },
    incidents: {
      title: "Cyber Incident Response Center",
      subtitle:
        "Step-by-step containment, account protection, evidence preservation, and reporting checklists written in clear language.",
      startBtn: "Open Incident Playbook",
      disclaimer:
        "Guidance Only: SafePulse AI guides your team through containment and reporting. It cannot independently remove malware, freeze bank transfers, or recover hacked accounts.",
    },
    awareness: {
      title: "Employee Cyber Awareness",
      subtitle:
        "Practical security lessons, clearly labeled training simulations, and interactive quizzes for shop and office teams.",
      simBadge: "TRAINING SIMULATION — SAFE EDUCATIONAL EXAMPLE",
    },
    history: {
      title: "Scan History & Audit Trail",
      subtitle:
        "Review past phishing scans, URL inspections, assessments, incident playbooks, and audit logs.",
      activityTab: "Activity & Reports",
      auditTab: "Audit Logs",
    },
    settings: {
      title: "Business & Security Settings",
      subtitle:
        "Manage your business workspace metadata, bilingual interface preference, and platform security posture.",
      profileCard: "Business Profile",
      saveBtn: "Save Changes",
      savingBtn: "Saving...",
      safeguardsCard: "Active Platform Safeguards",
    },
    docs: {
      title: "Help, Documentation & Hackathon Demo Guide",
      subtitle:
        "AdtU Innovation Mela 2026 — Complete operational guide, emergency contacts, and demonstration walkthrough.",
    },
  },
  bn: {
    brand: "SafePulse AI",
    tagline: "স্মার্ট সাইবার নিরাপত্তা। সহজ সুরক্ষা। নিরাপদ ব্যবসা।",
    nav: {
      overview: "ওভারভিউ (Overview)",
      phishing: "ফিশিং ও স্ক্যাম ডিটেক্টর",
      urlScanner: "URL নিরাপত্তা স্ক্যানার",
      breachMonitor: "ডাটা ব্রিচ ও ফাঁস মনিটর",
      assessment: "ব্যবসায়িক নিরাপত্তা মূল্যায়ন",
      governance: "টিম ও নিরাপত্তা পরিচালনা",
      incidents: "ইনসিডেন্ট রেসপন্স সেন্টার",
      awareness: "কর্মী সচেতনতা ও প্রশিক্ষণ",
      history: "স্ক্যান ইতিহাস (History)",
      reports: "সহজ রিপোর্ট সেন্টার (PDF)",
      settings: "সেটিংস",
      docs: "সহায়তা ও ডকুমেন্টেশন",
      logout: "লগ-আউট",
    },
    topbar: {
      searchPlaceholder: "দ্রুত পেজ বা টুল খুঁজুন...",
      demoBadge: "ডেমো মোড (Demo)",
      notifications: "নিরাপত্তা সতর্কতা",
      noAlerts: "এই মুহূর্তে কোনো উচ্চ-ঝুঁকির সতর্কতা নেই।",
      languageLabel: "ভাষা",
    },
    landing: {
      heroHeadline: "আপনার ব্যবসার জন্য আরও শক্তিশালী সাইবার সুরক্ষা।",
      heroSub:
        "ফিশিং বার্তা শনাক্ত করুন, সন্দেহজনক লিঙ্ক নিরাপদে পরীক্ষা করুন, ব্যবসার নিরাপত্তা স্কোর মাপুন এবং জরুরি সাইবার ঘটনায় ধাপে ধাপে করণীয় জানুন — ছোট ব্যবসা, ফার্মেসি ও স্টার্টআপের জন্য তৈরি।",
      getStarted: "শুরু করুন",
      exploreFeatures: "ফিচার দেখুন",
      tryDemo: "ইন্টারেক্টিভ ডেমো দেখুন",
    },
    dashboard: {
      securityScore: "ব্যবসায়িক নিরাপত্তা স্কোর",
      totalAnalyses: "মোট থ্রেট বিশ্লেষণ",
      highRiskFindings: "উচ্চ-ঝুঁকির সতর্কতা",
      completedAssessments: "সম্পন্ন মূল্যায়ন",
      quickActions: "দ্রুত পদক্ষেপ (Quick Actions)",
      analyzeMessage: "সন্দেহজনক বার্তা পরীক্ষা করুন",
      scanUrl: "ওয়েবসাইট URL স্ক্যান করুন",
      startAssessment: "নিরাপত্তা মূল্যায়ন শুরু করুন",
      reportIncident: "সাইবার ঘটনা রিপোর্ট করুন",
      emptyTitle: "SafePulse AI-তে স্বাগতম",
      emptyDesc:
        "আপনার ওয়ার্কস্পেস প্রস্তুত। লাইভ নিরাপত্তা তথ্য দেখতে প্রথম ফিশিং পরীক্ষা, URL স্ক্যান বা বিজনেস সিকিউরিটি হেলথ চেক সম্পন্ন করুন।",
      monthlyReport: "মাসিক নিরাপত্তা রিপোর্ট (PDF)",
      improvementTitle: "নিরাপত্তা উন্নতির অগ্রগতি",
      vectorBreakdown: "থ্রেট মাধ্যম বিশ্লেষণ",
      planUsage: "মাসিক স্ক্যান ব্যবহার",
    },
    governance: {
      title: "নিরাপত্তা পরিচালনা, টিম ও রোডম্যাপ",
      subtitle:
        "কর্মীদের MFA ব্যবহার, সফটওয়্যার আপডেট, ব্যাকআপ এবং সিকিউরিটি পলিসির অগ্রগতি সহজে পরিচালনা করুন।",
      manualNotice:
        "ম্যানুয়াল যাচাইকরণ তথ্য: এখানে প্রদর্শিত তথ্য আপনার ব্যবসা বা আইটি দায়িত্বপ্রাপ্ত ব্যক্তির আপডেটের ওপর ভিত্তি করে সংরক্ষিত হয়।",
    },
    phishing: {
      title: "AI ফিশিং ও স্ক্যাম ডিটেক্টর",
      subtitle:
        "TF-IDF + Logistic Regression এবং স্বচ্ছ নিরাপত্তা নিয়মের মাধ্যমে ইমেইল, SMS এবং হোয়াটসঅ্যাপ বার্তা বিশ্লেষণ করুন।",
      channelLabel: "বার্তার মাধ্যম (Channel)",
      senderLabel: "প্রেরকের ইমেইল বা ফোন (ঐচ্ছিক)",
      messageLabel: "সন্দেহজনক বার্তাটি এখানে পেস্ট করুন",
      analyzeBtn: "বার্তা বিশ্লেষণ করুন",
      analyzing: "ঝুঁকি বিশ্লেষণ চলছে...",
      samplesLabel: "নমুনা ডেমো বার্তা লোড করুন",
      highlightedTitle: "চিহ্নিত সন্দেহজনক অংশ",
      reasonsTitle: "কেন ঝুঁকিপূর্ণ হিসেবে চিহ্নিত হয়েছে",
      actionsTitle: "করণীয় নিরাপত্তা পদক্ষেপ",
      downloadPdf: "PDF রিপোর্ট ডাউনলোড",
      mlMetricsTab: "ML মডেল ও মূল্যায়ন ফলাফল",
      riskBandNote:
        "অ্যাপ্লিকেশন ঝুঁকির স্তর: ০–২৪ কম, ২৫–৪৯ মাঝারি, ৫০–৭৪ উচ্চ, ৭৫–১০০ মারাত্মক (সর্বজনীন মানদণ্ড নয়)।",
    },
    url: {
      title: "স্মার্ট URL নিরাপত্তা স্ক্যানার",
      subtitle:
        "ওয়েবসাইটটি ওপেন না করেই নকল ডোমেইন, সন্দেহজনক ক্যারেক্টার এবং DNS (SPF/DMARC) রেকর্ড পরীক্ষা করুন।",
      inputLabel: "ওয়েবসাইট বা লিঙ্ক URL",
      scanBtn: "নিরাপদে URL স্ক্যান করুন",
      scanning: "URL ও DNS যাচাই হচ্ছে...",
      httpsNote:
        "গুরুত্বপূর্ণ: HTTPS (তালা চিহ্ন) মানেই সাইটটি নিরাপদ নয় — ফিশিং সাইটেও HTTPS থাকে। কম ঝুঁকি মানে স্থানীয় কোনো লাল সংকেত পাওয়া যায়নি, কিন্তু সম্পূর্ণ নিরাপদের গ্যারান্টি নয়।",
      ssrfNote:
        "SSRF সুরক্ষা সক্রিয়: লোকালহোস্ট, প্রাইভেট IP এবং টার্গেট সাইট ওপেন করা সম্পূর্ণ ব্লক করা হয়েছে।",
    },
    breaches: {
      title: "ডাটা ব্রিচ ও ফাঁস পর্যবেক্ষণ (Data Breach Monitor)",
      subtitle:
        "আপনার দোকানের ইমেইল, ক্যাশিয়ার লগইন বা পাসওয়ার্ড কোনো পাবলিক ডাটা ফাঁসে লিক হয়েছে কি না যাচাই করুন।",
      inputLabel: "ব্যবসায়িক ইমেইল বা ডোমেইন নাম",
      inputPlaceholder: "যেমন: owner@pharmacy.in, billing@store.com",
      scanBtn: "ফাঁসের ঝুঁকি পরীক্ষা করুন",
      scanning: "ডাটাবেজ ও ডাম্প অনুসন্ধান চলছে...",
      demoBtn: "ডেমো নমুনা লোড করুন",
      detectedTitle: "শনাক্ত হওয়া ডাটা ফাঁসের ঘটনা",
      noBreachesTitle: "সব নিরাপদ — কোনো ফাঁসের তথ্য মেলেনি",
      dataClassesTitle: "ফাঁস হওয়া তথ্যের ধরন",
      remediationTitle: "অবিলম্বে করণীয় পদক্ষেপ",
      downloadPdf: "ডাটা ব্রিচ মূল্যায়ন PDF",
      disclaimer:
        "SafePulse AI অফলাইন নিরাপত্তা ডাটাবেজের মাধ্যমে যাচাই করে। এটি কোনো আসল পাসওয়ার্ড সংরক্ষণ বা প্রকাশ করে না।",
    },
    assessment: {
      title: "বিজনেস সিকিউরিটি হেলথ চেক",
      subtitle:
        "CERT-In MSME নির্দেশিকার সাথে সামঞ্জস্যপূর্ণ ১০টি প্রধান ক্ষেত্রের নিরাপত্তা মূল্যায়ন।",
      submitBtn: "নিরাপত্তা স্কোর হিসাব ও সংরক্ষণ করুন",
      updateBtn: "মূল্যায়ন আপডেট করুন",
      weakAreas: "দুর্বল ক্ষেত্রসমূহ",
      criticalGaps: "জরুরি ঘাটতি (Critical Gaps)",
      actionPlan: "অগ্রাধিকারভিত্তিক কর্মপরিকল্পনা",
      yes: "হ্যাঁ (সম্পূর্ণ চালু)",
      partial: "আংশিক",
      no: "না (চালু নেই)",
    },
    incidents: {
      title: "সাইবার ইনসিডেন্ট রেসপন্স সেন্টার",
      subtitle:
        "সহজ ভাষায় তাৎক্ষণিক পদক্ষেপ, অ্যাকাউন্ট সুরক্ষা, প্রমাণ সংরক্ষণ ও রিপোর্টিং চেকলিস্ট।",
      startBtn: "ইনসিডেন্ট প্লেবুক শুরু করুন",
      disclaimer:
        "শুধুমাত্র নির্দেশনা: SafePulse AI আপনাকে করণীয় ধাপগুলো দেখায়; এটি নিজে থেকে ম্যালওয়্যার সরাতে বা হ্যাক হওয়া অ্যাকাউন্ট উদ্ধার করতে পারে না।",
    },
    awareness: {
      title: "কর্মী সাইবার সচেতনতা ও প্রশিক্ষণ",
      subtitle:
        "দোকান ও অফিস কর্মীদের জন্য বাস্তবভিত্তিক পাঠ, প্রশিক্ষণ সিমুলেশন এবং ইন্টারেক্টিভ কুইজ।",
      simBadge: "প্রশিক্ষণ সিমুলেশন — নিরাপদ শিক্ষামূলক উদাহরণ",
    },
    history: {
      title: "স্ক্যান ইতিহাস ও অডিট লগ",
      subtitle:
        "পূর্ববর্তী ফিশিং স্ক্যান, URL পরীক্ষা, নিরাপত্তা মূল্যায়ন, ইনসিডেন্ট প্লেবুক এবং অডিট লগ দেখুন।",
      activityTab: "কার্যক্রম ও রিপোর্ট",
      auditTab: "অডিট লগ",
    },
    settings: {
      title: "ব্যবসায়িক ও নিরাপত্তা সেটিংস",
      subtitle:
        "আপনার ব্যবসার তথ্য, বাংলা/ইংরেজি ভাষা এবং প্ল্যাটফর্ম নিরাপত্তা ব্যবস্থা পরিচালনা করুন।",
      profileCard: "ব্যবসায়িক প্রোফাইল",
      saveBtn: "পরিবর্তন সংরক্ষণ করুন",
      savingBtn: "সংরক্ষণ হচ্ছে...",
      safeguardsCard: "সক্রিয় প্ল্যাটফর্ম সুরক্ষা",
    },
    docs: {
      title: "সহায়তা, ডকুমেন্টেশন ও ডেমো গাইড",
      subtitle:
        "AdtU Innovation Mela 2026 — সম্পূর্ণ ব্যবহার নির্দেশিকা, জরুরি হেল্পলাইন এবং ডেমো ধাপসমূহ।",
    },
  },
} as const;

