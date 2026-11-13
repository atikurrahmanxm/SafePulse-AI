import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowRight,
  CheckCircle2,
  ChevronDown,
  ClipboardCheck,
  FileBarChart2,
  FileWarning,
  Globe,
  GraduationCap,
  Link2,
  MessageSquareWarning,
  Shield,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useLanguage } from "../i18n/LanguageContext";
import { Logo } from "../components/layout/Logo";
import { Button, Card } from "../components/ui/Primitives";

const FAQS = [
  {
    q_en: "Can CyberShield AI run without paid external threat APIs?",
    q_bn: "কোনো পেইড বাহ্যিক API ছাড়া কি CyberShield AI কাজ করে?",
    a_en: "Yes. The phishing classifier, heuristic rules, SSRF-safe URL & DNS inspector, security assessment, incident playbooks, and PDF reporting all work completely locally.",
    a_bn: "হ্যাঁ। ফিশিং ML মডেল, হিউরিস্টিক নিয়ম, URL ও DNS বিশ্লেষক, বিজনেস সিকিউরিটি চেক এবং ইনসিডেন্ট প্লেবুক সম্পূর্ণ স্থানীয়ভাবে কাজ করে।",
  },
  {
    q_en: "Does the URL scanner open or visit suspicious websites?",
    q_bn: "URL স্ক্যানার কি সন্দেহজনক ওয়েবসাইটগুলো ওপেন করে?",
    a_en: "No. To protect against SSRF and malware exposure, CyberShield AI never fetches or renders submitted URLs. It runs static inspection and read-only DNS checks while blocking localhost and private IP ranges.",
    a_bn: "না। নিরাপত্তার জন্য এটি কখনোই জমা দেওয়া URL ওপেন বা ডাউনলোড করে না। এটি কেবল স্ট্যাটিক লিঙ্ক বিশ্লেষণ ও নিরাপদ DNS যাচাই করে এবং লোকালহোস্ট বা প্রাইভেট IP ব্লক করে।",
  },
  {
    q_en: "Does HTTPS on a website mean it is safe?",
    q_bn: "ওয়েবসাইটে HTTPS বা তালা চিহ্ন থাকা মানেই কি সেটি নিরাপদ?",
    a_en: "No. HTTPS only encrypts traffic; attackers can also get free TLS certificates for phishing domains. Always verify the exact domain spelling.",
    a_bn: "না। HTTPS শুধু তথ্য এনক্রিপ্ট করে; প্রতারকরাও ফ্রি HTTPS নিতে পারে। তাই মূল ডোমেইন নাম যাচাই করা জরুরি।",
  },
  {
    q_en: "Can CyberShield AI automatically remove ransomware or recover hacked accounts?",
    q_bn: "CyberShield AI কি নিজে থেকে র‍্যানসমওয়্যার সরাতে বা হ্যাক হওয়া অ্যাকাউন্ট উদ্ধার করতে পারে?",
    a_en: "No. Our Incident Response Center gives non-technical owners clear containment checklists and India 1930 helpline reporting steps, while highlighting when IT support or your bank must act.",
    a_bn: "না। এটি আপনাকে ধাপে ধাপে করণীয় এবং ১৯৩০ হেল্পলাইনে রিপোর্ট করার নির্দেশনা দেয়, তবে সরাসরি ম্যালওয়্যার সরাতে বা ব্যাংক অ্যাকাউন্ট ফেরত আনতে পারে না।",
  },
];

