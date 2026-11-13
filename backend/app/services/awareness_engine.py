"""Employee Cyber Awareness training modules, clearly labeled phishing simulations, and quizzes."""

from __future__ import annotations

from typing import Any, Dict, List


TRAINING_LESSONS: List[Dict[str, Any]] = [
    {
        "id": "phishing-red-flags",
        "topic": "Phishing Recognition",
        "title_en": "Spotting Phishing Emails, SMS & WhatsApp Lures",
        "title_bn": "ফিশিং ইমেইল, SMS ও হোয়াটসঅ্যাপ প্রতারণা চেনার উপায়",
        "duration_min": 5,
        "summary_en": "Learn the 4 classic signs attackers use against small businesses: false urgency, lookalike domains, credential/OTP demands, and unexpected payment changes.",
        "summary_bn": "ছোট ব্যবসায় প্রতারণার ৪টি প্রধান লক্ষণ: কৃত্রিম তাড়াহুড়ো, নকল ডোমেইন, OTP/পাসওয়ার্ড চাওয়া এবং হঠাৎ ব্যাংক তথ্য পরিবর্তন।",
        "tips_en": [
            "Check the domain AFTER '@' or before the first '/' — 'hdfc-kyc.xyz' is NOT 'hdfcbank.com'.",
            "Receiving money via UPI NEVER requires entering your UPI PIN or scanning a QR code.",
            "Treat any message demanding action 'within 2 hours' or threatening account suspension as suspicious until verified by phone.",
        ],
        "tips_bn": [
            "'@' চিহ্নের পরের ডোমেইন ভালো করে দেখুন — 'hdfc-kyc.xyz' কখনোই 'hdfcbank.com' নয়।",
            "UPI-তে টাকা পাওয়ার জন্য কখনোই UPI PIN দিতে হয় না বা QR কোড স্ক্যান করতে হয় না।",
            "'২ ঘণ্টার মধ্যে অ্যাকাউন্ট বন্ধ হবে' ধরনের জরুরি হুমকি পেলে অফিসিয়াল নম্বরে ফোন করে যাচাই করুন।",
        ],
    },
    {
        "id": "password-mfa-hygiene",
        "topic": "Password & MFA Safety",
        "title_en": "Strong Passphrases & Multi-Factor Authentication",
        "title_bn": "শক্তিশালী পাসওয়ার্ড ও মাল্টি-ফ্যাক্টর নিরাপত্তা (MFA)",
        "duration_min": 4,
        "summary_en": "Why reusing one shop password across Gmail, billing, and banking creates a single point of failure, and how MFA stops 99% of password theft.",
        "summary_bn": "একই পাসওয়ার্ড একাধিক জায়গায় ব্যবহারের ঝুঁকি এবং কীভাবে MFA পাসওয়ার্ড চুরি হলেও অ্যাকাউন্ট বাঁচায়।",
        "tips_en": [
            "Use unique 12+ character passphrases (e.g., 3-4 unrelated words + numbers) for each business login.",
            "Turn on Authenticator-app MFA (or hardware key) for business email, banking, GST, and social media.",
            "Never share your login password on sticky notes at the billing counter or in staff WhatsApp groups.",
        ],
        "tips_bn": [
            "প্রতিটি ব্যবসায়িক অ্যাকাউন্টে কমপক্ষে ১২ অক্ষরের আলাদা পাসওয়ার্ড ব্যবহার করুন।",
            "ইমেইল, ব্যাংকিং, GST ও সোশ্যাল মিডিয়ায় অবশ্যই MFA / ২-স্তরের নিরাপত্তা চালু রাখুন।",
            "ক্যাশ কাউন্টারে কাগজে লিখে বা হোয়াটসঅ্যাপ গ্রুপে পাসওয়ার্ড শেয়ার করবেন না।",
        ],
    },
    {
        "id": "safe-browsing-devices",
        "topic": "Safe Browsing & Devices",
        "title_en": "Safe Browsing, Remote-Access Scams & APK Safety",
        "title_bn": "নিরাপদ ব্রাউজিং, AnyDesk প্রতারণা ও APK সতর্কতা",
        "duration_min": 5,
        "summary_en": "Understand why HTTPS alone does not prove a website is legitimate, and why unknown APK files or remote-support tools endanger business funds.",
        "summary_bn": "কেন শুধু HTTPS দেখেই ওয়েবসাইট নিরাপদ ভাবা উচিত নয় এবং অজানা APK বা স্ক্রিন-শেয়ারিং অ্যাপের বিপদ।",
        "tips_en": [
            "The browser padlock (HTTPS) only encrypts traffic — scam sites also get free HTTPS certificates.",
            "Never install '.apk' files received on WhatsApp or grant AnyDesk/TeamViewer access to unknown callers.",
            "Keep billing PCs updated and lock screens automatically whenever stepping away from the counter.",
        ],
        "tips_bn": [
            "ব্রাউজারে তালা চিহ্ন (HTTPS) থাকা মানেই সাইটটি আসল নয় — ভুয়া সাইটেও HTTPS থাকে।",
            "হোয়াটসঅ্যাপে আসা অজানা '.apk' ফাইল ইনস্টল করবেন না এবং অচেনা ব্যক্তিকে AnyDesk/TeamViewer অ্যাক্সেস দেবেন না।",
            "বিলিং কম্পিউটার নিয়মিত আপডেট রাখুন এবং কাউন্টার ছাড়ার আগে স্ক্রিন লক করুন।",
        ],
    },
    {
        "id": "social-engineering",
        "topic": "Social Engineering",
        "title_en": "Preventing Boss Impersonation & Fake Vendor Invoices",
        "title_bn": "মালিকের ছদ্মবেশ ও ভুয়া সাপ্লায়ার ইনভয়েস প্রতিরোধ",
        "duration_min": 4,
        "summary_en": "Protect your accounts staff from WhatsApp 'owner urgent transfer' tricks and altered supplier bank details.",
        "summary_bn": "হোয়াটসঅ্যাপে মালিকের নামে জরুরি টাকার অনুরোধ এবং ভুয়া ব্যাংক অ্যাকাউন্ট পরিবর্তনের প্রতারণা থেকে সাবধানতা।",
        "tips_en": [
            "Always follow a two-person or voice-callback rule before transferring money to any 'new' vendor bank account.",
            "Be skeptical of messages from an unknown number claiming to be your boss saying 'I am in a meeting, don't call me'.",
            "Verify customer UPI payment confirmations inside your official merchant app — never trust screenshots alone.",
        ],
        "tips_bn": [
            "কোনো সাপ্লায়ার ব্যাংক অ্যাকাউন্ট পরিবর্তনের কথা বললে আগে থেকে জানা নম্বরে কল করে নিশ্চিত হোন।",
            "'আমি মিটিংয়ে আছি, কল করো না, দ্রুত টাকা পাঠাও' — এমন অচেনা হোয়াটসঅ্যাপ নম্বরের অনুরোধে টাকা পাঠাবেন না।",
            "গ্রাহকের পেমেন্ট শুধু স্ক্রিনশট দেখে নয়, নিজের অফিসিয়াল মার্চেন্ট অ্যাপে ঢুকে নিশ্চিত হোন।",
        ],
    },
]


