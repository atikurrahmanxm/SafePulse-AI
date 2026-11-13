import React, { useState } from "react";
import {
  AlertTriangle,
  CheckCircle2,
  Database,
  Download,
  ExternalLink,
  Key,
  Lock,
  PhoneCall,
  Search,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { Button, Card, CardContent, CardHeader, RiskBadge } from "../components/ui/Primitives";
import { ProgressRing } from "../components/ui/ProgressRing";
import { useLanguage } from "../i18n/LanguageContext";
import {
  ApiError,
  BreachCheckResult,
  checkBreachExposure,
  downloadPdfReport,
  getDemoBreachSample,
} from "../lib/api";
import { cn } from "../lib/utils";

const QUICK_SAMPLES = [
  {
    label_en: "Scenario 1: Retail POS Billing Leak",
    label_bn: "নমুনা ১: রিটেল POS বিলিং ডাটা ফাঁস",
    query: "owner@pharmacy.in",
  },
  {
    label_en: "Scenario 2: Pharma B2B Vendor Leak",
    label_bn: "নমুনা ২: ফার্মাসাপ্লাই B2B পোর্টাল লিক",
    query: "admin@brahmaputra-pharma.in",
  },
  {
    label_en: "Scenario 3: Logistics Merchant Spill",
    label_bn: "নমুনা ৩: কুরিয়ার মার্চেন্ট অ্যাকাউন্ট লিক",
    query: "delivery@quickcourier.in",
  },
  {
    label_en: "Scenario 4: Clean Business Account",
    label_bn: "নমুনা ৪: সুরক্ষিত পরিষ্কার অ্যাকাউন্ট",
    query: "clean-owner@safepulse.local",
  },
];

export function BreachMonitorPage() {
  const { language, t } = useLanguage();
  const isBn = language === "bn";

  const [query, setQuery] = useState("owner@pharmacy.in");
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<BreachCheckResult | null>(null);
  const [checkedActions, setCheckedActions] = useState<Record<number, boolean>>({});

  const handleScan = async (targetQuery?: string) => {
    const q = (targetQuery || query).trim();
    if (!q || q.length < 3) {
      setError(
        isBn
          ? "অনুগ্রহ করে একটি বৈধ ব্যবসায়িক ইমেইল বা ডোমেইন নাম লিখুন।"
          : "Please enter a valid business email address or domain name."
      );
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const data = await checkBreachExposure(q, language);
      setResult(data);
      setCheckedActions({});
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to complete breach scan.");
    } finally {
      setLoading(false);
    }
  };

  const handleLoadDemo = async () => {
    setError(null);
    setLoading(true);
    try {
      const data = await getDemoBreachSample(language);
      setQuery(data.query);
      setResult(data);
      setCheckedActions({});
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to load demo scenario.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!result) return;
    setDownloading(true);
    try {
      await downloadPdfReport(
        `/api/breaches/report.pdf?query=${encodeURIComponent(result.query)}&language=${language}`,
        `safepulse-breach-report-${result.query.replace(/[^a-zA-Z0-9]/g, "_")}.pdf`
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not generate breach PDF report.");
    } finally {
      setDownloading(false);
    }
  };

  const toggleAction = (idx: number) => {
    setCheckedActions((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  return (
    <div className="space-y-6">
      {/* 4 Hackathon Focus Pillars Bar */}
      <div className="flex flex-wrap items-center gap-2 rounded-xl border border-indigo-500/20 bg-indigo-950/20 px-4 py-2 text-xs text-slate-300">
        <span className="font-semibold text-slate-200">
          {isBn ? "হ্যাকাথন কোর ফোকাস:" : "Hackathon Scope Alignment:"}
        </span>
        <span className="inline-flex items-center gap-1 rounded-md bg-slate-800/80 px-2 py-0.5 text-slate-300">
          🎣 {isBn ? "ফিশিং ডিটেকশন" : "Phishing Attempts"}
        </span>
        <span className="inline-flex items-center gap-1 rounded-md bg-slate-800/80 px-2 py-0.5 text-slate-300">
          🦠 {isBn ? "ম্যালওয়্যার সুরক্ষা" : "Malware Payloads"}
        </span>
        <span className="inline-flex items-center gap-1 rounded-md bg-slate-800/80 px-2 py-0.5 text-slate-300">
          ⚠️ {isBn ? "সন্দেহজনক কার্যক্রম" : "Suspicious Activities"}
        </span>
        <span className="inline-flex items-center gap-1 rounded-md border border-cyan-400/40 bg-cyan-400/15 px-2 py-0.5 font-bold text-cyan-300 shadow-[0_0_12px_rgba(6,182,212,0.3)]">
          🛡️ {isBn ? "ডাটা ব্রিচ ও ফাঁস মনিটর" : "Potential Data Breaches"}
        </span>
      </div>

      {/* Page Header */}
      <div>
        <h1 className="text-xl font-bold tracking-tight text-white sm:text-2xl">
          {t.breaches.title}
        </h1>
        <p className="mt-1 text-sm text-slate-400">{t.breaches.subtitle}</p>
      </div>

      {/* Input / Scanner Card */}
      <Card className="cs-card">
        <CardContent className="p-5 sm:p-6">
          <form
            onSubmit={(e: React.FormEvent) => {
              e.preventDefault();
              handleScan();
            }}
            className="space-y-4"
          >
            <div>
              <label
                htmlFor="breach-query-input"
                className="mb-1.5 block text-xs font-semibold text-slate-200"
              >
                {t.breaches.inputLabel}
              </label>
              <div className="relative">
                <Search
                  className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
                  aria-hidden="true"
                />
                <input
                  id="breach-query-input"
                  type="text"
                  value={query}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setQuery(e.target.value)}
                  placeholder={t.breaches.inputPlaceholder}
                  className="w-full rounded-xl border border-slate-700/80 bg-[#0B1226] pl-10 pr-4 py-2.5 text-sm text-slate-100 placeholder:text-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  disabled={loading}
                />
              </div>
            </div>

            {/* Quick Demo Scenario Pills */}
            <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
              <span className="font-medium text-slate-400">
                {isBn ? "দ্রুত নমুনা পরীক্ষা:" : "Quick Test Samples:"}
              </span>
              {QUICK_SAMPLES.map((sample, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => {
                    setQuery(sample.query);
                    handleScan(sample.query);
                  }}
                  className="rounded-md border border-slate-700 bg-slate-800/80 px-2.5 py-1 text-slate-300 transition-colors hover:border-cyan-400/50 hover:bg-slate-700 hover:text-white"
                >
                  {isBn ? sample.label_bn : sample.label_en}
                </button>
              ))}
            </div>

            {error && (
              <div
                role="alert"
                className="flex items-start gap-2 rounded-lg border border-red-500/30 bg-red-950/40 p-3 text-xs text-red-200"
              >
                <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0 text-red-400" />
                <span>{error}</span>
              </div>
            )}

            <div className="flex flex-wrap items-center gap-3 pt-2">
              <Button type="submit" disabled={loading} size="md">
                <Search className="h-4 w-4" aria-hidden="true" />
                <span>{loading ? t.breaches.scanning : t.breaches.scanBtn}</span>
              </Button>
              <Button
                type="button"
                variant="secondary"
                onClick={handleLoadDemo}
                disabled={loading}
                size="md"
              >
                <Sparkles className="h-4 w-4 text-cyan-400" aria-hidden="true" />
                <span>{t.breaches.demoBtn}</span>
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Results View */}
      {result && (
        <div className="space-y-6">
          {/* Verdict Banner */}
          <Card
            className={
              result.exposure_count > 0
                ? "cs-card border-red-500/40 bg-gradient-to-r from-red-950/40 via-slate-900 to-indigo-950/30"
                : "cs-card border-emerald-500/40 bg-gradient-to-r from-emerald-950/40 via-slate-900 to-indigo-950/30"
            }
          >
            <CardContent className="flex flex-col items-center justify-between gap-6 p-6 sm:flex-row">
              <div className="flex flex-col items-center gap-4 text-center sm:flex-row sm:text-left">
                <ProgressRing
                  value={result.risk_score}
                  max={100}
                  size={84}
                  strokeWidth={7}
                  colorHex={
                    result.exposure_count > 0
                      ? result.risk_level === "Critical"
                        ? "#F43F5E"
                        : "#F59E0B"
                      : "#10B981"
                  }
                  label={result.risk_level}
                  sublabel="/ 100"
                />
                <div>
                  <div className="flex flex-wrap items-center justify-center gap-2 sm:justify-start">
                    <RiskBadge category={result.risk_level} />
                    <span className="text-xs font-mono text-slate-400">
                      Target: {result.query} ({result.query_type.toUpperCase()})
                    </span>
                  </div>
                  <h2 className="mt-1 text-lg font-bold text-white sm:text-xl">
                    {result.category}
                  </h2>
                  <p className="mt-1 text-xs text-slate-300 max-w-xl">{result.summary}</p>
                </div>
              </div>
              <div className="shrink-0">
                <Button
                  onClick={handleDownloadPdf}
                  disabled={downloading}
                  variant="secondary"
                  size="md"
                  className="border-indigo-400/40 hover:bg-indigo-500/10 text-slate-100"
                >
                  <Download className="h-4 w-4 text-cyan-400" aria-hidden="true" />
                  <span>
                    {downloading
                      ? isBn
                        ? "ডাউনলোড হচ্ছে..."
                        : "Generating PDF..."
                      : t.breaches.downloadPdf}
                  </span>
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Two-Column Details */}
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
            {/* Left 2 Cols: Matched Breaches & Data Classes */}
            <div className="space-y-6 lg:col-span-2">
              {/* Leaked Data Classes */}
              {result.data_classes_exposed.length > 0 && (
                <Card className="cs-card">
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-2 text-sm font-bold text-white">
                      <Lock className="h-4 w-4 text-cyan-400" aria-hidden="true" />
                      <span>{t.breaches.dataClassesTitle}</span>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-2">
                      {result.data_classes_exposed.map((dc, i) => (
                        <span
                          key={i}
                          className="inline-flex items-center gap-1.5 rounded-lg border border-red-500/30 bg-red-950/50 px-3 py-1 text-xs font-medium text-red-200"
                        >
                          <Key className="h-3 w-3 text-red-400" aria-hidden="true" />
                          {dc}
                        </span>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Matched Breach Incidents */}
              <Card className="cs-card">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-sm font-bold text-white">
                      <Database className="h-4 w-4 text-indigo-400" aria-hidden="true" />
                      <span>
                        {result.exposure_count > 0
                          ? t.breaches.detectedTitle
                          : t.breaches.noBreachesTitle}
                      </span>
                    </div>
                    <span className="rounded bg-slate-800 px-2 py-0.5 text-xs text-slate-300 border border-slate-700">
                      {result.exposure_count} {isBn ? "টি রেকর্ড" : "Incident(s)"}
                    </span>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  {result.breaches.length === 0 ? (
                    <div className="flex items-center gap-3 rounded-lg border border-emerald-500/20 bg-emerald-950/20 p-4 text-xs text-emerald-200">
                      <CheckCircle2 className="h-5 w-5 shrink-0 text-emerald-400" />
                      <span>
                        {isBn
                          ? "আপনার ব্যবসা বা অ্যাকাউন্টের সাথে সম্পর্কিত কোনো তথ্য সাম্প্রতিক ফাঁস বা ডাম্পে পাওয়া যায়নি। অ্যাকাউন্ট নিরাপদ রাখতে টু-ফ্যাক্টর অথেনটিকেশন (2FA) চালু রাখুন।"
                          : "No public data breach records matched your inquiry. Keep Two-Factor Authentication active on all business accounts to remain protected."}
                      </span>
                    </div>
                  ) : (
                    result.breaches.map((b) => (
                      <div
                        key={b.id}
                        className="rounded-xl border border-slate-700/70 bg-slate-800/40 p-4 transition-colors hover:border-slate-600"
                      >
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <h3 className="text-sm font-bold text-white">{b.title}</h3>
                          <div className="flex items-center gap-2 text-xs">
                            <span className="font-mono text-slate-400">
                              {b.breach_date}
                            </span>
                            <span
                              className={cn(
                                "rounded px-1.5 py-0.5 text-[10px] font-bold uppercase",
                                b.severity === "critical"
                                  ? "bg-rose-500/15 text-rose-300 border border-rose-500/30"
                                  : "bg-amber-500/15 text-amber-300 border border-amber-500/30"
                              )}
                            >
                              {b.severity}
                            </span>
                          </div>
                        </div>
                        <p className="mt-1.5 text-xs text-slate-300 leading-relaxed">
                          {b.description}
                        </p>
                        <div className="mt-3 flex flex-wrap items-center gap-1.5 text-[11px] text-slate-400">
                          <span className="font-semibold text-slate-300">
                            {isBn ? "ফাঁস হওয়া ডাটা:" : "Exposed:"}
                          </span>
                          {b.data_classes.map((dc, idx) => (
                            <span
                              key={idx}
                              className="rounded bg-slate-900/80 px-2 py-0.5 text-slate-300"
                            >
                              {dc}
                            </span>
                          ))}
                          <span className="ml-auto font-mono text-[10px] text-slate-400">
                            ~{b.pwn_count.toLocaleString()} {isBn ? "অ্যাকাউন্ট" : "accounts"}
                          </span>
                        </div>
                      </div>
                    ))
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Right 1 Col: Actions & Emergency Reporting */}
            <div className="space-y-6">
              {/* Action Plan */}
              <Card className="cs-card">
                <CardHeader className="pb-3">
                  <div className="flex items-center gap-2 text-sm font-bold text-white">
                    <ShieldCheck className="h-4 w-4 text-emerald-400" aria-hidden="true" />
                    <span>{t.breaches.remediationTitle}</span>
                  </div>
                </CardHeader>
                <CardContent className="space-y-2.5">
                  {result.recommended_actions.map((act, idx) => (
                    <label
                      key={idx}
                      className="flex cursor-pointer items-start gap-2.5 rounded-lg border border-slate-800 bg-slate-900/50 p-2.5 text-xs text-slate-200 transition-colors hover:border-slate-700"
                    >
                      <input
                        type="checkbox"
                        checked={!!checkedActions[idx]}
                        onChange={() => toggleAction(idx)}
                        className="mt-0.5 h-4 w-4 rounded border-slate-700 text-cyan-500 focus:ring-cyan-400"
                      />
                      <span
                        className={
                          checkedActions[idx]
                            ? "text-slate-400 line-through"
                            : "text-slate-200"
                        }
                      >
                        {act}
                      </span>
                    </label>
                  ))}
                </CardContent>
              </Card>

              {/* India Helpline 1930 / CERT-In Reporting Box */}
              <Card className="cs-card border-amber-500/30 bg-amber-950/20">
                <CardHeader className="pb-2">
                  <div className="flex items-center gap-2 text-xs font-bold text-amber-300">
                    <PhoneCall className="h-4 w-4 text-amber-400" />
                    <span>
                      {isBn ? "আর্থিক ক্ষতির জরুরি হেল্পলাইন" : "National Cyber Helpline"}
                    </span>
                  </div>
                </CardHeader>
                <CardContent className="space-y-2 text-xs text-amber-100/90">
                  <p>
                    {isBn
                      ? "ফাঁস হওয়া তথ্যের মাধ্যমে যদি আপনার ব্যাংক বা UPI থেকে অননুমোদিত টাকা কেটে নেওয়া হয়, তবে গোল্ডেন আওয়ারের মধ্যে ১৯৩০ হেল্পলাইনে কল করুন।"
                      : "If compromised credentials lead to unauthorized banking or UPI fraud, immediately call 1930 within the golden hour to freeze payment gateways."}
                  </p>
                  <div className="pt-1">
                    <a
                      href="https://cybercrime.gov.in"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1 font-semibold text-amber-300 hover:underline"
                    >
                      <span>cybercrime.gov.in</span>
                      <ExternalLink className="h-3 w-3" />
                    </a>
                  </div>
                </CardContent>
              </Card>

              {/* Platform Transparency Notice */}
              <p className="text-[11px] text-slate-400 leading-relaxed">
                {t.breaches.disclaimer}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
