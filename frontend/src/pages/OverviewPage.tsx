import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Activity,
  AlertTriangle,
  ArrowUpRight,
  Calendar,
  CheckCircle2,
  ClipboardCheck,
  Download,
  FileBarChart2,
  FileWarning,
  Link2,
  MessageSquareWarning,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useLanguage } from "../i18n/LanguageContext";
import { apiRequest, downloadPdfReport } from "../lib/api";
import { formatTimestamp, getHealthScoreColor } from "../lib/utils";
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

interface DashboardOverview {
  business: {
    id: number;
    name: string;
    industry: string;
    city: string;
    is_demo_workspace: boolean;
  };
  is_empty: boolean;
  summary: {
    business_security_score: number | null;
    security_category: string;
    total_threat_analyses: number;
    high_risk_findings: number;
    completed_assessments: number;
    active_incidents: number;
    quizzes_completed: number;
  };
  score_trend: Array<{ label: string; score: number; category: string }>;
  risk_distribution: Array<{ name: string; count: number; color: string }>;
  recent_phishing: Array<{
    id: number;
    channel: string;
    excerpt: string;
    risk_score: number;
    risk_category: string;
    is_demo_sample: boolean;
    created_at: string;
  }>;
  recent_urls: Array<{
    id: number;
    url: string;
    host: string;
    risk_score: number;
    risk_category: string;
    is_demo_sample: boolean;
    created_at: string;
  }>;
  recommendations: Array<{
    source: string;
    priority: string;
    title: string;
    detail: string;
  }>;
  incident_activity: Array<{
    id: number;
    title: string;
    severity: string;
    status: string;
    completed_count: number;
    total_count: number;
    is_demo_sample: boolean;
    updated_at: string;
  }>;
  threat_vectors?: Array<{ channel?: string; name?: string; count: number }>;
  improvement_progress?: {
    assessment_score_delta: number;
    mfa_adoption_percent: number;
    controls_percent?: number;
    controls_completion_percent?: number;
    incident_resolution_percent?: number;
    incident_resolution_rate?: number;
  };
  subscription_usage?: {
    tier: string;
    monthly_scans_used?: number;
    monthly_scan_quota?: number;
    used_scans?: number;
    monthly_quota?: number;
  };
}

type DateWindow = "7" | "30" | "90" | "all";

