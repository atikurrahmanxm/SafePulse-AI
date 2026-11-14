import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
  CheckCircle2,
  Clock,
  Download,
  FlaskConical,
  Info,
  Link2,
  ShieldAlert,
  Copy,
  Check,
  Share2,
  MessageSquare,
} from "lucide-react";
import { useLanguage } from "../i18n/LanguageContext";
import { apiRequest, ApiError, downloadPdfReport } from "../lib/api";
import { getRiskColor } from "../lib/utils";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  ErrorBanner,
  RiskBadge,
} from "../components/ui/Primitives";
import { ProgressRing } from "../components/ui/ProgressRing";

interface UrlIndicator {
  code: string;
  label: string;
  severity: string;
  detail: string;
  score_impact: number;
}

interface UrlScanResult {
  id: number;
  submitted_url: string;
  normalized_host: string;
  scheme: string;
  risk_score: number;
  risk_category: string;
  verdict_classification?: string;
  indicators: UrlIndicator[];
  dns_records: {
    queried_domain?: string;
    a_records?: string[];
    spf_present?: boolean;
    spf_record?: string | null;
    dmarc_present?: boolean;
    dmarc_record?: string | null;
    dns_status?: string;
  };
  tls_info?: {
    tls_status?: string;
    issuer_org?: string | null;
    subject_cn?: string | null;
    not_after?: string | null;
    san_count?: number;
    detail?: string | null;
  };
  reputation_source: string;
  technical_explanation: string;
  recommendations: string[];
  created_at: string;
}

interface UrlSample {
  id: string;
  label: string;
  url: string;
}

