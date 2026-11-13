import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  CheckCircle2,
  ClipboardCheck,
  Download,
  ExternalLink,
  FileBarChart2,
  FileWarning,
  Link2,
  MessageSquareWarning,
  RefreshCw,
  ShieldCheck,
} from "lucide-react";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  EmptyState,
  ErrorBanner,
  RiskBadge,
  Skeleton,
} from "../components/ui/Primitives";
import { useLanguage } from "../i18n/LanguageContext";
import { apiRequest, downloadPdfReport } from "../lib/api";
import { formatTimestamp } from "../lib/utils";

type ReportItemType = "phishing" | "url" | "assessment" | "incident";
type FilterType = "all" | ReportItemType;

interface UnifiedReportItem {
  uid: string;
  record_id: number;
  type: ReportItemType;
  title: string;
  target: string;
  score: number;
  status_label: string;
  is_demo_sample: boolean;
  created_at: string;
  pdf_url: string;
}

interface DashboardSnapshot {
  summary?: {
    business_security_score?: number | null;
    security_category?: string;
    total_threat_analyses?: number;
    high_risk_findings?: number;
    completed_assessments?: number;
    active_incidents?: number;
  };
  improvement_progress?: {
    mfa_adoption_percent?: number;
    controls_percent?: number;
    incident_resolution_percent?: number;
  };
  business?: {
    name?: string;
    industry?: string;
    city?: string;
  };
}

const REPORT_FILTER_OPTIONS: Array<{ value: FilterType; en: string; bn: string }> = [
  { value: "all", en: "All Reports", bn: "সব রিপোর্ট" },
  { value: "phishing", en: "Phishing PDFs", bn: "ফিশিং রিপোর্ট" },
  { value: "url", en: "Website & URL PDFs", bn: "ওয়েবসাইট রিপোর্ট" },
  { value: "assessment", en: "Security Assessments", bn: "সিকিউরিটি চেকআপ" },
  { value: "incident", en: "Incident Reports", bn: "ঘটনা রিপোর্ট" },
];