export function OverviewPage() {
  const { language, t } = useLanguage();
  const navigate = useNavigate();
  const [data, setData] = useState<DashboardOverview | null>(null);
  const [daysWindow, setDaysWindow] = useState<DateWindow>("all");
  const [downloadingPdf, setDownloadingPdf] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    const daysParam = daysWindow === "all" ? "" : `&days=${daysWindow}`;
    apiRequest<DashboardOverview>(`/api/dashboard/overview?language=${language}${daysParam}`)
      .then((res) => {
        if (active) {
          setData(res);
          setError(null);
        }
      })
      .catch((err) => {
        if (active) setError(err.message || "Failed to load dashboard overview.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [language, daysWindow]);

  const handleDownloadMonthlyPdf = async () => {
    setDownloadingPdf(true);
    try {
      await downloadPdfReport(
        `/api/reports/monthly.pdf?language=${language}`,
        `cybershield-monthly-report-${language}.pdf`
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to download monthly report.");
    } finally {
      setDownloadingPdf(false);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[1, 2, 3, 4].map((k) => (
            <Skeleton key={k} className="h-28" />
          ))}
        </div>
        <div className="grid gap-6 lg:grid-cols-2">
          <Skeleton className="h-72" />
          <Skeleton className="h-72" />
        </div>
      </div>
    );
  }

  if (error || !data) {
    return <ErrorBanner message={error || "Dashboard unavailable."} />;
  }

  const scoreVal = data.summary.business_security_score;

  return (
    <div className="space-y-6">
      {/* Quick Actions & Filter Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="space-y-1">
          <p className="text-xs font-medium uppercase tracking-wider text-slate-400">
            {data.business.name} • {data.business.industry} ({data.business.city})
          </p>
          <div className="flex flex-wrap items-center gap-2">
            <span className="inline-flex items-center gap-1 text-[11px] text-slate-400">
              <Calendar className="h-3 w-3 text-[#06B6D4]" aria-hidden="true" />
              Window:
            </span>
            {(["7", "30", "90", "all"] as DateWindow[]).map((opt) => (
              <button
                key={opt}
                type="button"
                onClick={() => setDaysWindow(opt)}
                className={`rounded-md px-2 py-0.5 text-[11px] font-medium border transition-colors ${
                  daysWindow === opt
                    ? "border-indigo-500/60 bg-indigo-500/20 text-indigo-200"
                    : "border-slate-700/80 bg-[#141F35] text-slate-400 hover:text-slate-200"
                }`}
              >
                {opt === "all" ? "All Time" : `${opt}d`}
              </button>
            ))}
            {data.subscription_usage && (
              <span className="rounded-md border border-cyan-500/30 bg-cyan-500/10 px-2 py-0.5 text-[11px] font-medium text-cyan-200">
                {t.dashboard.planUsage}:{" "}
                {data.subscription_usage.monthly_scans_used ?? data.subscription_usage.used_scans ?? 0}/
                {data.subscription_usage.monthly_scan_quota ?? data.subscription_usage.monthly_quota ?? 50}
              </span>
            )}
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button size="sm" variant="secondary" onClick={handleDownloadMonthlyPdf} disabled={downloadingPdf}>
            <Download className="h-3.5 w-3.5 text-[#06B6D4]" aria-hidden="true" />
            <span>{downloadingPdf ? "..." : t.dashboard.monthlyReport}</span>
          </Button>
          <Button size="sm" onClick={() => navigate("/app/phishing")}>
            <MessageSquareWarning className="h-3.5 w-3.5" aria-hidden="true" />
            <span>{t.dashboard.analyzeMessage}</span>
          </Button>
          <Button size="sm" variant="danger" onClick={() => navigate("/app/incidents")}>
            <FileWarning className="h-3.5 w-3.5" aria-hidden="true" />
            <span>{t.dashboard.reportIncident}</span>
          </Button>
        </div>
      </div>

      {/* KPI Summary Cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="border-t-2 border-t-cyan-400/75">
          <CardContent>
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">{t.dashboard.securityScore}</span>
              <span className="rounded-lg bg-cyan-500/15 p-1.5 ring-1 ring-cyan-500/30">
                <ShieldCheck className="h-4 w-4 text-[#06B6D4]" aria-hidden="true" />
              </span>
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span
                className="text-3xl font-bold"
                style={{ color: getHealthScoreColor(scoreVal) }}
              >
                {scoreVal !== null ? `${scoreVal}%` : "—"}
              </span>
              <RiskBadge category={data.summary.security_category} />
            </div>
          </CardContent>
        </Card>

        <Card className="border-t-2 border-t-indigo-400/75">
          <CardContent>
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">{t.dashboard.totalAnalyses}</span>
              <span className="rounded-lg bg-indigo-500/15 p-1.5 ring-1 ring-indigo-500/30">
                <Activity className="h-4 w-4 text-[#6366F1]" aria-hidden="true" />
              </span>
            </div>
            <div className="mt-2 text-3xl font-bold text-slate-50">
              {data.summary.total_threat_analyses}
            </div>
            <p className="mt-1 text-xs text-slate-400">Phishing messages + URL scans</p>
          </CardContent>
        </Card>

        <Card className="border-t-2 border-t-red-400/75">
          <CardContent>
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">{t.dashboard.highRiskFindings}</span>
              <span className="rounded-lg bg-red-500/15 p-1.5 ring-1 ring-red-500/30">
                <AlertTriangle className="h-4 w-4 text-red-400" aria-hidden="true" />
              </span>
            </div>
            <div className="mt-2 text-3xl font-bold text-red-400">
              {data.summary.high_risk_findings}
            </div>
            <p className="mt-1 text-xs text-slate-400">High & Critical risk alerts</p>
          </CardContent>
        </Card>

        <Card className="border-t-2 border-t-emerald-400/75">
          <CardContent>
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-400">{t.dashboard.completedAssessments}</span>
              <span className="rounded-lg bg-emerald-500/15 p-1.5 ring-1 ring-emerald-500/30">
                <CheckCircle2 className="h-4 w-4 text-emerald-400" aria-hidden="true" />
              </span>
            </div>
            <div className="mt-2 text-3xl font-bold text-slate-50">
              {data.summary.completed_assessments}
            </div>
            <p className="mt-1 text-xs text-slate-400">
              {data.summary.active_incidents} active incident(s) • {data.summary.quizzes_completed} quiz(zes)
            </p>
          </CardContent>
        </Card>
      </div>

      {data.is_empty ? (
        <EmptyState
          title={t.dashboard.emptyTitle}
          description={t.dashboard.emptyDesc}
          action={
            <div className="flex flex-wrap justify-center gap-3">
              <Button onClick={() => navigate("/app/phishing")}>{t.dashboard.analyzeMessage}</Button>
              <Button variant="secondary" onClick={() => navigate("/app/assessment")}>
                {t.dashboard.startAssessment}
              </Button>
            </div>
          }
        />
      ) : (
        <>
          {/* Luminous Speedometer Health Gauge + Easy 3-Step Owner Quick-Start & Reports */}
          <div className="grid gap-6 lg:grid-cols-12">
            <Card className="lg:col-span-5">
              <CardHeader>
                <div>
                  <h2 className="text-sm font-semibold text-slate-100">
                    {language === "bn" ? "ব্যবসার সাইবার স্বাস্থ্য মিটার" : "Security Posture Gauge"}
                  </h2>
                  <p className="text-xs text-slate-400">
                    {language === "bn"
                      ? "চেকআপ স্কোর ও বর্তমান ঝুঁকির সংক্ষিপ্ত চিত্র"
                      : "Live overview of your business protection readiness"}
                  </p>
                </div>
                <RiskBadge category={data.summary.security_category} />
              </CardHeader>
              <CardContent className="flex flex-col items-center justify-center py-4">
                <svg viewBox="0 0 220 128" className="w-full max-w-[240px]" aria-label="Security Health Gauge">
                  <defs>
                    <linearGradient id="csGaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" stopColor="#6366F1" />
                      <stop offset="55%" stopColor="#06B6D4" />
                      <stop offset="100%" stopColor="#22C55E" />
                    </linearGradient>
                  </defs>
                  <path
                    d="M 24 106 A 86 86 0 0 1 196 106"
                    fill="none"
                    stroke="#1E293B"
                    strokeWidth="16"
                    strokeLinecap="round"
                  />
                  <path
                    d="M 24 106 A 86 86 0 0 1 196 106"
                    fill="none"
                    stroke="url(#csGaugeGrad)"
                    strokeWidth="16"
                    strokeLinecap="round"
                    strokeDasharray={`${Math.round(((Math.max(0, Math.min(100, scoreVal ?? 0)) / 100) * 270.18))} 270.18`}
                  />
                  <text
                    x="110"
                    y="88"
                    textAnchor="middle"
                    className="fill-slate-50 text-3xl font-bold"
                  >
                    {scoreVal !== null ? `${Math.round(scoreVal)}%` : "—"}
                  </text>
                  <text
                    x="110"
                    y="108"
                    textAnchor="middle"
                    className="fill-slate-400 text-[11px]"
                  >
                    {scoreVal !== null
                      ? data.summary.security_category
                      : language === "bn"
                      ? "এখনো চেকআপ হয়নি"
                      : "Checkup Pending"}
                  </text>
                </svg>
                <div className="mt-2 flex w-full items-center justify-between border-t border-slate-800/80 pt-3 text-xs text-slate-400">
                  <span>{language === "bn" ? "মোট স্ক্যান" : "Total Scans"}: <strong className="text-slate-100">{data.summary.total_threat_analyses}</strong></span>
                  <span>{language === "bn" ? "সক্রিয় ঘটনা" : "Open Incidents"}: <strong className="text-amber-300">{data.summary.active_incidents}</strong></span>
                </div>
              </CardContent>
            </Card>

            <Card className="lg:col-span-7">
              <CardHeader>
                <div>
                  <h2 className="text-sm font-semibold text-slate-100">
                    {language === "bn" ? "সহজ ৩ ধাপ ও দ্রুত PDF রিপোর্ট" : "Easy 3-Step Protection & Instant PDF Reports"}
                  </h2>
                  <p className="text-xs text-slate-400">
                    {language === "bn"
                      ? "কোনো টেকনিক্যাল জ্ঞান ছাড়াই ১ ক্লিকে যাচাই করুন ও রিপোর্ট ডাউনলোড করুন"
                      : "Verify suspicious messages or links safely, then export clear owner-friendly PDF reports"}
                  </p>
                </div>
                <Button variant="secondary" size="sm" onClick={() => navigate("/app/reports")}>
                  <FileBarChart2 className="h-3.5 w-3.5 text-cyan-300" aria-hidden="true" />
                  <span>{language === "bn" ? "সব রিপোর্ট" : "Reports Hub"}</span>
                </Button>
              </CardHeader>
              <CardContent className="grid gap-3 sm:grid-cols-3">
                <button
                  type="button"
                  onClick={() => navigate("/app/phishing")}
                  className="flex flex-col justify-between rounded-xl border border-slate-800 bg-[#0A1124]/80 p-3.5 text-left transition-all hover:border-indigo-500/50 hover:bg-[#131E3A]"
                >
                  <div className="flex items-center justify-between">
                    <span className="rounded-lg bg-indigo-500/15 p-2 text-indigo-300">
                      <MessageSquareWarning className="h-4 w-4" aria-hidden="true" />
                    </span>
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-indigo-300">Step 1</span>
                  </div>
                  <div className="mt-3">
                    <p className="text-xs font-semibold text-white">
                      {language === "bn" ? "মেসেজ / SMS যাচাই" : "Check SMS / Email"}
                    </p>
                    <p className="mt-0.5 text-[11px] text-slate-400">
                      {language === "bn" ? "প্রতারণা ও ভুয়া OTP ধরুন" : "Spot scams before staff click"}
                    </p>
                  </div>
                </button>

                <button
                  type="button"
                  onClick={() => navigate("/app/url-scanner")}
                  className="flex flex-col justify-between rounded-xl border border-slate-800 bg-[#0A1124]/80 p-3.5 text-left transition-all hover:border-cyan-500/50 hover:bg-[#131E3A]"
                >
                  <div className="flex items-center justify-between">
                    <span className="rounded-lg bg-cyan-500/15 p-2 text-cyan-300">
                      <Link2 className="h-4 w-4" aria-hidden="true" />
                    </span>
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-cyan-300">Step 2</span>
                  </div>
                  <div className="mt-3">
                    <p className="text-xs font-semibold text-white">
                      {language === "bn" ? "ওয়েবসাইট লিংক স্ক্যান" : "Scan Website Link"}
                    </p>
                    <p className="mt-0.5 text-[11px] text-slate-400">
                      {language === "bn" ? "SSL ও ডোমেইন নিরাপত্তা দেখুন" : "Verify SSL, DNS & phishing traps"}
                    </p>
                  </div>
                </button>

                <button
                  type="button"
                  onClick={() => navigate("/app/reports")}
                  className="flex flex-col justify-between rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-3.5 text-left transition-all hover:border-emerald-400/60 hover:bg-emerald-500/15"
                >
                  <div className="flex items-center justify-between">
                    <span className="rounded-lg bg-emerald-500/20 p-2 text-emerald-300">
                      <Download className="h-4 w-4" aria-hidden="true" />
                    </span>
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-emerald-300">Step 3</span>
                  </div>
                  <div className="mt-3">
                    <p className="text-xs font-semibold text-white">
                      {language === "bn" ? "সহজ PDF রিপোর্ট নিন" : "Export Easy PDFs"}
                    </p>
                    <p className="mt-0.5 text-[11px] text-emerald-200/80">
                      {language === "bn" ? "মাসিক, স্ক্যান ও ১৯৩০ রিপোর্ট" : "Monthly, scans & 1930 evidence"}
                    </p>
                  </div>
                </button>
              </CardContent>
            </Card>
          </div>

          {/* Charts Row */}
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <div>
                  <h2 className="text-sm font-semibold text-slate-100">Business Security Score History</h2>
                  <p className="text-xs text-slate-400">Recorded assessment posture over time</p>
                </div>
                <button
                  type="button"
                  onClick={() => navigate("/app/assessment")}
                  className="inline-flex items-center gap-1 text-xs font-medium text-[#06B6D4] hover:underline"
                >
                  <span>Assess</span>
                  <ArrowUpRight className="h-3.5 w-3.5" aria-hidden="true" />
                </button>
              </CardHeader>
              <CardContent className="h-64">
                {data.score_trend.length === 0 ? (
                  <div className="flex h-full items-center justify-center text-xs text-slate-400">
                    Complete your first Business Security Assessment to plot score history.
                  </div>
                ) : (
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data.score_trend}>
                      <defs>
                        <linearGradient id="scoreFill" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#06B6D4" stopOpacity={0.35} />
                          <stop offset="95%" stopColor="#06B6D4" stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                      <XAxis dataKey="label" stroke="#94A3B8" fontSize={11} />
                      <YAxis domain={[0, 100]} stroke="#94A3B8" fontSize={11} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "#10182B",
                          borderColor: "#334155",
                          borderRadius: "8px",
                          fontSize: "12px",
                        }}
                      />
                      <Area
                        type="monotone"
                        dataKey="score"
                        stroke="#06B6D4"
                        strokeWidth={2}
                        fill="url(#scoreFill)"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div>
                  <h2 className="text-sm font-semibold text-slate-100">Threat Risk Distribution</h2>
                  <p className="text-xs text-slate-400">Message & URL findings across risk bands</p>
                </div>
                <button
                  type="button"
                  onClick={() => navigate("/app/history")}
                  className="inline-flex items-center gap-1 text-xs font-medium text-[#06B6D4] hover:underline"
                >
                  <span>View History</span>
                  <ArrowUpRight className="h-3.5 w-3.5" aria-hidden="true" />
                </button>
              </CardHeader>
              <CardContent className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={data.risk_distribution}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                    <XAxis dataKey="name" stroke="#94A3B8" fontSize={11} />
                    <YAxis allowDecimals={false} stroke="#94A3B8" fontSize={11} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "#10182B",
                        borderColor: "#334155",
                        borderRadius: "8px",
                        fontSize: "12px",
                      }}
                    />
                    <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                      {data.risk_distribution.map((entry) => (
                        <Cell key={entry.name} fill={entry.color} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Security Improvement Progress & Threat Vectors */}
          {(data.improvement_progress || (data.threat_vectors && data.threat_vectors.length > 0)) && (
            <div className="grid gap-6 lg:grid-cols-2">
              {data.improvement_progress && (
                <Card>
                  <CardHeader>
                    <div className="flex items-center gap-2">
                      <TrendingUp className="h-4 w-4 text-emerald-400" aria-hidden="true" />
                      <h2 className="text-sm font-semibold text-slate-100">{t.dashboard.improvementTitle}</h2>
                    </div>
                    <button
                      type="button"
                      onClick={() => navigate("/app/governance")}
                      className="inline-flex items-center gap-1 text-xs font-medium text-[#06B6D4] hover:underline"
                    >
                      <span>Manage Team & Controls</span>
                      <ArrowUpRight className="h-3.5 w-3.5" aria-hidden="true" />
                    </button>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {[
                      {
                        label: "Staff MFA Adoption",
                        val: data.improvement_progress.mfa_adoption_percent,
                        color: "bg-cyan-500",
                      },
                      {
                        label: "Governance Checklists (Backup/Updates/Policy)",
                        val:
                          data.improvement_progress.controls_percent ??
                          data.improvement_progress.controls_completion_percent ??
                          0,
                        color: "bg-indigo-500",
                      },
                      {
                        label: "Incident Containment & Resolution Rate",
                        val:
                          data.improvement_progress.incident_resolution_percent ??
                          data.improvement_progress.incident_resolution_rate ??
                          0,
                        color: "bg-emerald-500",
                      },
                    ].map((row) => (
                      <div key={row.label} className="space-y-1">
                        <div className="flex items-center justify-between text-xs">
                          <span className="text-slate-300">{row.label}</span>
                          <span className="font-semibold text-slate-100">{row.val}%</span>
                        </div>
                        <div className="h-2 overflow-hidden rounded-full bg-[#080D1B] border border-slate-800">
                          <div
                            className={`h-full rounded-full ${row.color} transition-all duration-300`}
                            style={{ width: `${Math.min(100, Math.max(0, row.val))}%` }}
                          />
                        </div>
                      </div>
                    ))}
                    <div className="rounded-lg border border-slate-800 bg-[#080D1B]/70 px-3 py-2 text-xs flex items-center justify-between">
                      <span className="text-slate-400">Assessment Score Change vs Previous</span>
                      <span
                        className={`font-semibold ${
                          data.improvement_progress.assessment_score_delta >= 0
                            ? "text-emerald-400"
                            : "text-red-400"
                        }`}
                      >
                        {data.improvement_progress.assessment_score_delta >= 0 ? "+" : ""}
                        {data.improvement_progress.assessment_score_delta} pts
                      </span>
                    </div>
                  </CardContent>
                </Card>
              )}

              {data.threat_vectors && (
                <Card>
                  <CardHeader>
                    <h2 className="text-sm font-semibold text-slate-100">{t.dashboard.vectorBreakdown}</h2>
                    <span className="text-[11px] text-slate-400">Logged channels in selected window</span>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {data.threat_vectors.length === 0 ? (
                      <p className="text-xs text-slate-400">No scans recorded in this time window.</p>
                    ) : (
                      data.threat_vectors.map((vec, idx) => {
                        const label = vec.channel || vec.name || `Vector ${idx + 1}`;
                        const maxCount = Math.max(...data.threat_vectors!.map((v) => v.count), 1);
                        const pct = Math.round((vec.count / maxCount) * 100);
                        return (
                          <div key={`${label}-${idx}`} className="space-y-1">
                            <div className="flex items-center justify-between text-xs">
                              <span className="text-slate-200 font-medium">{label}</span>
                              <span className="font-semibold text-cyan-300">{vec.count}</span>
                            </div>
                            <div className="h-2 overflow-hidden rounded-full bg-[#080D1B] border border-slate-800">
                              <div
                                className="h-full rounded-full bg-gradient-to-r from-[#6366F1] to-[#06B6D4]"
                                style={{ width: `${pct}%` }}
                              />
                            </div>
                          </div>
                        );
                      })
                    )}
                  </CardContent>
                </Card>
              )}
            </div>
          )}

          {/* Recommendations & Incident Activity */}
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <h2 className="text-sm font-semibold text-slate-100">Prioritized Security Recommendations</h2>
              </CardHeader>
              <CardContent className="space-y-3">
                {data.recommendations.map((rec, idx) => (
                  <div
                    key={idx}
                    className="rounded-lg border border-slate-800 bg-[#10182B] p-3.5"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-xs font-semibold text-slate-100">{rec.title}</span>
                      <RiskBadge category={rec.priority} />
                    </div>
                    <p className="mt-1.5 text-xs leading-relaxed text-slate-400">{rec.detail}</p>
                  </div>
                ))}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <h2 className="text-sm font-semibold text-slate-100">Incident Response Activity</h2>
                <button
                  type="button"
                  onClick={() => navigate("/app/incidents")}
                  className="text-xs font-medium text-[#06B6D4] hover:underline"
                >
                  Open Center
                </button>
              </CardHeader>
              <CardContent>
                {data.incident_activity.length === 0 ? (
                  <p className="text-xs text-slate-400">No incident playbooks opened yet.</p>
                ) : (
                  <div className="space-y-3">
                    {data.incident_activity.map((inc) => (
                      <button
                        key={inc.id}
                        type="button"
                        onClick={() => navigate("/app/incidents")}
                        className="w-full rounded-lg border border-slate-800 bg-[#10182B] p-3.5 text-left hover:border-slate-700"
                      >
                        <div className="flex items-center justify-between gap-2">
                          <span className="text-xs font-semibold text-slate-100">{inc.title}</span>
                          <RiskBadge category={inc.severity} />
                        </div>
                        <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
                          <span>
                            {inc.completed_count}/{inc.total_count} actions completed
                          </span>
                          <span>{formatTimestamp(inc.updated_at)}</span>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Recent Phishing & URL Scans */}
          <div className="grid gap-6 lg:grid-cols-2">
            <Card>
              <CardHeader>
                <h2 className="text-sm font-semibold text-slate-100">Recent Phishing Analyses</h2>
                <button
                  type="button"
                  onClick={() => navigate("/app/phishing")}
                  className="text-xs font-medium text-[#06B6D4] hover:underline"
                >
                  New Scan
                </button>
              </CardHeader>
              <CardContent>
                {data.recent_phishing.length === 0 ? (
                  <p className="text-xs text-slate-400">No message scans recorded yet.</p>
                ) : (
                  <div className="space-y-2.5">
                    {data.recent_phishing.map((p) => (
                      <button
                        key={p.id}
                        type="button"
                        onClick={() => navigate(`/app/phishing?id=${p.id}`)}
                        className="w-full rounded-lg border border-slate-800 bg-[#10182B] p-3 text-left transition-colors hover:border-[#6366F1]"
                      >
                        <div className="flex items-center justify-between gap-2">
                          <span className="font-mono text-[11px] uppercase text-[#06B6D4]">
                            {p.channel} {p.is_demo_sample ? "• DEMO SAMPLE" : ""}
                          </span>
                          <RiskBadge category={`${p.risk_score}/100 • ${p.risk_category}`} />
                        </div>
                        <p className="mt-1.5 line-clamp-2 text-xs text-slate-300">{p.excerpt}</p>
                      </button>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <h2 className="text-sm font-semibold text-slate-100">Recent URL Scans</h2>
                <button
                  type="button"
                  onClick={() => navigate("/app/url-scanner")}
                  className="text-xs font-medium text-[#06B6D4] hover:underline"
                >
                  New Scan
                </button>
              </CardHeader>
              <CardContent>
                {data.recent_urls.length === 0 ? (
                  <p className="text-xs text-slate-400">No URL scans recorded yet.</p>
                ) : (
                  <div className="space-y-2.5">
                    {data.recent_urls.map((u) => (
                      <button
                        key={u.id}
                        type="button"
                        onClick={() => navigate(`/app/url-scanner?id=${u.id}`)}
                        className="w-full rounded-lg border border-slate-800 bg-[#10182B] p-3 text-left transition-colors hover:border-[#06B6D4]"
                      >
                        <div className="flex items-center justify-between gap-2">
                          <span className="truncate font-mono text-xs text-slate-200">{u.host}</span>
                          <RiskBadge category={`${u.risk_score}/100 • ${u.risk_category}`} />
                        </div>
                        <p className="mt-1 truncate text-[11px] text-slate-400">{u.url}</p>
                      </button>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </>
      )}
    </div>
  );
}