export function LandingPage() {
  const navigate = useNavigate();
  const { user, startDemoMode } = useAuth();
  const { language, setLanguage, t } = useLanguage();
  const isBn = language === "bn";
  const [demoLoading, setDemoLoading] = useState(false);
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  const handleDemo = async () => {
    setDemoLoading(true);
    try {
      await startDemoMode();
      navigate("/app");
    } finally {
      setDemoLoading(false);
    }
  };

  const steps = isBn
    ? [
        {
          num: "01",
          title: "মেসেজ বা লিংক পেস্ট করুন",
          desc: "সন্দেহজনক WhatsApp, SMS, ইমেইল বা ওয়েবসাইট লিংক নিরাপদে যাচাই করতে দিন।",
        },
        {
          num: "02",
          title: "সহজ AI বিশ্লেষণ পান",
          desc: "০–১০০ ঝুঁকির স্কোর ও সাধারণ ভাষায় “এখন কী করবেন” পরামর্শ দেখে নিন।",
        },
        {
          num: "03",
          title: "১-ক্লিকে PDF ও অ্যাকশন নিন",
          desc: "মাসিক বা স্ক্যান রিপোর্ট ডাউনলোড করুন এবং ১৯৩০ হেল্পলাইন গাইড অনুসরণ করুন।",
        },
      ]
    : [
        {
          num: "01",
          title: "Paste Message or Link",
          desc: "Drop any suspicious SMS, WhatsApp text, email, or website URL without opening it.",
        },
        {
          num: "02",
          title: "Get Plain-Language Verdict",
          desc: "See an explainable 0–100 risk score, trigger phrases, and clear next steps.",
        },
        {
          num: "03",
          title: "Export PDF & Protect Team",
          desc: "Download 1-click PDF reports and follow 6-phase playbooks when incidents happen.",
        },
      ];

  const features = isBn
    ? [
        {
          icon: MessageSquareWarning,
          color: "text-rose-400 bg-rose-500/15 border-rose-500/30",
          title: "AI ফিশিং ডিটেক্টর",
          desc: "ভুয়া ব্যাংক KYC, OTP প্রতারণা ও জরুরি চাপের ভাষা নিমিষেই শনাক্ত করে।",
        },
        {
          icon: Link2,
          color: "text-cyan-300 bg-cyan-500/15 border-cyan-500/30",
          title: "নিরাপদ URL ও DNS স্ক্যানার",
          desc: "লিংক না খুলেই টাইপো-ডোমেইন, SSL সার্টিফিকেট এবং SPF/DMARC যাচাই করে।",
        },
        {
          icon: ClipboardCheck,
          color: "text-emerald-400 bg-emerald-500/15 border-emerald-500/30",
          title: "১০-পয়েন্ট সিকিউরিটি চেকআপ",
          desc: "দোকান বা অফিসের পাসওয়ার্ড, MFA ও ব্যাকআপের অবস্থা যাচাই করে স্কোর দেয়।",
        },
        {
          icon: FileWarning,
          color: "text-amber-400 bg-amber-500/15 border-amber-500/30",
          title: "ইনসিডেন্ট রেসপন্স ও ১৯৩০",
          desc: "হ্যাক বা UPI প্রতারণা হলে ৬ ধাপের চেকলিস্ট ও ১৯৩০ রিপোর্টিং গাইড দেয়।",
        },
        {
          icon: FileBarChart2,
          color: "text-indigo-300 bg-indigo-500/15 border-indigo-500/30",
          title: "সহজ PDF রিপোর্ট সেন্টার",
          desc: "মাসিক, ফিশিং, লিংক, চেকআপ ও ঘটনার PDF রিপোর্ট ১ ক্লিকে ডাউনলোড করুন।",
        },
        {
          icon: GraduationCap,
          color: "text-sky-300 bg-sky-500/15 border-sky-500/30",
          title: "টিম সচেতনতা ও কুইজ",
          desc: "কর্মচারীদের জন্য বাংলা ও ইংরেজি প্রশিক্ষণ ও কুইজ ট্র্যাকিং।",
        },
      ]
    : [
        {
          icon: MessageSquareWarning,
          color: "text-rose-400 bg-rose-500/15 border-rose-500/30",
          title: "AI Phishing Detector",
          desc: "Spots fake bank KYC, UPI traps, and urgency cues across SMS, WhatsApp, and email.",
        },
        {
          icon: Link2,
          color: "text-cyan-300 bg-cyan-500/15 border-cyan-500/30",
          title: "SSRF-Safe URL Scanner",
          desc: "Checks lookalike domains, TLS certificates, and SPF/DMARC without visiting unsafe links.",
        },
        {
          icon: ClipboardCheck,
          color: "text-emerald-400 bg-emerald-500/15 border-emerald-500/30",
          title: "10-Point Security Checkup",
          desc: "Scores MFA, backups, updates, and Wi-Fi hygiene with clear improvement steps.",
        },
        {
          icon: FileWarning,
          color: "text-amber-400 bg-amber-500/15 border-amber-500/30",
          title: "Incident Playbooks & 1930",
          desc: "Step-by-step containment checklists, owner assignments, and India 1930 escalation.",
        },
        {
          icon: FileBarChart2,
          color: "text-indigo-300 bg-indigo-500/15 border-indigo-500/30",
          title: "Easy PDF Reports Center",
          desc: "Export monthly executive, phishing, URL, checkup, and incident PDFs in 1 click.",
        },
        {
          icon: GraduationCap,
          color: "text-sky-300 bg-sky-500/15 border-sky-500/30",
          title: "Staff Cyber Awareness",
          desc: "Short bilingual lessons and quizzes so counter staff spot scams before clicking.",
        },
      ];

  return (
    <div className="min-h-[100dvh] bg-[#070B18] text-[#F8FAFC]">
      {/* Clean Sticky Header */}
      <header className="sticky top-0 z-30 border-b border-slate-800/70 bg-[#070B18]/85 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between gap-2 px-3 sm:gap-4 sm:px-6">
          <Logo size="sm" />
          <nav aria-label="Landing Navigation" className="hidden md:flex items-center gap-7 text-sm font-medium text-slate-300">
            <a href="#how-it-works" className="transition-colors hover:text-white">
              {isBn ? "কীভাবে কাজ করে" : "How It Works"}
            </a>
            <a href="#features" className="transition-colors hover:text-white">
              {isBn ? "ফিচারসমূহ" : "Features"}
            </a>
            <a href="#faq" className="transition-colors hover:text-white">
              {isBn ? "প্রশ্নোত্তর" : "FAQ"}
            </a>
          </nav>
          <div className="flex shrink-0 items-center gap-1.5 sm:gap-2.5">
            <button
              type="button"
              onClick={() => setLanguage(language === "en" ? "bn" : "en")}
              className="inline-flex items-center gap-1 rounded-lg border border-slate-700/80 bg-[#111A33] px-2 py-1.5 text-xs font-medium text-slate-200 transition-colors hover:bg-[#1B2942] sm:gap-1.5 sm:px-2.5"
            >
              <Globe className="h-3.5 w-3.5 text-[#06B6D4]" aria-hidden="true" />
              <span>{language === "en" ? "বাংলা" : "English"}</span>
            </button>
            {user ? (
              <Button onClick={() => navigate("/app")} size="sm">
                {isBn ? "ড্যাশবোর্ড খোলো" : "Open Console"}
              </Button>
            ) : (
              <>
                <Button variant="ghost" size="sm" className="hidden sm:inline-flex" onClick={() => navigate("/login")}>
                  {isBn ? "সাইন ইন" : "Sign In"}
                </Button>
                <Button size="sm" onClick={() => navigate("/register")}>
                  {t.landing.getStarted}
                </Button>
              </>
            )}
          </div>
        </div>
      </header>

      <main>
        {/* Hero Section — Balanced, Breathable & Visual */}
        <section className="relative overflow-hidden border-b border-slate-800/60">
          <div
            className="pointer-events-none absolute inset-0"
            style={{
              background:
                "radial-gradient(60% 50% at 20% 15%, rgba(99, 102, 241, 0.18), transparent 70%), radial-gradient(50% 45% at 85% 25%, rgba(6, 182, 212, 0.14), transparent 70%)",
            }}
            aria-hidden="true"
          />
          <div className="relative mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-24">
            <div className="grid items-center gap-12 lg:grid-cols-12">
              <div className="min-w-0 lg:col-span-6">
                <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-indigo-400/30 bg-indigo-500/10 px-3.5 py-1 text-xs font-medium text-indigo-200">
                  <Sparkles className="h-3.5 w-3.5 text-cyan-300" aria-hidden="true" />
                  <span>
                    {isBn
                      ? "AdtU Innovation Mela 2026 • ছোট ব্যবসার সাইবার সুরক্ষা"
                      : "AdtU Innovation Mela 2026 • Built for SMEs"}
                  </span>
                </div>
                <h1 className="text-3xl font-bold tracking-tight text-white sm:text-5xl sm:leading-[1.12]">
                  {t.landing.heroHeadline}
                </h1>
                <p className="mt-5 max-w-xl text-base leading-relaxed text-slate-300">
                  {t.landing.heroSub}
                </p>

                <div className="mt-8 flex flex-wrap items-center gap-3.5">
                  <Button size="lg" onClick={() => navigate(user ? "/app" : "/register")}>
                    <span>{t.landing.getStarted}</span>
                    <ArrowRight className="h-4 w-4" aria-hidden="true" />
                  </Button>
                  <Button
                    size="lg"
                    variant="secondary"
                    onClick={handleDemo}
                    disabled={demoLoading}
                  >
                    <Shield className="h-4 w-4 text-[#06B6D4]" aria-hidden="true" />
                    <span>{demoLoading ? "Loading Demo..." : t.landing.tryDemo}</span>
                  </Button>
                </div>

                <div className="mt-7 flex flex-wrap items-center gap-x-6 gap-y-2 text-xs text-slate-400">
                  <span className="inline-flex items-center gap-1.5">
                    <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" aria-hidden="true" />
                    {isBn ? "বাংলা ও ইংরেজি সাপোর্ট" : "English & বাংলা Ready"}
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <CheckCircle2 className="h-3.5 w-3.5 text-cyan-400" aria-hidden="true" />
                    {isBn ? "১-ক্লিক PDF রিপোর্ট" : "1-Click PDF Reports"}
                  </span>
                  <span className="inline-flex items-center gap-1.5">
                    <CheckCircle2 className="h-3.5 w-3.5 text-indigo-400" aria-hidden="true" />
                    {isBn ? "কোনো পেইড API ছাড়াই চলে" : "Runs 100% Locally"}
                  </span>
                </div>
              </div>

              {/* Clean Visual Dashboard Preview Card */}
              <div className="min-w-0 lg:col-span-6">
                <div className="cs-card rounded-2xl border border-slate-700/70 p-6 shadow-2xl shadow-indigo-950/50">
                  <div className="flex items-center justify-between border-b border-slate-800/80 pb-4">
                    <div className="flex items-center gap-2.5">
                      <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-cyan-500/15 text-cyan-300 ring-1 ring-cyan-500/30">
                        <ShieldCheck className="h-4 w-4" aria-hidden="true" />
                      </span>
                      <div>
                        <div className="text-xs font-semibold text-white">
                          {isBn ? "সিকিউরিটি কনসোল প্রিভিউ" : "Security Console Preview"}
                        </div>
                        <div className="text-[11px] text-slate-400">
                          {isBn ? "উদাহরণ ডেমো দৃশ্য" : "Sample Business Workspace"}
                        </div>
                      </div>
                    </div>
                    <span className="rounded-full border border-emerald-500/35 bg-emerald-500/10 px-2.5 py-0.5 text-[11px] font-medium text-emerald-300">
                      {isBn ? "সুরক্ষিত মোড" : "Sample Preview"}
                    </span>
                  </div>

                  {/* Clean Posture Ring + Quick Summary */}
                  <div className="mt-5 grid items-center gap-5 sm:grid-cols-12">
                    <div className="flex flex-col items-center justify-center rounded-xl border border-slate-800/80 bg-[#0A1124]/80 p-4 sm:col-span-5">
                      <svg viewBox="0 0 120 76" className="w-32" aria-hidden="true">
                        <defs>
                          <linearGradient id="heroPreviewArc" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#6366F1" />
                            <stop offset="60%" stopColor="#06B6D4" />
                            <stop offset="100%" stopColor="#22C55E" />
                          </linearGradient>
                        </defs>
                        <path
                          d="M 14 64 A 46 46 0 0 1 106 64"
                          fill="none"
                          stroke="#1E293B"
                          strokeWidth="10"
                          strokeLinecap="round"
                        />
                        <path
                          d="M 14 64 A 46 46 0 0 1 106 64"
                          fill="none"
                          stroke="url(#heroPreviewArc)"
                          strokeWidth="10"
                          strokeLinecap="round"
                          strokeDasharray="124 145"
                        />
                        <text x="60" y="54" textAnchor="middle" className="fill-white text-xl font-bold">
                          86%
                        </text>
                        <text x="60" y="68" textAnchor="middle" className="fill-emerald-400 text-[9px] font-medium">
                          {isBn ? "ভালো সুরক্ষা" : "Strong Posture"}
                        </text>
                      </svg>
                    </div>

                    <div className="space-y-2.5 sm:col-span-7">
                      <div className="flex items-center justify-between rounded-xl border border-rose-500/30 bg-rose-500/10 px-3.5 py-2.5">
                        <div>
                          <div className="text-xs font-semibold text-white">
                            {isBn ? "ভুয়া KYC SMS ধরা পড়েছে" : "Fake Bank KYC Scam"}
                          </div>
                          <div className="text-[11px] text-rose-200/80">
                            {isBn ? "লিংক ও OTP প্রতারণা ব্লক" : "Urgency & OTP trap flagged"}
                          </div>
                        </div>
                        <span className="rounded-md bg-rose-500/20 px-2 py-0.5 font-mono text-[11px] font-bold text-rose-300">
                          92/100
                        </span>
                      </div>

                      <div className="flex items-center justify-between rounded-xl border border-cyan-500/25 bg-[#0A1124]/85 px-3.5 py-2.5">
                        <div>
                          <div className="text-xs font-semibold text-white">
                            {isBn ? "URL ও SSL যাচাই" : "URL & DNS Inspection"}
                          </div>
                          <div className="text-[11px] text-slate-400">
                            {isBn ? "SPF / DMARC ও ডোমেইন চেক" : "SPF, DMARC & TLS verified"}
                          </div>
                        </div>
                        <span className="rounded-md bg-emerald-500/15 px-2 py-0.5 text-[11px] font-semibold text-emerald-300">
                          {isBn ? "নিরাপদ" : "SSRF-Safe"}
                        </span>
                      </div>

                      <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-[#0A1124]/85 px-3.5 py-2.5">
                        <div>
                          <div className="text-xs font-semibold text-white">
                            {isBn ? "মাসিক বিজনেস PDF রিপোর্ট" : "Monthly Security PDF"}
                          </div>
                          <div className="text-[11px] text-slate-400">
                            {isBn ? "১ ক্লিকে প্রিন্ট ও শেয়ারযোগ্য" : "Ready in 1 click (EN / বাংলা)"}
                          </div>
                        </div>
                        <span className="rounded-md border border-indigo-400/35 bg-indigo-500/15 px-2 py-0.5 text-[11px] font-medium text-indigo-200">
                          PDF
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works — 3 Clean Steps */}
        <section id="how-it-works" className="mx-auto max-w-6xl px-4 py-20 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <span className="text-xs font-semibold uppercase tracking-widest text-cyan-400">
              {isBn ? "সহজ ৩ ধাপ" : "Simple 3-Step Workflow"}
            </span>
            <h2 className="mt-2 text-2xl font-bold text-white sm:text-3xl">
              {isBn ? "কোনো টেকনিক্যাল জ্ঞান ছাড়াই ব্যবহার করুন" : "Cybersecurity anyone can use in seconds"}
            </h2>
          </div>

          <div className="mt-10 grid gap-6 md:grid-cols-3">
            {steps.map((s) => (
              <Card key={s.num} className="p-6">
                <div className="inline-flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500/25 to-cyan-500/20 font-mono text-xs font-bold text-cyan-300 ring-1 ring-cyan-500/30">
                  {s.num}
                </div>
                <h3 className="mt-4 text-base font-semibold text-white">{s.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-400">{s.desc}</p>
              </Card>
            ))}
          </div>
        </section>

        {/* Main Capabilities — Crisp 6-Card Grid */}
        <section id="features" className="border-y border-slate-800/70 bg-[#0B1224]/70">
          <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6">
            <div className="mx-auto max-w-2xl text-center">
              <span className="text-xs font-semibold uppercase tracking-widest text-cyan-400">
                {isBn ? "মূল ফিচারসমূহ" : "Everything Included"}
              </span>
              <h2 className="mt-2 text-2xl font-bold text-white sm:text-3xl">
                {isBn
                  ? "ছোট ব্যবসা সুরক্ষার সবকিছু এক প্ল্যাটফর্মে"
                  : "One calm workspace to prevent, check, and respond"}
              </h2>
            </div>

            <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {features.map((f) => (
                <Card key={f.title} className="p-6">
                  <div className={`inline-flex h-10 w-10 items-center justify-center rounded-xl border ${f.color}`}>
                    <f.icon className="h-5 w-5" aria-hidden="true" />
                  </div>
                  <h3 className="mt-4 text-base font-semibold text-white">{f.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-slate-400">{f.desc}</p>
                </Card>
              ))}
            </div>
          </div>
        </section>

        {/* FAQ Section — Clean & Focused */}
        <section id="faq" className="mx-auto max-w-4xl px-4 py-20 sm:px-6">
          <div className="text-center">
            <span className="text-xs font-semibold uppercase tracking-widest text-cyan-400">
              {isBn ? "সচরাচর জিজ্ঞাসা" : "FAQ"}
            </span>
            <h2 className="mt-2 text-2xl font-bold text-white sm:text-3xl">
              {isBn ? "স্বচ্ছ ও বাস্তবসম্মত উত্তর" : "Honest answers about safety & scope"}
            </h2>
          </div>

          <div className="mt-8 space-y-3">
            {FAQS.map((item, idx) => {
              const isOpen = openFaq === idx;
              return (
                <Card key={item.q_en}>
                  <button
                    type="button"
                    onClick={() => setOpenFaq(isOpen ? null : idx)}
                    aria-expanded={isOpen}
                    className="flex w-full items-center justify-between gap-4 px-5 py-4 text-left text-sm font-semibold text-slate-100"
                  >
                    <span>{isBn ? item.q_bn : item.q_en}</span>
                    <ChevronDown
                      className={`h-4 w-4 shrink-0 text-slate-400 transition-transform ${
                        isOpen ? "rotate-180" : ""
                      }`}
                      aria-hidden="true"
                    />
                  </button>
                  {isOpen && (
                    <div className="border-t border-slate-800/80 px-5 py-3.5 text-sm leading-relaxed text-slate-300">
                      {isBn ? item.a_bn : item.a_en}
                    </div>
                  )}
                </Card>
              );
            })}
          </div>
        </section>

        {/* Bottom CTA Strip */}
        <section className="mx-auto max-w-6xl px-4 pb-20 sm:px-6">
          <div className="cs-card flex flex-col items-center justify-between gap-6 rounded-2xl border border-indigo-500/30 bg-gradient-to-r from-indigo-950/60 via-[#101A36] to-cyan-950/50 px-6 py-10 text-center sm:flex-row sm:px-10 sm:text-left">
            <div>
              <h2 className="text-xl font-bold text-white sm:text-2xl">
                {isBn
                  ? "এখনই আপনার ব্যবসার নিরাপত্তা যাচাই করে দেখুন"
                  : "Ready to see CyberShield AI in action?"}
              </h2>
              <p className="mt-1.5 text-sm text-slate-300">
                {isBn
                  ? "ডেমো মোডে ১ ক্লিকে সব ফিচার ঘুরে দেখুন অথবা নিজের দোকানের অ্যাকাউন্ট তৈরি করুন।"
                  : "Explore all tools instantly in Demo Mode or create an isolated workspace for your shop."}
              </p>
            </div>
            <div className="flex flex-wrap justify-center gap-3">
              <Button size="lg" variant="secondary" onClick={handleDemo} disabled={demoLoading}>
                <span>{demoLoading ? "Loading..." : t.landing.tryDemo}</span>
              </Button>
              <Button size="lg" onClick={() => navigate(user ? "/app" : "/register")}>
                <span>{t.landing.getStarted}</span>
                <ArrowRight className="h-4 w-4" aria-hidden="true" />
              </Button>
            </div>
          </div>
        </section>
      </main>

      {/* Clean Footer */}
      <footer className="border-t border-slate-800/80 bg-[#070B18] px-4 py-8 sm:px-6">
        <div className="mx-auto flex max-w-6xl flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
          <div>
            <Logo size="sm" />
            <p className="mt-2 text-xs text-slate-400">
              {t.tagline} • Assam down town University (AdtU) Innovation Mela 2026
            </p>
          </div>
          <div className="flex flex-wrap gap-5 text-xs font-medium text-slate-400">
            <button type="button" onClick={() => navigate("/login")} className="hover:text-white">
              {isBn ? "সাইন ইন" : "Sign In"}
            </button>
            <button type="button" onClick={() => navigate("/register")} className="hover:text-white">
              {isBn ? "নতুন অ্যাকাউন্ট" : "Register Business"}
            </button>
            <button type="button" onClick={handleDemo} className="hover:text-white">
              {isBn ? "ডেমো মোড" : "Demo Mode"}
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