export function UrlScannerPage() {
  const { language, t } = useLanguage();
  const [searchParams, setSearchParams] = useSearchParams();
  const [urlInput, setUrlInput] = useState("");
  const [samples, setSamples] = useState<UrlSample[]>([]);
  const [recentScans, setRecentScans] = useState<UrlScanResult[]>([]);
  const [result, setResult] = useState<UrlScanResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [copiedWarning, setCopiedWarning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiRequest<{ samples: UrlSample[] }>("/api/urls/samples")
      .then((res) => {
        if (Array.isArray(res?.samples)) setSamples(res.samples);
      })
      .catch(() => {});
    apiRequest<UrlScanResult[]>("/api/urls/history")
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
    apiRequest<UrlScanResult>(`/api/urls/${numericId}`)
      .then((res) => {
        if (res && typeof res.risk_score === "number") {
          setResult(res);
          setUrlInput(res.submitted_url || "");
        }
      })
      .catch(() => {});
  }, [selectedIdParam]);

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const res = await apiRequest<UrlScanResult>("/api/urls/scan", {
        method: "POST",
        body: JSON.stringify({ url: urlInput.trim(), language }),
      });
      setResult(res);
      setRecentScans((prev) => [res, ...prev.filter((item) => item.id !== res.id)].slice(0, 8));
      setSearchParams({ id: String(res.id) }, { replace: true });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "URL scan failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!result) return;
    setPdfLoading(true);
    try {
      await downloadPdfReport(
        `/api/urls/${result.id}/report.pdf`,
        `safepulse-url-${result.id}.pdf`
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not download PDF report.");
    } finally {
      setPdfLoading(false);
    }
  };

  const getStaffWarningMessage = () => {
    if (!result) return "";
    const urlClean = result.submitted_url || result.normalized_host;

    if (language === "bn") {
      return `⚠️ *জরুরি সাইবার সতর্কতা (SafePulse AI)* ⚠️\n\nসাবধান! দোকানে এই মাত্র একটি বিপজ্জনক/সন্দেহজনক লিংক ধরা পড়েছে:\n"${urlClean}"\n🚨 *সতর্কতা নির্দেশ:* দোকানের কেউ এই লিঙ্কে ভুলেও ক্লিক করবেন না বা ব্রাউজারে খুলবেন না। কোনো পাসওয়ার্ড বা UPI পিন দেবেন না।\n\n— SafePulse AI SME Protection`;
    }
    return `⚠️ *URGENT SECURITY ALERT (SafePulse AI)* ⚠️\n\nWarning! A suspicious/malicious link was just detected at our counter:\n"${urlClean}"\n🚨 *ACTION REQUIRED:* Do NOT click or open this link. Do NOT enter any passwords or UPI PINs.\n\n— SafePulse AI SME Protection`;
  };

  const handleCopyStaffWarning = async () => {
    try {
      await navigator.clipboard.writeText(getStaffWarningMessage());
      setCopiedWarning(true);
      setTimeout(() => setCopiedWarning(false), 2500);
    } catch {
      // Fallback
    }
  };

  const getWhatsAppShareUrl = () => {
    const msg = getStaffWarningMessage();
    return `https://wa.me/?text=${encodeURIComponent(msg)}`;
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-bold text-slate-50">{t.url.title}</h2>
        <p className="mt-1 text-sm text-slate-400">{t.url.subtitle}</p>
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        <div className="flex items-start gap-2.5 rounded-xl border border-cyan-500/30 bg-cyan-500/5 p-3.5 text-xs text-cyan-200">
          <ShieldAlert className="mt-0.5 h-4 w-4 shrink-0 text-[#06B6D4]" aria-hidden="true" />
          <span>{t.url.ssrfNote}</span>
        </div>
        <div className="flex items-start gap-2.5 rounded-xl border border-amber-500/30 bg-amber-500/5 p-3.5 text-xs text-amber-200">
          <Info className="mt-0.5 h-4 w-4 shrink-0 text-amber-400" aria-hidden="true" />
          <span>{t.url.httpsNote}</span>
        </div>
      </div>

      <Card>
        <CardContent className="space-y-4">
          {samples.length > 0 && (
            <div>
              <div className="mb-2 flex items-center gap-1.5 text-xs font-medium text-[#06B6D4]">
                <FlaskConical className="h-3.5 w-3.5" aria-hidden="true" />
                <span>Sample URLs (Demonstration):</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {samples.map((s) => (
                  <button
                    key={s.id}
                    type="button"
                    onClick={() => {
                      setUrlInput(s.url);
                      setError(null);
                    }}
                    className="rounded-lg border border-slate-700/80 bg-[#10182B] px-2.5 py-1.5 text-xs text-slate-200 hover:border-[#06B6D4]"
                  >
                    {s.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

          <form onSubmit={handleScan} className="flex flex-col gap-3 sm:flex-row sm:items-end">
            <div className="flex-1">
              <label htmlFor="url-input" className="block text-xs font-medium text-slate-300">
                {t.url.inputLabel}
              </label>
              <input
                id="url-input"
                type="text"
                required
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="https://example-portal.com/login"
                className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3.5 py-2.5 font-mono text-sm text-white placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
              />
            </div>
            <div className="flex flex-wrap gap-2">
              <Button
                type="button"
                variant="ghost"
                size="lg"
                onClick={() => {
                  setUrlInput("");
                  setError(null);
                }}
              >
                <span>{language === "bn" ? "মুছুন" : "Clear"}</span>
              </Button>
              <Button type="submit" size="lg" disabled={loading}>
                <Link2 className="h-4 w-4" aria-hidden="true" />
                <span>{loading ? t.url.scanning : t.url.scanBtn}</span>
              </Button>
            </div>
          </form>

          {recentScans.length > 0 && (
            <div className="border-t border-slate-800/80 pt-3">
              <div className="mb-2 flex items-center gap-1.5 text-xs font-medium text-slate-400">
                <Clock className="h-3.5 w-3.5 text-[#06B6D4]" aria-hidden="true" />
                <span>Recent URL Inspections</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {recentScans.slice(0, 5).map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => {
                      setResult(item);
                      setUrlInput(item.submitted_url);
                      setSearchParams({ id: String(item.id) }, { replace: true });
                    }}
                    className={`rounded-lg border px-2.5 py-1 text-[11px] transition-colors ${
                      result?.id === item.id
                        ? "border-[#06B6D4] bg-[#06B6D4]/15 text-white"
                        : "border-slate-800 bg-[#10182B] text-slate-300 hover:border-slate-700"
                    }`}
                  >
                    <span className="font-mono">{item.normalized_host}</span> • {item.risk_score}/100
                  </button>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {result && (
        <div className="grid gap-6 lg:grid-cols-12">
          <Card className="lg:col-span-5">
            <CardHeader>
              <h3 className="text-sm font-semibold text-slate-100">URL Risk Summary</h3>
              <Button size="sm" variant="secondary" onClick={handleDownloadPdf} disabled={pdfLoading}>
                <Download className="h-3.5 w-3.5" aria-hidden="true" />
                <span>{pdfLoading ? "Exporting..." : "PDF Report"}</span>
              </Button>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-col items-center gap-4 rounded-xl border border-slate-800 bg-[#10182B] p-5 text-center">
                <ProgressRing
                  value={result.risk_score}
                  colorHex={getRiskColor(result.risk_category).hex}
                  label="URL Risk Score"
                  sublabel="/ 100 Risk"
                />
                <div className="flex flex-wrap items-center justify-center gap-2">
                  <RiskBadge category={result.risk_category} />
                  {result.verdict_classification && (
                    <span
                      className={`inline-flex items-center rounded-md border px-2 py-0.5 text-[11px] font-semibold ${
                        result.verdict_classification === "Malicious"
                          ? "border-red-500/40 bg-red-500/15 text-red-300"
                          : result.verdict_classification === "Suspicious"
                          ? "border-amber-500/40 bg-amber-500/15 text-amber-300"
                          : result.verdict_classification === "Safe-Looking"
                          ? "border-emerald-500/40 bg-emerald-500/15 text-emerald-300"
                          : "border-slate-600 bg-slate-800/70 text-slate-300"
                      }`}
                    >
                      Verdict: {result.verdict_classification}
                    </span>
                  )}
                </div>
                <div className="w-full rounded-lg border border-slate-800 bg-[#080D1B]/80 px-3 py-2 text-xs text-slate-200">
                  <span className="font-semibold text-cyan-300">
                    {language === "bn" ? "খোলা নিরাপদ?" : "Safe to Open?"}{" "}
                  </span>
                  <span>
                    {result.verdict_classification === "Malicious"
                      ? language === "bn"
                        ? "না — এই লিংকটি ক্ষতিকর বা প্রতারণামূলক হতে পারে, খুলবেন না।"
                        : "No — Avoid opening this link or entering passwords/UPI details."
                      : result.verdict_classification === "Suspicious"
                      ? language === "bn"
                        ? "সাবধান — সন্দেহজনক লক্ষণ আছে, সরাসরি অফিশিয়াল সাইট ব্যবহার করুন।"
                        : "Caution — Suspicious signs detected. Visit the official site manually instead."
                      : result.verdict_classification === "Safe-Looking"
                      ? language === "bn"
                        ? "সাধারণভাবে নিরাপদ মনে হচ্ছে — তবুও অফিশিয়াল ডোমেইন নাম মিলিয়ে নিন।"
                        : "Looks relatively safe — Still verify the exact spelling of the domain."
                      : language === "bn"
                      ? "অজানা — পুরো তথ্য মেলেনি, ব্যক্তিগত তথ্য দেওয়ার আগে যাচাই করুন।"
                      : "Unknown — Insufficient signals. Confirm before entering credentials."}
                  </span>
                </div>
                <div className="w-full space-y-1 text-left text-xs">
                  <div className="text-slate-400">Normalized Host</div>
                  <div className="break-all font-mono text-slate-100">{result.normalized_host}</div>
                  <div className="pt-1 text-slate-400">Engine</div>
                  <div className="font-mono text-[11px] text-[#06B6D4]">{result.reputation_source}</div>
                </div>
              </div>

              {/* Staff WhatsApp Emergency Alert */}
              {result.risk_score >= 30 && (
                <div className="rounded-xl border border-emerald-500/30 bg-gradient-to-r from-emerald-950/30 via-[#10182B] to-[#10182B] p-3.5 text-xs">
                  <div className="flex items-center gap-2">
                    <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-[#25D366]/20 text-[#25D366]">
                      <MessageSquare className="h-3.5 w-3.5" aria-hidden="true" />
                    </span>
                    <div>
                      <div className="font-semibold text-emerald-300">
                        {language === "bn" ? "দোকানের কর্মচারীদের WhatsApp সতর্কবার্তা" : "Staff WhatsApp Alert"}
                      </div>
                      <div className="text-[10px] text-slate-400">
                        {language === "bn" ? "কাউন্টার স্টাফদের দ্রুত সতর্ক করতে" : "Alert counter staff instantly"}
                      </div>
                    </div>
                  </div>

                  <div className="mt-2.5 flex flex-wrap gap-2">
                    <Button
                      type="button"
                      size="sm"
                      variant="secondary"
                      onClick={handleCopyStaffWarning}
                      className="border-emerald-500/40 bg-emerald-500/10 text-emerald-200 hover:bg-emerald-500/20"
                    >
                      {copiedWarning ? (
                        <>
                          <Check className="h-3.5 w-3.5 text-emerald-400" aria-hidden="true" />
                          <span>{language === "bn" ? "কপি হয়েছে!" : "Copied!"}</span>
                        </>
                      ) : (
                        <>
                          <Copy className="h-3.5 w-3.5" aria-hidden="true" />
                          <span>{language === "bn" ? "Copy Warning" : "Copy Warning"}</span>
                        </>
                      )}
                    </Button>

                    <a
                      href={getWhatsAppShareUrl()}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 rounded-lg bg-[#25D366] px-2.5 py-1 text-xs font-semibold text-black transition-opacity hover:opacity-90"
                    >
                      <Share2 className="h-3 w-3" aria-hidden="true" />
                      <span>{language === "bn" ? "WhatsApp শেয়ার" : "Share"}</span>
                    </a>
                  </div>

                  <div className="mt-2.5 rounded-lg border border-slate-800 bg-[#080D1B] p-2.5 font-mono text-[10px] leading-relaxed text-slate-300 whitespace-pre-line">
                    {getStaffWarningMessage()}
                  </div>
                </div>
              )}

              <div className="rounded-xl border border-slate-800 bg-[#10182B] p-4 text-xs">
                <div className="mb-2 font-semibold text-slate-200">DNS & Email Authentication</div>
                <div className="space-y-1.5 text-slate-300">
                  <div className="flex justify-between">
                    <span className="text-slate-400">SPF TXT Record:</span>
                    <span className={result.dns_records.spf_present ? "text-emerald-400" : "text-amber-300"}>
                      {result.dns_records.spf_present ? "Present" : "Not Found"}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">DMARC TXT Record:</span>
                    <span className={result.dns_records.dmarc_present ? "text-emerald-400" : "text-amber-300"}>
                      {result.dns_records.dmarc_present ? "Present" : "Not Found"}
                    </span>
                  </div>
                  {result.dns_records.a_records && result.dns_records.a_records.length > 0 && (
                    <div className="pt-1 text-[11px] text-slate-400">
                      Resolved A: {result.dns_records.a_records.join(", ")}
                    </div>
                  )}
                </div>
              </div>

              {result.tls_info && (
                <div className="rounded-xl border border-slate-800 bg-[#10182B] p-4 text-xs">
                  <div className="mb-2 font-semibold text-slate-200">X.509 TLS Certificate Metadata</div>
                  {result.tls_info.tls_status === "valid_certificate_read" ? (
                    <div className="space-y-1.5 text-slate-300">
                      <div className="flex justify-between gap-2">
                        <span className="text-slate-400">Issuer:</span>
                        <span className="truncate font-mono text-[11px] text-emerald-300">
                          {result.tls_info.issuer_org || "Verified CA"}
                        </span>
                      </div>
                      <div className="flex justify-between gap-2">
                        <span className="text-slate-400">Subject CN:</span>
                        <span className="truncate font-mono text-[11px] text-slate-200">
                          {result.tls_info.subject_cn || result.normalized_host}
                        </span>
                      </div>
                      {result.tls_info.not_after && (
                        <div className="flex justify-between gap-2">
                          <span className="text-slate-400">Valid Until:</span>
                          <span className="font-mono text-[11px] text-slate-300">
                            {result.tls_info.not_after}
                          </span>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-[11px] text-slate-400">
                      {result.tls_info.tls_status === "skipped_http_or_ip"
                        ? "Skipped (URL uses plain HTTP or raw IP instead of HTTPS)."
                        : result.tls_info.tls_status === "verification_warning"
                        ? `TLS Verification Warning: ${result.tls_info.detail || "Untrusted or mismatched certificate."}`
                        : `TLS Status: ${(result.tls_info.tls_status || "unavailable").replace(/_/g, " ")}`}
                    </p>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="lg:col-span-7">
            <CardHeader>
              <h3 className="text-sm font-semibold text-slate-100">Detected Indicators & Technical Explanation</h3>
            </CardHeader>
            <CardContent className="space-y-5">
              <p className="rounded-xl border border-slate-800 bg-[#10182B] p-3.5 text-xs leading-relaxed text-slate-200">
                {result.technical_explanation}
              </p>

              <div className="space-y-2.5">
                {result.indicators.map((ind, idx) => (
                  <div
                    key={`${ind.code}-${idx}`}
                    className="rounded-xl border border-slate-800 bg-[#10182B] p-3.5"
                  >
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-xs font-semibold text-slate-100">{ind.label}</span>
                      <div className="flex items-center gap-2">
                        {ind.score_impact > 0 && (
                          <span className="font-mono text-[11px] text-amber-300">
                            +{ind.score_impact} pts
                          </span>
                        )}
                        <RiskBadge category={ind.severity} />
                      </div>
                    </div>
                    <p className="mt-1.5 text-xs text-slate-400">{ind.detail}</p>
                  </div>
                ))}
              </div>

              <div>
                <h4 className="mb-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Security Recommendations
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
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}

