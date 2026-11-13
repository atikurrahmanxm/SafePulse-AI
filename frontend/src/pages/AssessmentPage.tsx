import React, { useEffect, useState } from "react";
import { CheckCircle2, ClipboardCheck, Download, ShieldAlert } from "lucide-react";
import {
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
import { apiRequest, ApiError, downloadPdfReport } from "../lib/api";
import { formatTimestamp, getHealthScoreColor } from "../lib/utils";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  ErrorBanner,
  RiskBadge,
  Skeleton,
} from "../components/ui/Primitives";
import { ProgressRing } from "../components/ui/ProgressRing";

interface QuestionItem {
  key: string;
  domain: string;
  domain_label: string;
  weight: number;
  prompt: string;
  guidance: string;
}

interface AssessmentResult {
  id: number;
  overall_score: number;
  security_category: string;
  category_scores: Record<string, number>;
  weak_areas: string[];
  critical_gaps: string[];
  recommendations: Array<{
    domain: string;
    domain_label: string;
    priority: string;
    action: string;
  }>;
  answers: Record<string, string>;
  updated_at: string;
}

export function AssessmentPage() {
  const { language, t } = useLanguage();
  const [questions, setQuestions] = useState<QuestionItem[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [latest, setLatest] = useState<AssessmentResult | null>(null);
  const [history, setHistory] = useState<AssessmentResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    Promise.all([
      apiRequest<{ questions: QuestionItem[] }>(`/api/assessments/questions?language=${language}`),
      apiRequest<{ assessment: AssessmentResult | null }>("/api/assessments/latest"),
      apiRequest<{ assessments: AssessmentResult[] }>("/api/assessments/history").catch(() => ({ assessments: [] })),
    ])
      .then(([qRes, aRes, hRes]) => {
        if (!active) return;
        setQuestions(qRes.questions);
        if (Array.isArray(hRes.assessments)) {
          setHistory(hRes.assessments);
        }
        if (aRes.assessment) {
          setLatest(aRes.assessment);
          setAnswers(aRes.assessment.answers);
        } else {
          const initial: Record<string, string> = {};
          qRes.questions.forEach((q) => {
            initial[q.key] = "partial";
          });
          setAnswers(initial);
        }
      })
      .catch((err) => {
        if (active) setError(err.message || "Failed to load assessment.");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [language]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const res = await apiRequest<AssessmentResult>("/api/assessments/submit", {
        method: "POST",
        body: JSON.stringify({ answers, language }),
      });
      setLatest(res);
      setHistory((prev) => [res, ...prev.filter((item) => item.id !== res.id)]);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not save assessment.");
    } finally {
      setSubmitting(false);
    }
  };

  const handlePdf = async () => {
    if (!latest) return;
    setPdfLoading(true);
    try {
      await downloadPdfReport(
        `/api/assessments/${latest.id}/report.pdf`,
        `cybershield-assessment-${latest.id}.pdf`
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to download PDF.");
    } finally {
      setPdfLoading(false);
    }
  };

  if (loading) {
    return <Skeleton className="h-96" />;
  }

  const chartData = questions.map((q) => {
    const score = latest?.category_scores[q.key] ?? 0;
    return {
      name: q.domain_label.split(" ").slice(0, 2).join(" "),
      score,
    };
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-50">{t.assessment.title}</h2>
          <p className="mt-1 text-sm text-slate-400">{t.assessment.subtitle}</p>
        </div>
        {latest && (
          <Button variant="secondary" size="sm" onClick={handlePdf} disabled={pdfLoading}>
            <Download className="h-3.5 w-3.5" aria-hidden="true" />
            <span>{pdfLoading ? "Exporting..." : "Download PDF Report"}</span>
          </Button>
        )}
      </div>

      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      {latest && (
        <div className="grid gap-6 lg:grid-cols-12">
          <Card className="lg:col-span-4">
            <CardHeader>
              <h3 className="text-sm font-semibold text-slate-100">Overall Security Health</h3>
            </CardHeader>
            <CardContent className="flex flex-col items-center gap-4 text-center">
              <ProgressRing
                value={latest.overall_score}
                colorHex={getHealthScoreColor(latest.overall_score)}
                label="Business Security Score"
                sublabel="/ 100"
              />
              <RiskBadge category={latest.security_category} />
              <div className="w-full space-y-2 pt-2 text-left text-xs">
                <div className="rounded-lg border border-red-500/30 bg-red-500/10 p-3">
                  <div className="font-semibold text-red-300">
                    {t.assessment.criticalGaps} ({latest.critical_gaps.length})
                  </div>
                  <p className="mt-1 text-slate-300">
                    {latest.critical_gaps.length > 0
                      ? latest.critical_gaps.join(", ")
                      : "No critical gaps reported."}
                  </p>
                </div>
                <div className="rounded-lg border border-amber-500/30 bg-amber-500/10 p-3">
                  <div className="font-semibold text-amber-300">
                    {t.assessment.weakAreas} ({latest.weak_areas.length})
                  </div>
                  <p className="mt-1 text-slate-300">
                    {latest.weak_areas.length > 0
                      ? latest.weak_areas.join(", ")
                      : "All 10 domains meet baseline controls."}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="lg:col-span-8">
            <CardHeader>
              <h3 className="text-sm font-semibold text-slate-100">Domain Control Scores (%)</h3>
            </CardHeader>
            <CardContent className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} layout="vertical" margin={{ left: 20, right: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                  <XAxis type="number" domain={[0, 100]} stroke="#94A3B8" fontSize={11} />
                  <YAxis type="category" dataKey="name" width={130} stroke="#CBD5E1" fontSize={11} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#10182B",
                      borderColor: "#334155",
                      borderRadius: "8px",
                      fontSize: "12px",
                    }}
                  />
                  <Bar dataKey="score" radius={[0, 6, 6, 0]}>
                    {chartData.map((entry, idx) => (
                      <Cell
                        key={idx}
                        fill={entry.score === 100 ? "#22C55E" : entry.score >= 50 ? "#06B6D4" : "#EF4444"}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>
      )}

      {latest && latest.recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <h3 className="text-sm font-semibold text-slate-100">{t.assessment.actionPlan}</h3>
          </CardHeader>
          <CardContent className="grid gap-3 md:grid-cols-2">
            {latest.recommendations.map((rec, idx) => (
              <div key={idx} className="rounded-xl border border-slate-800 bg-[#10182B] p-3.5">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-xs font-semibold text-slate-100">{rec.domain_label}</span>
                  <RiskBadge category={rec.priority} />
                </div>
                <p className="mt-1.5 text-xs leading-relaxed text-slate-300">{rec.action}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Interactive 10-Question Assessment Form */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <ClipboardCheck className="h-4 w-4 text-[#06B6D4]" aria-hidden="true" />
            <h3 className="text-sm font-semibold text-slate-100">
              10-Point Security Questionnaire (CERT-In MSME Aligned)
            </h3>
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {questions.map((q, idx) => {
              const current = answers[q.key] || "no";
              return (
                <fieldset
                  key={q.key}
                  className="rounded-xl border border-slate-800 bg-[#10182B] p-4"
                >
                  <legend className="px-1 text-xs font-semibold text-[#06B6D4]">
                    {idx + 1}. {q.domain_label} (Weight: {q.weight}%)
                  </legend>
                  <p className="mt-1 text-sm font-medium text-slate-100">{q.prompt}</p>
                  <p className="mt-1 text-xs text-slate-400">{q.guidance}</p>
                  <div className="mt-3 flex flex-wrap gap-2.5">
                    {[
                      { val: "yes", label: t.assessment.yes },
                      { val: "partial", label: t.assessment.partial },
                      { val: "no", label: t.assessment.no },
                    ].map((opt) => {
                      const active = current === opt.val;
                      return (
                        <label
                          key={opt.val}
                          className={`inline-flex cursor-pointer items-center gap-2 rounded-lg border px-3 py-2 text-xs font-medium transition-colors ${
                            active
                              ? "border-[#6366F1] bg-[#6366F1]/20 text-white"
                              : "border-slate-700/80 bg-[#080D1B] text-slate-300 hover:border-slate-600"
                          }`}
                        >
                          <input
                            type="radio"
                            name={`q-${q.key}`}
                            value={opt.val}
                            checked={active}
                            onChange={() =>
                              setAnswers((prev) => ({ ...prev, [q.key]: opt.val }))
                            }
                            className="accent-[#6366F1]"
                          />
                          <span>{opt.label}</span>
                        </label>
                      );
                    })}
                  </div>
                </fieldset>
              );
            })}

            <div className="flex justify-end pt-2">
              <Button type="submit" size="lg" disabled={submitting}>
                <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
                <span>
                  {submitting
                    ? "Calculating..."
                    : latest
                    ? t.assessment.updateBtn
                    : t.assessment.submitBtn}
                </span>
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {history.length > 0 && (
        <Card>
          <CardHeader>
            <h3 className="text-sm font-semibold text-slate-100">Assessment Submission History ({history.length})</h3>
            <span className="text-xs text-slate-400">Chronological posture progression</span>
          </CardHeader>
          <CardContent>
            <div className="divide-y divide-slate-800/80">
              {history.map((item) => (
                <div key={item.id} className="flex flex-wrap items-center justify-between gap-3 py-2.5 text-xs">
                  <div className="flex items-center gap-3">
                    <span
                      className="font-mono text-sm font-bold"
                      style={{ color: getHealthScoreColor(item.overall_score) }}
                    >
                      {item.overall_score}%
                    </span>
                    <RiskBadge category={item.security_category} />
                    <span className="text-slate-300">
                      {item.critical_gaps.length > 0
                        ? `${item.critical_gaps.length} critical gap(s)`
                        : "0 critical gaps"}
                    </span>
                  </div>
                  <span className="text-[11px] text-slate-400">{formatTimestamp(item.updated_at)}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

