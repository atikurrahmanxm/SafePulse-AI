import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
  AlertTriangle,
  BarChart3,
  CheckCircle2,
  Clock,
  Download,
  FileSearch,
  FlaskConical,
  Sparkles,
} from "lucide-react";
import { useLanguage } from "../i18n/LanguageContext";
import { apiRequest, ApiError, downloadPdfReport } from "../lib/api";
import { formatTimestamp, getRiskColor } from "../lib/utils";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  ErrorBanner,
  RiskBadge,
} from "../components/ui/Primitives";
import { ProgressRing } from "../components/ui/ProgressRing";

interface HighlightSpan {
  phrase: string;
  category: string;
  weight: number;
  start: number;
  end: number;
}

interface SocialEngineeringTactic {
  category: string;
  label: string;
  severity: string;
  match_count: number;
  evidence_examples?: string[];
}

interface PhishingResult {
  id: number;
  channel: string;
  sender_hint?: string | null;
  raw_message: string;
  risk_score: number;
  risk_category: string;
  ml_probability: number;
  model_confidence: number;
  highlighted_phrases: HighlightSpan[];
  social_engineering_tactics?: Array<SocialEngineeringTactic | string>;
  reasons: string[];
  recommendations: string[];
  created_at: string;
}

interface SampleItem {
  id: string;
  label: string;
  channel: "email" | "sms" | "whatsapp" | "other";
  sender_hint: string;
  message: string;
}

interface ModelEvalReport {
  model_name: string;
  trained_at: string;
  dataset: {
    total_samples: number;
    phishing_samples: number;
    benign_samples: number;
    train_size: number;
    held_out_test_size: number;
    split_strategy: string;
    description: string;
  };
  held_out_metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
    roc_auc: number;
    confusion_matrix: {
      tn: number;
      fp: number;
      fn: number;
      tp: number;
    };
  };
  cross_validation_5fold: {
    mean_f1: number;
    std_f1: number;
  };
  top_indicators: {
    phishing_terms: Array<{ term: string; weight: number }>;
    legitimate_terms: Array<{ term: string; weight: number }>;
  };
  limitations: string[];
}

function HighlightedText({
  text,
  spans,
}: {
  text: string;
  spans: HighlightSpan[];
}) {
  if (!spans || spans.length === 0) {
    return <p className="whitespace-pre-wrap text-sm leading-relaxed text-slate-200">{text}</p>;
  }

  const ordered = [...spans].sort((a, b) => a.start - b.start);
  const parts: React.ReactNode[] = [];
  let cursor = 0;

  ordered.forEach((span, idx) => {
    if (span.start > cursor) {
      parts.push(
        <span key={`plain-${idx}`}>{text.slice(cursor, span.start)}</span>
      );
    }
    const seg = text.slice(span.start, span.end);
    parts.push(
      <mark
        key={`mark-${idx}`}
        title={`${span.category.replace(/_/g, " ")} (+${span.weight})`}
        className="rounded border border-red-500/40 bg-red-500/20 px-1 py-0.5 text-red-200"
      >
        {seg}
      </mark>
    );
    cursor = Math.max(cursor, span.end);
  });

  if (cursor < text.length) {
    parts.push(<span key="tail">{text.slice(cursor)}</span>);
  }

  return <p className="whitespace-pre-wrap text-sm leading-relaxed text-slate-200">{parts}</p>;
}