SIMULATED_PHISHING_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "sim-kyc-sms",
        "is_training_simulation": True,
        "simulation_badge": "TRAINING SIMULATION — SAFE EDUCATIONAL EXAMPLE",
        "channel": "SMS",
        "title_en": "Simulated Bank KYC Suspension SMS",
        "title_bn": "প্রশিক্ষণ সিমুলেশন: ভুয়া ব্যাংক KYC SMS",
        "sample_text": "Dear Merchant, your Current A/c will freeze in 2 hrs due to pending e-KYC. Update PAN & NetBanking PIN at http://sbi-kyc-portal.xyz/verify immediately.",
        "red_flags_en": [
            "Artificial 2-hour deadline to cause panic.",
            "Lookalike disposable domain (.xyz) instead of official bank domain.",
            "Asks for NetBanking PIN via a link — banks never do this.",
        ],
        "red_flags_bn": [
            "আতঙ্ক তৈরি করতে ২ ঘণ্টার কৃত্রিম সময়সীমা দেওয়া হয়েছে।",
            "আসল ব্যাংকের ডোমেইনের বদলে ভুয়া .xyz ডোমেইন ব্যবহার করা হয়েছে।",
            "লিঙ্কের মাধ্যমে NetBanking PIN চাওয়া হয়েছে যা ব্যাংক কখনো চায় না।",
        ],
    },
    {
        "id": "sim-whatsapp-boss",
        "is_training_simulation": True,
        "simulation_badge": "TRAINING SIMULATION — SAFE EDUCATIONAL EXAMPLE",
        "channel": "WhatsApp",
        "title_en": "Simulated Owner Impersonation WhatsApp Message",
        "title_bn": "প্রশিক্ষণ সিমুলেশন: মালিকের ছদ্মবেশী হোয়াটসঅ্যাপ",
        "sample_text": "Hi, this is Anil (store owner) texting from my new temporary number. Stuck at hospital, cannot take calls. Send Rs 18,000 urgently to supplier UPI quickpay99@ybl right now.",
        "red_flags_en": [
            "Unverified new phone number claiming to be the owner.",
            "Discourages phone verification ('cannot take calls').",
            "Pressures staff into an immediate irreversible UPI transfer.",
        ],
        "red_flags_bn": [
            "অজানা নতুন নম্বর থেকে মালিকের পরিচয় দাবি করা হয়েছে।",
            "ফোন করে যাচাই করতে নিরুৎসাহিত করা হয়েছে ('কল ধরতে পারছি না')।",
            "তাৎক্ষণিক UPI পেমেন্ট করার জন্য চাপ দেওয়া হয়েছে।",
        ],
    },
    {
        "id": "sim-upi-collect",
        "is_training_simulation": True,
        "simulation_badge": "TRAINING SIMULATION — SAFE EDUCATIONAL EXAMPLE",
        "channel": "WhatsApp / QR",
        "title_en": "Simulated UPI 'Receive Money' PIN Trap",
        "title_bn": "প্রশিক্ষণ সিমুলেশন: টাকা পাওয়ার নামে UPI PIN ফাঁদ",
        "sample_text": "I sent Rs 5,000 advance for your shop order. Click 'Accept Collect Request' and enter your 6-digit UPI PIN so the money credits to your account.",
        "red_flags_en": [
            "UPI PIN is ONLY for sending money, NEVER for receiving money.",
            "Approving a collect request with your PIN actually deducts money from your bank.",
        ],
        "red_flags_bn": [
            "UPI PIN শুধুমাত্র টাকা পাঠানোর সময় লাগে, টাকা পাওয়ার সময় কখনোই লাগে না।",
            "কালেক্ট রিকোয়েস্টে PIN দিলে আপনার অ্যাকাউন্ট থেকে টাকা কেটে যাবে।",
        ],
    },
]