export function ReportsPage() {
  const { language } = useLanguage();
  const isBn = language === "bn";
  const navigate = useNavigate();

  const [snapshot, setSnapshot] = useState<DashboardSnapshot | null>(null);
  const [items, setItems] = useState<UnifiedReportItem[]>([]);
  const [filter, setFilter] = useState<FilterType>("all");
  const [selectedIds, setSelectedIds] = useState<Partial<Record<ReportItemType, number>>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [downloadingKey, setDownloadingKey] = useState<string | null>(null);
  const [successNotice, setSuccessNotice] = useState<string | null>(null);

  const loadReportsData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [overviewRes, unifiedRes] = await Promise.all([
        apiRequest<DashboardSnapshot>(`/dashboard/overview?language=${language}`),
        apiRequest<{ items?: UnifiedReportItem[] }>("/history/unified"),
      ]);
      setSnapshot(overviewRes || {});
      const list = Array.isArray(unifiedRes?.items) ? unifiedRes.items : [];
      setItems(list);
      setSelectedIds((prev) => {
        const next: Partial<Record<ReportItemType, number>> = { ...prev };
        for (const kind of ["phishing", "url", "assessment", "incident"] as ReportItemType[]) {
          const matches = list.filter((i) => i.type === kind);
          if (matches.length > 0 && (!next[kind] || !matches.some((m) => m.record_id === next[kind]))) {
            next[kind] = matches[0].record_id;
          }
        }
        return next;
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load security reports.");
    } finally {
      setLoading(false);
    }
  }, [language]);

  useEffect(() => {
    void loadReportsData();
  }, [loadReportsData]);

  const handleDownload = async (key: string, pdfUrl: string, filename: string, label: string) => {
    setDownloadingKey(key);
    setError(null);
    setSuccessNotice(null);
    try {
      const urlWithLang = pdfUrl.includes("language=")
        ? pdfUrl
        : `${pdfUrl}${pdfUrl.includes("?") ? "&" : "?"}language=${language}`;
      await downloadPdfReport(urlWithLang, filename);
      setSuccessNotice(
        isBn
          ? `ডাউনলোড শুরু হয়েছে: ${label}`
          : `PDF download ready: ${label}`
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to download PDF report.");
    } finally {
      setDownloadingKey(null);
    }
  };

  const itemsByType = useMemo(() => {
    return {
      phishing: items.filter((i) => i.type === "phishing"),
      url: items.filter((i) => i.type === "url"),
      assessment: items.filter((i) => i.type === "assessment"),
      incident: items.filter((i) => i.type === "incident"),
    };
  }, [items]);

  const filteredItems = useMemo(() => {
    if (filter === "all") return items;
    return items.filter((i) => i.type === filter);
  }, [filter, items]);

  const getSelectedItem = (kind: ReportItemType): UnifiedReportItem | undefined => {
    const list = itemsByType[kind];
    if (list.length === 0) return undefined;
    const chosenId = selectedIds[kind];
    return list.find((i) => i.record_id === chosenId) || list[0];
  };

  const openFeatureRoute = (type: ReportItemType) => {
    if (type === "phishing") navigate("/app/phishing");
    else if (type === "url") navigate("/app/url-scanner");
    else if (type === "assessment") navigate("/app/assessment");
    else navigate("/app/incidents");
  };

  const scoreValue = snapshot?.summary?.business_security_score;
  const scoreDisplay =
    typeof scoreValue === "number" ? `${Math.round(scoreValue)}/100` : isBn ? "মূল্যায়ন বাকি" : "Not Checked Yet";
  const mfaDisplay =
    typeof snapshot?.improvement_progress?.mfa_adoption_percent === "number"
      ? `${snapshot.improvement_progress.mfa_adoption_percent}%`
      : "0%";
  const totalScansDisplay = snapshot?.summary?.total_threat_analyses ?? items.length;

  const categoryCards: Array<{
    kind: ReportItemType;
    title: string;
    subtitle: string;
    filenamePrefix: string;
    emptyActionLabel: string;
    icon: typeof MessageSquareWarning;
    accent: string;
  }> = [
    {
      kind: "phishing",
      title: isBn ? "ফিশিং ও প্রতারণা রিপোর্ট (PDF)" : "Phishing & Scam Analysis Report",
      subtitle: isBn
        ? "সন্দেহজনক SMS, WhatsApp বা ইমেইলের AI বিশ্লেষণ ও প্রমাণ ডাউনলোড করুন।"
        : "Download AI scam verdicts, suspicious triggers, and staff safety notes.",
      filenamePrefix: "phishing-report",
      emptyActionLabel: isBn ? "প্রথম মেসেজ যাচাই করুন" : "Check a Message First",
      icon: MessageSquareWarning,
      accent: "border-t-indigo-400/70",
    },
    {
      kind: "url",
      title: isBn ? "ওয়েবসাইট ও লিংক ঝুঁকি রিপোর্ট (PDF)" : "Website & Link Safety Report",
      subtitle: isBn
        ? "ওয়েবসাইটের SSL, DNS (SPF/DMARC) এবং ঝুঁকির সম্পূর্ণ রিপোর্ট নিন।"
        : "Print domain risk scores, SSL certificate status, and DNS checks.",
      filenamePrefix: "url-safety-report",
      emptyActionLabel: isBn ? "একটি লিংক স্ক্যান করুন" : "Scan a Website Link",
      icon: Link2,
      accent: "border-t-cyan-400/70",
    },
    {
      kind: "assessment",
      title: isBn ? "ব্যবসায়িক নিরাপত্তা চেকআপ রিপোর্ট (PDF)" : "Business Security Assessment Report",
      subtitle: isBn
        ? "আপনার দোকানের বা অফিসের পাসওয়ার্ড, ব্যাকআপ ও MFA স্কোর রিপোর্ট।"
        : "Shareable security score breakdown and practical improvement steps.",
      filenamePrefix: "security-assessment",
      emptyActionLabel: isBn ? "নিরাপত্তা চেকআপ শুরু করুন" : "Run Security Checkup",
      icon: ClipboardCheck,
      accent: "border-t-emerald-400/70",
    },
    {
      kind: "incident",
      title: isBn ? "সাইবার ঘটনা ও 1930 রিপোর্ট (PDF)" : "Incident & 1930 Escalation Report",
      subtitle: isBn
        ? "ব্যাংক, পুলিশ বা ১৯৩০ সাইবার হেল্পলাইনে জমা দেওয়ার উপযোগী রিপোর্ট।"
        : "Ready-to-share incident timeline, checklist, and 1930 escalation evidence.",
      filenamePrefix: "incident-report",
      emptyActionLabel: isBn ? "নতুন ঘটনা রিপোর্ট করুন" : "Log an Incident",
      icon: FileWarning,
      accent: "border-t-amber-400/70",
    },
  ];

  return (
    <div className="min-w-0 space-y-6">
      {/* Header */}
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full border border-cyan-500/30 bg-cyan-500/10 px-3 py-1 text-[11px] font-medium text-cyan-300">
            <FileBarChart2 className="h-3.5 w-3.5" />
            {isBn ? "১-ক্লিকে সব নিরাপত্তা রিপোর্ট" : "1-Click Printable PDF Reports"}
          </div>
          <h1 className="mt-2 text-2xl font-bold tracking-tight text-white">
            {isBn ? "সহজ রিপোর্ট সেন্টার (PDF)" : "Easy Security Reports Center"}
          </h1>
          <p className="mt-1 text-sm text-slate-400">
            {isBn
              ? "ম্যানেজার, ব্যাংক বা ১৯৩০ হেল্পলাইনের সাথে শেয়ার করার জন্য সব নিরাপত্তা রিপোর্ট এক জায়গায় পান।"
              : "Download clean, plain-language PDF reports for your team, partners, or 1930 cyber helpline from one place."}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Button variant="secondary" size="sm" onClick={() => void loadReportsData()} disabled={loading}>
            <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} />
            {isBn ? "রিফ্রেশ" : "Refresh"}
          </Button>
          <Button
            size="sm"
            disabled={downloadingKey === "monthly"}
            onClick={() =>
              void handleDownload(
                "monthly",
                `/api/reports/monthly.pdf?language=${language}`,
                `cybershield-monthly-report-${language}.pdf`,
                isBn ? "মাসিক নিরাপত্তা রিপোর্ট" : "Monthly Security Report"
              )
            }
          >
            <Download className="h-4 w-4" />
            {downloadingKey === "monthly"
              ? isBn
                ? "ডাউনলোড হচ্ছে..."
                : "Preparing PDF..."
              : isBn
              ? "মাসিক রিপোর্ট (PDF)"
              : "Download Monthly Report (PDF)"}
          </Button>
        </div>
      </div>

      {error && <ErrorBanner message={error} />}

      {successNotice && (
        <div className="flex items-center gap-2.5 rounded-xl border border-emerald-500/35 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">
          <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" />
          <span>{successNotice}</span>
        </div>
      )}

      {/* Featured Monthly Executive Report Card */}
      <Card className="border-indigo-500/35 bg-gradient-to-r from-indigo-950/50 via-[#111C38]/95 to-cyan-950/40">
        <CardContent className="flex flex-col justify-between gap-5 py-6 lg:flex-row lg:items-center">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <span className="rounded-lg bg-indigo-500/20 p-2 text-indigo-300 ring-1 ring-indigo-500/35">
                <ShieldCheck className="h-5 w-5" />
              </span>
              <div>
                <h2 className="text-lg font-semibold text-white">
                  {isBn ? "মাসিক বিজনেস সিকিউরিটি রিপোর্ট (সম্পূর্ণ সারাংশ)" : "Monthly Executive Business Security Report"}
                </h2>
                <p className="text-xs text-slate-400">
                  {snapshot?.business?.name
                    ? `${snapshot.business.name}${snapshot.business.city ? ` • ${snapshot.business.city}` : ""}`
                    : isBn
                    ? "আপনার ব্যবসার সম্পূর্ণ মাসের নিরাপত্তা বিশ্লেষণ"
                    : "Complete monthly summary of threats blocked, hygiene score, and next steps"}
                </p>
              </div>
            </div>
            <div className="flex flex-wrap gap-3 pt-1 text-xs">
              <span className="rounded-lg border border-slate-700/80 bg-[#0A1124]/80 px-3 py-1.5 text-slate-300">
                {isBn ? "নিরাপত্তা স্কোর:" : "Security Score:"}{" "}
                <strong className="text-cyan-300">{scoreDisplay}</strong>
              </span>
              <span className="rounded-lg border border-slate-700/80 bg-[#0A1124]/80 px-3 py-1.5 text-slate-300">
                {isBn ? "মোট স্ক্যান:" : "Total Scans:"}{" "}
                <strong className="text-white">{totalScansDisplay}</strong>
              </span>
              <span className="rounded-lg border border-slate-700/80 bg-[#0A1124]/80 px-3 py-1.5 text-slate-300">
                {isBn ? "২-স্তর সুরক্ষা (MFA):" : "MFA Adoption:"}{" "}
                <strong className="text-emerald-300">{mfaDisplay}</strong>
              </span>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2.5">
            <Button
              size="lg"
              disabled={downloadingKey === "monthly-hero"}
              onClick={() =>
                void handleDownload(
                  "monthly-hero",
                  `/api/reports/monthly.pdf?language=${language}`,
                  `cybershield-monthly-report-${language}.pdf`,
                  isBn ? "মাসিক নিরাপত্তা রিপোর্ট" : "Monthly Security Report"
                )
              }
            >
              <Download className="h-4 w-4" />
              {downloadingKey === "monthly-hero"
                ? isBn
                  ? "ডাউনলোড হচ্ছে..."
                  : "Preparing PDF..."
                : isBn
                ? "সম্পূর্ণ মাসিক PDF ডাউনলোড"
                : "Download Full Monthly PDF"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* 4 Specific Category Report Cards */}
      {loading ? (
        <div className="grid min-w-0 gap-4 md:grid-cols-2">
          {Array.from({ length: 4 }).map((_, idx) => (
            <Skeleton key={idx} className="h-44 w-full" />
          ))}
        </div>
      ) : (
        <div className="grid min-w-0 gap-4 md:grid-cols-2">
          {categoryCards.map((card) => {
            const Icon = card.icon;
            const list = itemsByType[card.kind];
            const selected = getSelectedItem(card.kind);
            return (
              <Card key={card.kind} className={`min-w-0 overflow-hidden border-t-2 ${card.accent}`}>
                <CardContent className="flex h-full min-w-0 flex-col justify-between gap-4 py-5">
                  <div className="min-w-0 space-y-3">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex min-w-0 items-start gap-3">
                        <div className="shrink-0 rounded-xl bg-slate-800/90 p-2.5 text-cyan-300 ring-1 ring-slate-700">
                          <Icon className="h-5 w-5" />
                        </div>
                        <div className="min-w-0">
                          <h3 className="text-base font-semibold text-white">{card.title}</h3>
                          <p className="mt-0.5 text-xs leading-relaxed text-slate-400">{card.subtitle}</p>
                        </div>
                      </div>
                      <span className="shrink-0 rounded-full border border-slate-700 bg-slate-900/90 px-2.5 py-0.5 text-[11px] font-medium text-slate-300">
                        {list.length} {isBn ? "টি" : list.length === 1 ? "ready" : "ready"}
                      </span>
                    </div>

                    {list.length > 0 && selected ? (
                      <div className="min-w-0 space-y-2 rounded-xl border border-slate-800 bg-[#090F20]/80 p-3">
                        <label
                          htmlFor={`select-${card.kind}`}
                          className="block text-[11px] font-medium text-slate-400"
                        >
                          {isBn ? "রিপোর্ট বেছে নিন:" : "Select record to export:"}
                        </label>
                        <select
                          id={`select-${card.kind}`}
                          value={selected.record_id}
                          onChange={(e) =>
                            setSelectedIds((prev) => ({
                              ...prev,
                              [card.kind]: Number(e.target.value),
                            }))
                          }
                          className="w-full max-w-full truncate rounded-lg border border-slate-700 bg-[#0F172A] px-2.5 py-2 text-xs text-slate-100 focus:border-cyan-500 focus:outline-none"
                        >
                          {list.map((opt) => (
                            <option key={opt.uid} value={opt.record_id}>
                              {opt.title.length > 42 ? `${opt.title.slice(0, 42)}...` : opt.title} ({opt.score}/100) — {opt.status_label}
                            </option>
                          ))}
                        </select>
                        <div className="flex min-w-0 items-center justify-between gap-2 text-[11px] text-slate-400">
                          <span className="min-w-0 flex-1 truncate">{selected.target}</span>
                          <RiskBadge category={selected.status_label} />
                        </div>
                      </div>
                    ) : (
                      <div className="rounded-xl border border-dashed border-slate-800 bg-[#090F20]/50 p-3 text-xs text-slate-400">
                        {isBn
                          ? "এই বিভাগে এখনো কোনো স্ক্যান করা হয়নি। নিচের বাটনে ক্লিক করে প্রথম রিপোর্ট তৈরি করুন।"
                          : "No saved scan in this category yet. Run one quick check to generate your PDF report."}
                      </div>
                    )}
                  </div>

                  <div className="flex flex-wrap items-center justify-between gap-2 pt-1">
                    {selected ? (
                      <>
                        <Button
                          size="sm"
                          disabled={downloadingKey === `card-${card.kind}`}
                          onClick={() =>
                            void handleDownload(
                              `card-${card.kind}`,
                              selected.pdf_url,
                              `${card.filenamePrefix}-${selected.record_id}.pdf`,
                              selected.title
                            )
                          }
                        >
                          <Download className="h-3.5 w-3.5" />
                          {downloadingKey === `card-${card.kind}`
                            ? "..."
                            : isBn
                            ? "PDF ডাউনলোড"
                            : "Download PDF"}
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => openFeatureRoute(card.kind)}
                        >
                          <ExternalLink className="h-3.5 w-3.5" />
                          {isBn ? "নতুন স্ক্যান করুন" : "Run New Check"}
                        </Button>
                      </>
                    ) : (
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => openFeatureRoute(card.kind)}
                      >
                        <ExternalLink className="h-3.5 w-3.5" />
                        {card.emptyActionLabel}
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      {/* All Individual Printable Reports Table */}
      <Card className="min-w-0 overflow-hidden">
        <CardHeader className="flex-wrap">
          <div>
            <h2 className="text-base font-semibold text-white">
              {isBn ? "সব সংরক্ষিত রিপোর্টের তালিকা" : "All Individual Printable Reports"}
            </h2>
            <p className="text-xs text-slate-400">
              {isBn
                ? "যে কোনো পুরনো স্ক্যান বা ঘটনার PDF ১ ক্লিকে ডাউনলোড করুন"
                : "Every phishing scan, URL check, assessment, and incident ready for instant PDF export"}
            </p>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {REPORT_FILTER_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                type="button"
                onClick={() => setFilter(opt.value)}
                className={`rounded-lg px-2.5 py-1 text-xs font-medium transition-colors ${
                  filter === opt.value
                    ? "bg-cyan-500/20 text-cyan-300 ring-1 ring-cyan-500/40"
                    : "bg-slate-800/80 text-slate-400 hover:text-slate-200"
                }`}
              >
                {isBn ? opt.bn : opt.en}
              </button>
            ))}
          </div>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="space-y-2">
              {Array.from({ length: 4 }).map((_, idx) => (
                <Skeleton key={idx} className="h-12 w-full" />
              ))}
            </div>
          ) : filteredItems.length === 0 ? (
            <EmptyState
              title={isBn ? "কোনো রিপোর্ট পাওয়া যায়নি" : "No individual reports yet"}
              description={
                isBn
                  ? "ফিশিং যাচাই, লিংক স্ক্যান বা সিকিউরিটি চেকআপ করলেই এখানে PDF তৈরি হয়ে যাবে।"
                  : "Run a Phishing check, URL scan, or Security Checkup and your printable PDFs will appear right here."
              }
              action={
                <Button size="sm" onClick={() => navigate("/app/phishing")}>
                  {isBn ? "প্রথম স্ক্যান শুরু করুন" : "Start First Check"}
                </Button>
              }
            />
          ) : (
            <div className="w-full max-w-full overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-800 text-xs uppercase text-slate-400">
                    <th className="py-2.5 pr-4">{isBn ? "ধরন" : "Report Type"}</th>
                    <th className="py-2.5 pr-4">{isBn ? "শিরোনাম ও বিবরণ" : "Summary"}</th>
                    <th className="py-2.5 pr-4">{isBn ? "স্কোর" : "Score"}</th>
                    <th className="py-2.5 pr-4">{isBn ? "অবস্থা" : "Status"}</th>
                    <th className="py-2.5 pr-4">{isBn ? "তারিখ" : "Date"}</th>
                    <th className="py-2.5 text-right">{isBn ? "ডাউনলোড" : "PDF Export"}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/70">
                  {filteredItems.map((item) => (
                    <tr key={item.uid} className="hover:bg-slate-800/35">
                      <td className="py-3 pr-4">
                        <span className="rounded-md border border-slate-700 bg-slate-900/90 px-2 py-0.5 text-[11px] font-medium uppercase text-slate-300">
                          {item.type}
                        </span>
                      </td>
                      <td className="max-w-xs py-3 pr-4">
                        <p className="truncate font-medium text-slate-100">{item.title}</p>
                        <p className="truncate text-xs text-slate-400">{item.target}</p>
                      </td>
                      <td className="py-3 pr-4 font-mono text-xs text-slate-200">{item.score}/100</td>
                      <td className="py-3 pr-4">
                        <RiskBadge category={item.status_label} />
                      </td>
                      <td className="whitespace-nowrap py-3 pr-4 text-xs text-slate-400">
                        {formatTimestamp(item.created_at)}
                      </td>
                      <td className="py-3 text-right">
                        <div className="inline-flex items-center gap-1.5">
                          <Button
                            variant="secondary"
                            size="sm"
                            disabled={downloadingKey === item.uid}
                            onClick={() =>
                              void handleDownload(
                                item.uid,
                                item.pdf_url,
                                `${item.type}-report-${item.record_id}.pdf`,
                                item.title
                              )
                            }
                          >
                            <Download className="h-3.5 w-3.5" />
                            <span>{downloadingKey === item.uid ? "..." : isBn ? "PDF নিন" : "PDF"}</span>
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