export function PhishingDetectorPage() {
  const { language, t } = useLanguage();
  const [searchParams, setSearchParams] = useSearchParams();
  const [tab, setTab] = useState<"analyze" | "evaluation">("analyze");
  const [channel, setChannel] = useState<"email" | "sms" | "whatsapp" | "other">("email");
  const [senderHint, setSenderHint] = useState("");
  const [message, setMessage] = useState("");
  const [samples, setSamples] = useState<SampleItem[]>([]);
  const [recentScans, setRecentScans] = useState<PhishingResult[]>([]);
  const [result, setResult] = useState<PhishingResult | null>(null);
  const [evalReport, setEvalReport] = useState<ModelEvalReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiRequest<{ samples: SampleItem[] }>("/api/phishing/samples")
      .then((res) => {
        if (Array.isArray(res?.samples)) setSamples(res.samples);
      })
      .catch(() => {});
    apiRequest<ModelEvalReport>("/api/phishing/model-evaluation")
      .then((res) => {
        if (res && res.held_out_metrics) setEvalReport(res);
      })
      .catch(() => {});
    apiRequest<PhishingResult[]>("/api/phishing/history")
      .then((res) => {
        if (Array.isArray(res)) setRecentScans(res);
      })
      .catch(() => {});
  }, []);

  const selectedIdParam = searchParams.get("id");
  useEffect(() => {
    if (!selectedIdParam) return;
    const numericId = Number(selectedIdParam);
    if (!Number.isFinite(numericId) || numericId <= 0) return;
    apiRequest<PhishingResult>(`/api/phishing/${numericId}`)
      .then((res) => {
        if (res && typeof res.risk_score === "number") {
          setResult(res);
          setMessage(res.raw_message || "");
          setSenderHint(res.sender_hint || "");
          if (res.channel === "email" || res.channel === "sms" || res.channel === "whatsapp" || res.channel === "other") {
            setChannel(res.channel);
          }
          setTab("analyze");
        }
      })
      .catch(() => {});
  }, [selectedIdParam]);

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (message.trim().length < 10) {
      setError("Please paste at least 10 characters of message text to analyze.");
      return;
    }
    setLoading(true);
    try {
      const res = await apiRequest<PhishingResult>("/api/phishing/analyze", {
        method: "POST",
        body: JSON.stringify({
          message,
          channel,
          sender_hint: senderHint.trim() || null,
          language,
        }),
      });
      setResult(res);
      setRecentScans((prev) => [res, ...prev.filter((item) => item.id !== res.id)].slice(0, 8));
      setSearchParams({ id: String(res.id) }, { replace: true });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleLoadSample = (s: SampleItem) => {
    setChannel(s.channel);
    setSenderHint(s.sender_hint);
    setMessage(s.message);
    setError(null);
  };

  const handleDownloadPdf = async () => {
    if (!result) return;
    setPdfLoading(true);
    try {
      await downloadPdfReport(
        `/api/phishing/${result.id}/report.pdf`,
        `cybershield-phishing-${result.id}.pdf`
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not download PDF report.");
    } finally {
      setPdfLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-50">{t.phishing.title}</h2>
          <p className="mt-1 text-sm text-slate-400">{t.phishing.subtitle}</p>
        </div>

        <div className="inline-flex rounded-xl border border-slate-800 bg-[#10182B] p-1">
          <button
            type="button"
            onClick={() => setTab("analyze")}
            className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium transition-colors ${
              tab === "analyze" ? "bg-[#6366F1] text-white" : "text-slate-300 hover:text-white"
            }`}
          >
            <FileSearch className="h-3.5 w-3.5" aria-hidden="true" />
            <span>Message Analyzer</span>
          </button>
          <button
            type="button"
            onClick={() => setTab("evaluation")}
            className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium transition-colors ${
              tab === "evaluation" ? "bg-[#6366F1] text-white" : "text-slate-300 hover:text-white"
            }`}
          >
            <BarChart3 className="h-3.5 w-3.5" aria-hidden="true" />
            <span>{t.phishing.mlMetricsTab}</span>
          </button>
        </div>
      </div>

      {tab === "analyze" ? (
        <div className="grid gap-6 lg:grid-cols-12">
          {/* Input Panel */}
          <Card className="lg:col-span-6">
            <CardHeader>
              <h3 className="text-sm font-semibold text-slate-100">Submit Message for Inspection</h3>
            </CardHeader>
            <CardContent className="space-y-4">
              {samples.length > 0 && (
                <div>
                  <div className="mb-2 flex items-center gap-1.5 text-xs font-medium text-[#06B6D4]">
                    <FlaskConical className="h-3.5 w-3.5" aria-hidden="true" />
                    <span>{t.phishing.samplesLabel} (Demonstration):</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {samples.map((s) => (
                      <button
                        key={s.id}
                        type="button"
                        onClick={() => handleLoadSample(s)}
                        className="rounded-lg border border-slate-700/80 bg-[#10182B] px-2.5 py-1.5 text-left text-xs text-slate-200 hover:border-[#06B6D4] hover:bg-[#1B2942]"
                      >
                        {s.label}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

              <form onSubmit={handleAnalyze} className="space-y-4">
                <div className="grid gap-3 sm:grid-cols-2">
                  <div>
                    <label htmlFor="phish-channel" className="block text-xs font-medium text-slate-300">
                      {t.phishing.channelLabel}
                    </label>
                    <select
                      id="phish-channel"
                      value={channel}
                      onChange={(e) => setChannel(e.target.value as typeof channel)}
                      className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white focus:border-[#6366F1] focus:outline-none"
                    >
                      <option value="email">Email</option>
                      <option value="sms">SMS</option>
                      <option value="whatsapp">WhatsApp</option>
                      <option value="other">Other Text</option>
                    </select>
                  </div>
                  <div>
                    <label htmlFor="phish-sender" className="block text-xs font-medium text-slate-300">
                      {t.phishing.senderLabel}
                    </label>
                    <input
                      id="phish-sender"
                      type="text"
                      value={senderHint}
                      onChange={(e) => setSenderHint(e.target.value)}
                      placeholder="e.g., support@gmail.com or VK-SBIALT"
                      className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="phish-message" className="block text-xs font-medium text-slate-300">
                    {t.phishing.messageLabel}
                  </label>
                  <textarea
                    id="phish-message"
                    rows={7}
                    required
                    minLength={10}
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Paste suspicious email body, SMS, or WhatsApp text here..."
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] p-3 text-sm text-white placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
                  />
                </div>

                <div className="flex flex-wrap items-center justify-between gap-3">
                  <span className="text-[11px] text-slate-400">{t.phishing.riskBandNote}</span>
                  <div className="flex flex-wrap items-center gap-2">
                    <Button
                      type="button"
                      variant="ghost"
                      size="lg"
                      onClick={() => {
                        setMessage("");
                        setSenderHint("");
                        setError(null);
                      }}
                    >
                      <span>{language === "bn" ? "মুছুন" : "Clear"}</span>
                    </Button>
                    <Button type="submit" size="lg" disabled={loading}>
                      <Sparkles className="h-4 w-4" aria-hidden="true" />
                      <span>{loading ? t.phishing.analyzing : t.phishing.analyzeBtn}</span>
                    </Button>
                  </div>
                </div>
              </form>

              {recentScans.length > 0 && (
                <div className="border-t border-slate-800/80 pt-4">
                  <div className="mb-2 flex items-center gap-1.5 text-xs font-medium text-slate-400">
                    <Clock className="h-3.5 w-3.5 text-[#06B6D4]" aria-hidden="true" />
                    <span>Recent Saved Analyses</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {recentScans.slice(0, 5).map((item) => (
                      <button
                        key={item.id}
                        type="button"
                        onClick={() => {
                          setResult(item);
                          setMessage(item.raw_message || "");
                          setSenderHint(item.sender_hint || "");
                          setSearchParams({ id: String(item.id) }, { replace: true });
                        }}
                        className={`rounded-lg border px-2.5 py-1 text-left text-[11px] transition-colors ${
                          result?.id === item.id
                            ? "border-[#6366F1] bg-[#6366F1]/15 text-white"
                            : "border-slate-800 bg-[#10182B] text-slate-300 hover:border-slate-700"
                        }`}
                      >
                        <span className="font-mono uppercase text-[#06B6D4]">{item.channel}</span> •{" "}
                        {item.risk_score}/100
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Result Panel */}
          <Card className="lg:col-span-6">
            <CardHeader>
              <h3 className="text-sm font-semibold text-slate-100">Explainable Threat Verdict</h3>
              {result && (
                <Button size="sm" variant="secondary" onClick={handleDownloadPdf} disabled={pdfLoading}>
                  <Download className="h-3.5 w-3.5" aria-hidden="true" />
                  <span>{pdfLoading ? "Exporting..." : t.phishing.downloadPdf}</span>
                </Button>
              )}
            </CardHeader>
            <CardContent>
              {!result ? (
                <div className="flex flex-col items-center justify-center py-14 text-center">
                  <AlertTriangle className="h-10 w-10 text-slate-600" aria-hidden="true" />
                  <p className="mt-3 text-sm font-medium text-slate-300">
                    No message analyzed in this view yet
                  </p>
                  <p className="mt-1 max-w-sm text-xs text-slate-400">
                    Select a demo sample or paste a real suspicious message on the left to inspect its ML probability, confidence, and trigger phrases.
                  </p>
                </div>
              ) : (
                <div className="space-y-5">
                  <div className="flex flex-col items-center gap-5 rounded-xl border border-slate-800 bg-[#10182B] p-5 sm:flex-row">
                    <ProgressRing
                      value={result.risk_score}
                      colorHex={getRiskColor(result.risk_category).hex}
                      label="Phishing Risk Score"
                      sublabel="/ 100 Risk"
                    />
                    <div className="flex-1 space-y-2 text-center sm:text-left">
                      <div className="flex flex-wrap items-center justify-center gap-2 sm:justify-start">
                        <RiskBadge category={result.risk_category} />
                        <span className="font-mono text-xs text-slate-400">
                          {result.channel.toUpperCase()}
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-2 pt-1 text-xs">
                        <div className="rounded-lg border border-slate-800 bg-[#141F35] px-3 py-2">
                          <div className="text-slate-400">ML Probability</div>
                          <div className="font-mono text-sm font-semibold text-slate-100">
                            {(result.ml_probability * 100).toFixed(1)}%
                          </div>
                        </div>
                        <div className="rounded-lg border border-slate-800 bg-[#141F35] px-3 py-2">
                          <div className="text-slate-400">Calibrated Confidence</div>
                          <div className="font-mono text-sm font-semibold text-slate-100">
                            {Math.round(result.model_confidence * 100)}%
                          </div>
                        </div>
                      </div>
                      <p className="text-[11px] text-slate-400">
                        Analyzed: {formatTimestamp(result.created_at)}
                      </p>
                    </div>
                  </div>

                  {/* Simple Owner Advice Banner */}
                  <div
                    className={`rounded-xl border px-4 py-3 text-xs leading-relaxed ${
                      result.risk_score >= 60
                        ? "border-red-500/40 bg-red-500/12 text-red-100"
                        : result.risk_score >= 30
                        ? "border-amber-500/40 bg-amber-500/12 text-amber-100"
                        : "border-emerald-500/40 bg-emerald-500/12 text-emerald-100"
                    }`}
                  >
                    <div className="font-semibold">
                      {result.risk_score >= 60
                        ? language === "bn"
                          ? "সতর্কতা: এখনই কী করবেন?"
                          : "What Should You Do? — High Scam Risk"
                        : result.risk_score >= 30
                        ? language === "bn"
                          ? "সাবধান: আগে নিশ্চিত হয়ে নিন"
                          : "What Should You Do? — Verify Before Acting"
                        : language === "bn"
                        ? "তুলনামূলক নিরাপদ, তবুও সতর্ক থাকুন"
                        : "What Should You Do? — Low Risk Indicator"}
                    </div>
                    <p className="mt-1 opacity-90">
                      {result.risk_score >= 60
                        ? language === "bn"
                          ? "কোনো লিংকে ক্লিক করবেন না, রিপ্লাই করবেন না এবং OTP বা UPI PIN শেয়ার করবেন না। সন্দেহজনক হলে ১৯৩০ নম্বরে বা অফিশিয়াল ওয়েবসাইটে যাচাই করুন।"
                          : "Do NOT click links, reply, or share OTP/UPI PIN. Confirm directly through official phone numbers or apps first."
                        : result.risk_score >= 30
                        ? language === "bn"
                          ? "প্রেরকের আসল নাম্বার বা ইমেইল ঠিকানা ফোন করে যাচাই করার আগে কোনো পেমেন্ট বা লগইন করবেন না।"
                          : "Double-check the sender's official number or domain via a trusted channel before approving payments or logins."
                        : language === "bn"
                        ? "কোনো বড় প্রতারণার লক্ষণ পাওয়া যায়নি, তবুও লগইন বা টাকা পাঠানোর আগে অফিশিয়াল সোর্স মিলিয়ে নিন।"
                        : "No strong phishing cues detected, though you should always confirm banking or login requests directly."}
                    </p>
                  </div>

                  <div>
                    <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
                      {t.phishing.highlightedTitle}
                    </h4>
                    <div className="rounded-xl border border-slate-800 bg-[#080D1B] p-3.5">
                      <HighlightedText
                        text={result.raw_message}
                        spans={result.highlighted_phrases}
                      />
                    </div>
                  </div>

                  {Array.isArray(result.social_engineering_tactics) &&
                    result.social_engineering_tactics.length > 0 && (
                      <div>
                        <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
                          Social Engineering Manipulation Tactics
                        </h4>
                        <div className="grid gap-2 sm:grid-cols-2">
                          {result.social_engineering_tactics.map((tactic, idx) => {
                            if (typeof tactic === "string") {
                              return (
                                <span
                                  key={`${tactic}-${idx}`}
                                  className="inline-flex items-center rounded-md border border-amber-500/35 bg-amber-500/10 px-2.5 py-1 text-xs font-medium text-amber-200"
                                >
                                  {tactic}
                                </span>
                              );
                            }
                            return (
                              <div
                                key={tactic.category || idx}
                                className="rounded-lg border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-xs"
                              >
                                <div className="flex items-center justify-between gap-2">
                                  <span className="font-semibold text-amber-200">
                                    {tactic.label}
                                  </span>
                                  <span className="rounded bg-amber-500/20 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-amber-300">
                                    {tactic.severity} ({tactic.match_count}x)
                                  </span>
                                </div>
                                {Array.isArray(tactic.evidence_examples) &&
                                  tactic.evidence_examples.length > 0 && (
                                    <div className="mt-1 truncate text-[11px] text-slate-300">
                                      Triggers: {tactic.evidence_examples.join(", ")}
                                    </div>
                                  )}
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    )}

                  <div>
                    <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
                      {t.phishing.reasonsTitle}
                    </h4>
                    <ul className="space-y-1.5 text-xs text-slate-300">
                      {result.reasons.map((r, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <span className="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-[#06B6D4]" aria-hidden="true" />
                          <span>{r}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
                      {t.phishing.actionsTitle}
                    </h4>
                    <ul className="space-y-1.5 text-xs text-emerald-200">
                      {result.recommendations.map((rec, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <CheckCircle2 className="mt-0.5 h-3.5 w-3.5 shrink-0 text-emerald-400" aria-hidden="true" />
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      ) : (
        /* ML Model & Held-Out Evaluation Tab */
        <div className="space-y-6">
          {!evalReport ? (
            <ErrorBanner message="Model evaluation metrics are loading or unavailable." />
          ) : (
            <>
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
                {[
                  { label: "Precision (Phishing)", val: `${(evalReport.held_out_metrics.precision * 100).toFixed(1)}%` },
                  { label: "Recall (Phishing)", val: `${(evalReport.held_out_metrics.recall * 100).toFixed(1)}%` },
                  { label: "F1-Score", val: `${(evalReport.held_out_metrics.f1_score * 100).toFixed(1)}%` },
                  { label: "ROC-AUC", val: evalReport.held_out_metrics.roc_auc.toFixed(3) },
                  { label: "5-Fold CV F1", val: `${(evalReport.cross_validation_5fold.mean_f1 * 100).toFixed(1)}%` },
                ].map((m) => (
                  <Card key={m.label}>
                    <CardContent>
                      <div className="text-xs text-slate-400">{m.label}</div>
                      <div className="mt-1.5 font-mono text-2xl font-bold text-[#06B6D4]">{m.val}</div>
                    </CardContent>
                  </Card>
                ))}
              </div>

              <div className="grid gap-6 lg:grid-cols-2">
                <Card>
                  <CardHeader>
                    <h3 className="text-sm font-semibold text-slate-100">
                      Held-Out Test Confusion Matrix ({evalReport.dataset.held_out_test_size} samples)
                    </h3>
                  </CardHeader>
                  <CardContent>
                    <table className="w-full text-center text-xs">
                      <caption className="mb-3 text-left text-xs text-slate-400">
                        {evalReport.dataset.split_strategy}
                      </caption>
                      <thead>
                        <tr className="border-b border-slate-800 text-slate-400">
                          <th scope="col" className="py-2 text-left">Actual \ Predicted</th>
                          <th scope="col" className="py-2">Legitimate (0)</th>
                          <th scope="col" className="py-2">Phishing (1)</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800">
                        <tr>
                          <th scope="row" className="py-3 text-left font-medium text-slate-200">
                            Legitimate (0)
                          </th>
                          <td className="py-3 font-mono font-semibold text-emerald-400">
                            TN = {evalReport.held_out_metrics.confusion_matrix.tn}
                          </td>
                          <td className="py-3 font-mono font-semibold text-amber-400">
                            FP = {evalReport.held_out_metrics.confusion_matrix.fp}
                          </td>
                        </tr>
                        <tr>
                          <th scope="row" className="py-3 text-left font-medium text-slate-200">
                            Phishing (1)
                          </th>
                          <td className="py-3 font-mono font-semibold text-red-400">
                            FN = {evalReport.held_out_metrics.confusion_matrix.fn}
                          </td>
                          <td className="py-3 font-mono font-semibold text-emerald-400">
                            TP = {evalReport.held_out_metrics.confusion_matrix.tp}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <h3 className="text-sm font-semibold text-slate-100">Dataset & Honest Limitations</h3>
                  </CardHeader>
                  <CardContent className="space-y-3 text-xs leading-relaxed text-slate-300">
                    <p>
                      <strong className="text-slate-100">Pipeline:</strong> {evalReport.model_name}
                    </p>
                    <p>
                      <strong className="text-slate-100">Corpus ({evalReport.dataset.total_samples} total):</strong>{" "}
                      {evalReport.dataset.phishing_samples} phishing/scam + {evalReport.dataset.benign_samples} legitimate SME messages.{" "}
                      {evalReport.dataset.description}
                    </p>
                    <div className="border-t border-slate-800 pt-2">
                      <div className="mb-1.5 font-semibold text-amber-300">Model Limitations:</div>
                      <ul className="space-y-1 text-slate-400">
                        {evalReport.limitations.map((lim, i) => (
                          <li key={i}>• {lim}</li>
                        ))}
                      </ul>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