QUIZ_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "slug": "phishing-defense-essentials",
        "title_en": "Phishing & Scam Defense for Shop Staff",
        "title_bn": "দোকান ও অফিস কর্মীদের জন্য ফিশিং ও স্ক্যাম প্রতিরোধ কুইজ",
        "topic": "Phishing & Social Engineering",
        "difficulty": "Beginner",
        "questions": [
            {
                "id": "q1",
                "prompt_en": "A customer says they transferred Rs 4,500 by mistake and sends a UPI 'Collect Request' asking you to enter your UPI PIN to receive/refund. What is true?",
                "prompt_bn": "একজন গ্রাহক টাকা পাঠানোর কথা বলে আপনাকে একটি UPI 'Collect Request' পাঠিয়ে UPI PIN দিতে বললেন। এর মধ্যে কোনটি সত্য?",
                "options_en": [
                    "Entering a UPI PIN only deducts money — you never enter a PIN to receive funds.",
                    "Entering a UPI PIN is required whenever an amount exceeds Rs 2,000.",
                    "It is safe as long as the caller sounds polite and shares a screenshot.",
                ],
                "options_bn": [
                    "UPI PIN দিলে টাকা কেটে যায় — টাকা পাওয়ার জন্য কখনোই PIN দিতে হয় না।",
                    "২,০০০ টাকার বেশি হলে টাকা পেতে PIN দিতে হয়।",
                    "কলার ভদ্রভাবে কথা বললে ও স্ক্রিনশট দেখালে এটি নিরাপদ।",
                ],
                "correct_index": 0,
                "explanation_en": "In UPI, PIN entry authorizes outbound payment only. Receiving money never requires entering your UPI PIN or scanning a QR code.",
                "explanation_bn": "UPI-তে PIN শুধুমাত্র টাকা পাঠানোর অনুমোদন দেয়; টাকা গ্রহণ করতে কখনোই PIN লাগে না।",
            },
            {
                "id": "q2",
                "prompt_en": "You receive an email with subject 'URGENT: GST Registration Cancelled' from gst-compliance@gmail.com with an attachment 'Notice.zip.exe'. What should you do?",
                "prompt_bn": "gst-compliance@gmail.com থেকে 'URGENT: GST Cancelled' এবং 'Notice.zip.exe' অ্যাটাচমেন্টসহ ইমেইল এলে কী করবেন?",
                "options_en": [
                    "Open the file immediately to avoid penalty.",
                    "Do not open the attachment; verify directly on official gst.gov.in or with your CA.",
                    "Forward it to every staff member so they can open it on their phones.",
                ],
                "options_bn": [
                    "জরিমানা এড়াতে সাথে সাথে ফাইলটি খুলবেন।",
                    "অ্যাটাচমেন্ট খুলবেন না; সরাসরি অফিসিয়াল gst.gov.in বা আপনার CA-এর সাথে যাচাই করবেন।",
                    "সব কর্মীর ফোনে ফাইলটি ফরওয়ার্ড করবেন।",
                ],
                "correct_index": 1,
                "explanation_en": "Official government portals do not send notices from free '@gmail.com' addresses or '.exe' executables.",
                "explanation_bn": "সরকারি পোর্টাল কখনোই ফ্রি '@gmail.com' থেকে বা '.exe' ফাইল পাঠায় না।",
            },
            {
                "id": "q3",
                "prompt_en": "A website URL shows 'https://hdfc-secure-kyc.top/login' with a browser padlock icon. Does the padlock prove it is HDFC Bank?",
                "prompt_bn": "একটি লিঙ্কে 'https://hdfc-secure-kyc.top/login' এবং ব্রাউজারে তালা চিহ্ন (HTTPS) দেখাচ্ছে। এটি কি প্রমাণ করে যে সাইটটি আসল HDFC ব্যাংকের?",
                "options_en": [
                    "Yes, HTTPS padlock means the bank verified the site.",
                    "No, attackers also get free HTTPS certificates — always check the real domain name.",
                    "Yes, if the page shows the bank logo at the top.",
                ],
                "options_bn": [
                    "হ্যাঁ, HTTPS তালা চিহ্ন মানেই ব্যাংক এটি যাচাই করেছে।",
                    "না, প্রতারকরাও ফ্রি HTTPS সার্টিফিকেট নিতে পারে — সবসময় আসল ডোমেইন যাচাই করতে হয়।",
                    "হ্যাঁ, পেজে ব্যাংকের লোগো থাকলে সেটি আসল।",
                ],
                "correct_index": 1,
                "explanation_en": "HTTPS only encrypts the connection between your browser and whichever server owns the domain; it never guarantees the domain belongs to a real bank.",
                "explanation_bn": "HTTPS কেবল সংযোগ এনক্রিপ্ট করে, ওয়েবসাইটটি আসল ব্যাংকের কি না তা প্রমাণ করে না।",
            },
            {
                "id": "q4",
                "prompt_en": "An unknown WhatsApp number claiming to be your shop owner asks you to transfer Rs 20,000 urgently and says 'Do not call me, I am in surgery/meeting'. Best response?",
                "prompt_bn": "অজানা হোয়াটসঅ্যাপ নম্বর থেকে মালিক সেজে ২০,০০০ টাকা পাঠাতে বলে 'কল করো না, মিটিংয়ে আছি' বললে কী করবেন?",
                "options_en": [
                    "Transfer half now and half later.",
                    "Refuse until you verify directly on the owner's known saved phone number or in person.",
                    "Ask the unknown WhatsApp number for their Aadhaar photo.",
                ],
                "options_bn": [
                    "অর্ধেক টাকা এখন এবং বাকি অর্ধেক পরে পাঠাবেন।",
                    "মালিকের আগে থেকে সেভ করা নম্বরে সরাসরি কল বা কথা বলে যাচাই না করে টাকা পাঠাবেন না।",
                    "অজানা নম্বরটি থেকে আধার ছবি চাইবেন।",
                ],
                "correct_index": 1,
                "explanation_en": "Secrecy and 'don't call me' are hallmark social engineering tactics used in CEO/owner impersonation fraud.",
                "explanation_bn": "'কল করো না' ও গোপনীয়তার চাপ মালিকের ছদ্মবেশী প্রতারণার সবচেয়ে বড় লক্ষণ।",
            },
        ],
    },
    {
        "slug": "workplace-cyber-hygiene",
        "title_en": "Passwords, Backups & Counter Device Hygiene",
        "title_bn": "পাসওয়ার্ড, ব্যাকআপ ও দোকানের ডিভাইস নিরাপত্তা কুইজ",
        "topic": "Device & Account Hygiene",
        "difficulty": "Intermediate",
        "questions": [
            {
                "id": "q1",
                "prompt_en": "Which authentication setup best protects your business email if a password gets leaked in a data breach?",
                "prompt_bn": "পাসওয়ার্ড ফাঁস হয়ে গেলেও কোন নিরাপত্তা ব্যবস্থা আপনার ব্যবসায়িক ইমেইলকে সবচেয়ে ভালো সুরক্ষা দেয়?",
                "options_en": [
                    "Changing one number at the end of the same password across sites.",
                    "Enabling Multi-Factor Authentication (MFA) with an authenticator app.",
                    "Writing the password in a locked WhatsApp chat.",
                ],
                "options_bn": [
                    "সব সাইটে একই পাসওয়ার্ডের শেষে শুধু একটি সংখ্যা বদলানো।",
                    "অথেনটিকেটর অ্যাপ ভিত্তিক মাল্টি-ফ্যাক্টর অথেনটিকেশন (MFA) চালু করা।",
                    "হোয়াটসঅ্যাপের লক করা চ্যাটে পাসওয়ার্ড লিখে রাখা।",
                ],
                "correct_index": 1,
                "explanation_en": "MFA requires a second verification factor beyond the password, blocking most automated and phished credential logins.",
                "explanation_bn": "MFA থাকলে শুধু পাসওয়ার্ড জেনে কেউ অ্যাকাউন্টে ঢুকতে পারে না।",
            },
            {
                "id": "q2",
                "prompt_en": "Your shop keeps Tally/billing backups only on a USB pendrive plugged into the billing PC all day. What is the main risk?",
                "prompt_bn": "দোকানের বিলিং ব্যাকআপ যদি সারাদিন বিলিং পিসিতে লাগানো একটি পেনড্রাইভে রাখা হয়, তবে প্রধান ঝুঁকি কী?",
                "options_en": [
                    "If ransomware infects the billing PC, it will also encrypt the connected pendrive.",
                    "USB pendrives erase files every midnight automatically.",
                    "There is no risk as long as the PC has Wi-Fi.",
                ],
                "options_bn": [
                    "পিসিতে র‍্যানসমওয়্যার আক্রমণ হলে যুক্ত থাকা পেনড্রাইভের ব্যাকআপও এনক্রিপ্ট হয়ে নষ্ট হয়ে যাবে।",
                    "পেনড্রাইভ প্রতি রাতে নিজে থেকেই ফাইল মুছে ফেলে।",
                    "পিসিতে Wi-Fi থাকলে কোনো ঝুঁকি নেই।",
                ],
                "correct_index": 0,
                "explanation_en": "Always keep at least one offline (unplugged) or immutable cloud backup copy so ransomware cannot encrypt your recovery data.",
                "explanation_bn": "র‍্যানসমওয়্যার থেকে বাঁচতে অন্তত একটি বিচ্ছিন্ন অফলাইন বা নিরাপদ ক্লাউড ব্যাকআপ রাখা জরুরি।",
            },
            {
                "id": "q3",
                "prompt_en": "A caller claiming to be from a courier or electricity board tells you to install AnyDesk and read out the 9-digit code to get a refund. What happens if you do?",
                "prompt_bn": "কুরিয়ার বা বিদ্যুৎ অফিসের কর্মী সেজে কেউ AnyDesk ইনস্টল করে ৯-সংখ্যার কোড বলতে বললে কী বিপদ হতে পারে?",
                "options_en": [
                    "It only shows your battery percentage.",
                    "The scammer gains remote control of your screen and can drain banking/UPI apps.",
                    "It speeds up your internet connection.",
                ],
                "options_bn": [
                    "এতে শুধু ফোনের ব্যাটারি দেখা যায়।",
                    "প্রতারক আপনার ফোনের সম্পূর্ণ রিমোট কন্ট্রোল পেয়ে ব্যাংকিং ও UPI অ্যাপ থেকে টাকা চুরি করতে পারে।",
                    "এতে ইন্টারনেটের গতি বাড়ে।",
                ],
                "correct_index": 1,
                "explanation_en": "Remote access apps like AnyDesk or TeamViewer grant full screen visibility and control; scammers use them to steal OTPs and authorize transfers.",
                "explanation_bn": "AnyDesk বা TeamViewer-এর কোড দিলে প্রতারক আপনার স্ক্রিন দেখে ও নিয়ন্ত্রণ করে ব্যাংক থেকে টাকা সরাতে পারে।",
            },
        ],
    },
]


