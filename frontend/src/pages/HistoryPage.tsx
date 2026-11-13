import { useCallback, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Download, ExternalLink, FileBarChart2, Search, Trash2 } from "lucide-react";
import { useLanguage } from "../i18n/LanguageContext";
import { apiRequest, ApiError, downloadPdfReport } from "../lib/api";
import { formatTimestamp } from "../lib/utils";
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

interface HistoryItem {
  uid: string;
  record_id: number;
  type: "phishing" | "url" | "assessment" | "incident";
  title: string;
  target: string;
  score: number;
  status_label: string;
  is_demo_sample: boolean;
  created_at: string;
  pdf_url: string;
}

interface AuditItem {
  id: number;
  action: string;
  resource_type: string;
  summary: string;
  created_at: string;
}

export function HistoryPage() {
  const navigate = useNavigate();
  const { language, t } = useLanguage();
  const [tab, setTab] = useState<"scans" | "audit">("scans");
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [auditLogs, setAuditLogs] = useState<AuditItem[]>([]);
  const [filterType, setFilterType] = useState<string>("all");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadHistory = useCallback(() => {
    setLoading(true);
    Promise.all([
      apiRequest<{ items: HistoryItem[] }>("/api/history/unified"),
      apiRequest<{ logs: AuditItem[] }>("/api/history/audit-logs"),
    ])
      .then(([u, a]) => {
        setItems(u.items);
        setAuditLogs(a.logs);
        setError(null);
      })
      .catch((err) => setError(err.message || "Failed to load scan history."))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const filteredItems = useMemo(() => {
    const q = search.trim().toLowerCase();
    return items.filter((item) => {
      if (filterType !== "all" && item.type !== filterType) return false;
      if (!q) return true;
      return (
        item.title.toLowerCase().includes(q) ||
        item.target.toLowerCase().includes(q) ||
        item.status_label.toLowerCase().includes(q)
      );
    });
  }, [items, filterType, search]);

  const handleDelete = async (item: HistoryItem) => {
    try {
      await apiRequest(`/api/history/${item.type}/${item.record_id}`, { method: "DELETE" });
      setItems((prev) => prev.filter((x) => x.uid !== item.uid));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not delete record.");
    }
  };

  const handleDownloadPdf = async (item: HistoryItem) => {
    try {
      await downloadPdfReport(item.pdf_url, `safepulse-${item.uid}.pdf`);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not download PDF report.");
    }
  };

  const handleDownloadMonthlyPdf = async () => {
    try {
      await downloadPdfReport(
        `/api/reports/monthly.pdf?language=${language}`,
        `safepulse-monthly-report-${language}.pdf`
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not download monthly PDF report.");
    }
  };

  if (loading) {
    return <Skeleton className="h-96" />;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-50">{t.history.title}</h2>
          <p className="mt-1 text-sm text-slate-400">
            {t.history.subtitle}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <Button variant="secondary" size="sm" onClick={() => void handleDownloadMonthlyPdf()}>
            <Download className="h-3.5 w-3.5" aria-hidden="true" />
            <span>{language === "bn" ? "মাসিক PDF" : "Monthly PDF"}</span>
          </Button>
          <Button variant="secondary" size="sm" onClick={() => navigate("/app/reports")}>
            <FileBarChart2 className="h-3.5 w-3.5 text-cyan-300" aria-hidden="true" />
            <span>{language === "bn" ? "সব রিপোর্ট সেন্টার" : "All Reports Hub"}</span>
          </Button>
          <div className="inline-flex rounded-xl border border-slate-800 bg-[#10182B] p-1">
            <button
              type="button"
              onClick={() => setTab("scans")}
              className={`rounded-lg px-3 py-1.5 text-xs font-medium ${
                tab === "scans" ? "bg-[#6366F1] text-white" : "text-slate-300"
              }`}
            >
              {t.history.activityTab} ({items.length})
            </button>
            <button
              type="button"
              onClick={() => setTab("audit")}
              className={`rounded-lg px-3 py-1.5 text-xs font-medium ${
                tab === "audit" ? "bg-[#6366F1] text-white" : "text-slate-300"
              }`}
            >
              {t.history.auditTab} ({auditLogs.length})
            </button>
          </div>
        </div>
      </div>

      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      {tab === "scans" ? (
        <Card>
          <CardHeader className="flex-wrap">
            <div className="flex flex-wrap items-center gap-2">
              {["all", "phishing", "url", "assessment", "incident"].map((t) => (
                <button
                  key={t}
                  type="button"
                  onClick={() => setFilterType(t)}
                  className={`rounded-lg px-2.5 py-1 text-xs font-medium capitalize ${
                    filterType === t
                      ? "bg-[#06B6D4]/20 text-[#06B6D4] border border-cyan-500/40"
                      : "bg-[#10182B] text-slate-300 border border-slate-800"
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>

            <div className="relative w-full sm:w-64">
              <Search
                className="pointer-events-none absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-slate-400"
                aria-hidden="true"
              />
              <input
                type="search"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Filter records..."
                aria-label="Filter scan history"
                className="w-full rounded-lg border border-slate-700 bg-[#080D1B] py-1.5 pl-8 pr-3 text-xs text-white placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
              />
            </div>
          </CardHeader>

          <CardContent className="overflow-x-auto">
            {filteredItems.length === 0 ? (
              <EmptyState
                title="No matching records"
                description="Run a phishing analysis, URL scan, or security assessment to populate your history."
              />
            ) : (
              <table className="w-full text-left text-xs">
                <caption className="visually-hidden">Unified SafePulse AI scan and incident history</caption>
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400">
                    <th scope="col" className="py-2.5 pr-3">Type</th>
                    <th scope="col" className="py-2.5 pr-3">Target / Summary</th>
                    <th scope="col" className="py-2.5 pr-3">Score</th>
                    <th scope="col" className="py-2.5 pr-3">Status</th>
                    <th scope="col" className="py-2.5 pr-3">Date</th>
                    <th scope="col" className="py-2.5 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/80">
                  {filteredItems.map((item) => (
                    <tr key={item.uid} className="hover:bg-[#10182B]/70">
                      <td className="py-3 pr-3 font-mono uppercase text-[#06B6D4]">
                        {item.type}
                        {item.is_demo_sample && (
                          <span className="ml-1.5 rounded bg-cyan-500/15 px-1.5 py-0.5 text-[10px] text-cyan-300">
                            DEMO
                          </span>
                        )}
                      </td>
                      <td className="max-w-xs py-3 pr-3">
                        <div className="font-semibold text-slate-100">{item.title}</div>
                        <div className="truncate text-slate-400">{item.target}</div>
                      </td>
                      <td className="py-3 pr-3 font-mono font-semibold text-slate-100">
                        {item.score}/100
                      </td>
                      <td className="py-3 pr-3">
                        <RiskBadge category={item.status_label} />
                      </td>
                      <td className="whitespace-nowrap py-3 pr-3 text-slate-400">
                        {formatTimestamp(item.created_at)}
                      </td>
                      <td className="py-3 text-right">
                        <div className="inline-flex items-center gap-1.5">
                          {(item.type === "phishing" || item.type === "url") && (
                            <button
                              type="button"
                              onClick={() =>
                                navigate(
                                  item.type === "phishing"
                                    ? `/app/phishing?id=${item.record_id}`
                                    : `/app/url-scanner?id=${item.record_id}`
                                )
                              }
                              aria-label={`Inspect ${item.title}`}
                              title="Open detailed analysis"
                              className="inline-flex items-center gap-1 rounded-lg border border-slate-700 bg-[#10182B] px-2.5 py-1.5 text-[11px] font-medium text-slate-200 hover:border-[#6366F1]"
                            >
                              <ExternalLink className="h-3.5 w-3.5 text-indigo-300" aria-hidden="true" />
                              <span>{language === "bn" ? "বিস্তারিত" : "View"}</span>
                            </button>
                          )}
                          <button
                            type="button"
                            onClick={() => handleDownloadPdf(item)}
                            aria-label={`Download PDF report for ${item.title}`}
                            className="inline-flex items-center gap-1 rounded-lg border border-cyan-500/35 bg-cyan-500/10 px-2.5 py-1.5 text-[11px] font-medium text-cyan-200 hover:bg-cyan-500/20"
                          >
                            <Download className="h-3.5 w-3.5 text-cyan-300" aria-hidden="true" />
                            <span>PDF</span>
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDelete(item)}
                            aria-label={`Delete ${item.title}`}
                            className="rounded-lg border border-slate-700 bg-[#10182B] p-1.5 text-red-300 hover:border-red-500/50 hover:bg-red-500/10"
                          >
                            <Trash2 className="h-3.5 w-3.5" aria-hidden="true" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent className="space-y-2.5">
            {auditLogs.map((log) => (
              <div
                key={log.id}
                className="flex flex-wrap items-center justify-between gap-2 rounded-lg border border-slate-800 bg-[#10182B] px-3.5 py-2.5 text-xs"
              >
                <div>
                  <span className="font-mono text-[#06B6D4]">{log.action}</span>
                  <span className="mx-2 text-slate-600">•</span>
                  <span className="text-slate-200">{log.summary}</span>
                </div>
                <span className="text-[11px] text-slate-400">{formatTimestamp(log.created_at)}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