def get_awareness_overview(language: str = "en") -> Dict[str, Any]:
    lessons = [
        {
            "id": l["id"],
            "topic": l["topic"],
            "title": l["title_bn"] if language == "bn" else l["title_en"],
            "duration_min": l["duration_min"],
            "summary": l["summary_bn"] if language == "bn" else l["summary_en"],
            "tips": l["tips_bn"] if language == "bn" else l["tips_en"],
        }
        for l in TRAINING_LESSONS
    ]
    simulations = [
        {
            "id": s["id"],
            "is_training_simulation": s["is_training_simulation"],
            "simulation_badge": s["simulation_badge"],
            "channel": s["channel"],
            "title": s["title_bn"] if language == "bn" else s["title_en"],
            "sample_text": s["sample_text"],
            "red_flags": s["red_flags_bn"] if language == "bn" else s["red_flags_en"],
        }
        for s in SIMULATED_PHISHING_EXAMPLES
    ]
    quizzes = [
        {
            "slug": q["slug"],
            "title": q["title_bn"] if language == "bn" else q["title_en"],
            "topic": q["topic"],
            "difficulty": q["difficulty"],
            "questions": [
                {
                    "id": qq["id"],
                    "prompt": qq["prompt_bn"] if language == "bn" else qq["prompt_en"],
                    "options": qq["options_bn"] if language == "bn" else qq["options_en"],
                }
                for qq in q["questions"]
            ],
        }
        for q in QUIZ_DEFINITIONS
    ]
    return {"lessons": lessons, "simulations": simulations, "quizzes": quizzes}


def grade_quiz(slug: str, answers: Dict[str, int], language: str = "en") -> Dict[str, Any]:
    quiz = next((q for q in QUIZ_DEFINITIONS if q["slug"] == slug), None)
    if not quiz:
        raise ValueError(f"Quiz '{slug}' not found.")

    score = 0
    total = len(quiz["questions"])
    summary: List[Dict[str, Any]] = []

    for qq in quiz["questions"]:
        chosen = answers.get(qq["id"], -1)
        correct = qq["correct_index"]
        is_correct = chosen == correct
        if is_correct:
            score += 1
        summary.append(
            {
                "question_id": qq["id"],
                "prompt": qq["prompt_bn"] if language == "bn" else qq["prompt_en"],
                "chosen_index": chosen,
                "correct_index": correct,
                "is_correct": is_correct,
                "explanation": qq["explanation_bn"] if language == "bn" else qq["explanation_en"],
            }
        )

    percentage = round((score / total) * 100.0, 1) if total else 0.0
    return {
        "quiz_slug": slug,
        "quiz_title": quiz["title_bn"] if language == "bn" else quiz["title_en"],
        "score": score,
        "total_questions": total,
        "percentage": percentage,
        "answers_summary": summary,
    }

