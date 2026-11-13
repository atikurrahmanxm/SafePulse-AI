import { useNavigate } from "react-router-dom";
import { BookOpen, ExternalLink, PhoneCall, PlayCircle, Shield } from "lucide-react";
import { useLanguage } from "../i18n/LanguageContext";
import { Button, Card, CardContent, CardHeader } from "../components/ui/Primitives";

export function DocsPage() {
  const navigate = useNavigate();
  const { t } = useLanguage();

  const scenarios = [
    {
      num: "Scenario 1",
      title: "Suspicious Bank Verification Message",
      desc: "Open the Phishing Detector, load 'Scenario 1 (Demo): Bank Account Verification Scam', and inspect the risk ring, highlighted urgency/credential phrases, and PDF export.",
      cta: "Open Phishing Detector",
      to: "/app/phishing",
    },
    {
      num: "Scenario 2",
      title: "Suspicious Website URL Inspection",
      desc: "Open the URL Security Scanner, submit 'http://sbi-kyc-verify-portal.xyz/netbanking/login?verify=otp', and review SSRF protection, brand impersonation indicators, and DNS SPF/DMARC checks.",
      cta: "Open URL Scanner",
      to: "/app/url-scanner",
    },
    {
      num: "Scenario 3",
      title: "Business Security Health Check",
      desc: "Open Business Security Assessment to review or update the 10-domain CERT-In MSME questionnaire, view weak areas and critical gaps, and export a PDF action plan.",
      cta: "Open Assessment",
      to: "/app/assessment",
    },
    {
      num: "Scenario 4",
      title: "Employee Clicks a Phishing Link",
      desc: "Open the Incident Response Center, select 'Phishing Link Clicked', mark immediate containment actions completed, and track live progress.",
      cta: "Open Incident Center",
      to: "/app/incidents",
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-lg font-bold text-slate-50">{t.docs.title}</h2>
        <p className="mt-1 text-sm text-slate-400">
          {t.docs.subtitle}
        </p>
      </div>

      {/* Emergency Contacts */}
      <Card className="border-red-500/30 bg-red-500/5">
        <CardHeader>
          <div className="flex items-center gap-2">
            <PhoneCall className="h-4 w-4 text-red-400" aria-hidden="true" />
            <h3 className="text-sm font-semibold text-red-200">
              India Cyber Incident Emergency Contacts
            </h3>
          </div>
        </CardHeader>
        <CardContent className="grid gap-4 sm:grid-cols-3 text-xs">
          <div className="rounded-lg border border-slate-800 bg-[#10182B] p-3">
            <div className="font-semibold text-slate-100">National Cyber Crime Helpline</div>
            <div className="mt-1 font-mono text-base font-bold text-[#06B6D4]">Dial 1930</div>
            <p className="mt-1 text-slate-400">Call immediately during financial/UPI fraud golden hour.</p>
          </div>
          <div className="rounded-lg border border-slate-800 bg-[#10182B] p-3">
            <div className="font-semibold text-slate-100">National Cyber Crime Portal</div>
            <a
              href="https://cybercrime.gov.in"
              target="_blank"
              rel="noreferrer"
              className="mt-1 inline-flex items-center gap-1 font-mono text-sm text-[#06B6D4] hover:underline"
            >
              <span>cybercrime.gov.in</span>
              <ExternalLink className="h-3 w-3" aria-hidden="true" />
            </a>
            <p className="mt-1 text-slate-400">Official Ministry of Home Affairs reporting portal.</p>
          </div>
          <div className="rounded-lg border border-slate-800 bg-[#10182B] p-3">
            <div className="font-semibold text-slate-100">CERT-In Incident Desk</div>
            <a
              href="https://www.cert-in.org.in"
              target="_blank"
              rel="noreferrer"
              className="mt-1 inline-flex items-center gap-1 font-mono text-sm text-[#06B6D4] hover:underline"
            >
              <span>cert-in.org.in</span>
              <ExternalLink className="h-3 w-3" aria-hidden="true" />
            </a>
            <p className="mt-1 text-slate-400">MSME advisories & incident@cert-in.org.in reporting.</p>
          </div>
        </CardContent>
      </Card>

      {/* 4 Hackathon Demo Scenarios */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <PlayCircle className="h-4 w-4 text-[#6366F1]" aria-hidden="true" />
            <h3 className="text-sm font-semibold text-slate-100">
              Hackathon Presentation Mode — 4 Live Scenarios (Demonstration)
            </h3>
          </div>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-2">
          {scenarios.map((s) => (
            <div
              key={s.num}
              className="flex flex-col justify-between rounded-xl border border-slate-800 bg-[#10182B] p-4"
            >
              <div>
                <div className="font-mono text-[11px] font-semibold text-[#06B6D4]">{s.num}</div>
                <h4 className="mt-1 text-sm font-semibold text-slate-100">{s.title}</h4>
                <p className="mt-1.5 text-xs leading-relaxed text-slate-400">{s.desc}</p>
              </div>
              <div className="mt-4">
                <Button size="sm" variant="secondary" onClick={() => navigate(s.to)}>
                  {s.cta}
                </Button>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Responsible AI & Limitations */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4 text-emerald-400" aria-hidden="true" />
            <h3 className="text-sm font-semibold text-slate-100">Responsible AI & Scope Limitations</h3>
          </div>
        </CardHeader>
        <CardContent className="space-y-2 text-xs leading-relaxed text-slate-300">
          <p className="flex items-start gap-2">
            <BookOpen className="mt-0.5 h-3.5 w-3.5 shrink-0 text-[#06B6D4]" aria-hidden="true" />
            <span>
              <strong>Risk Bands (0–24 Low, 25–49 Moderate, 50–74 High, 75–100 Critical):</strong> These are CyberShield AI application triage thresholds, not universal security certifications.
            </span>
          </p>
          <p className="flex items-start gap-2">
            <BookOpen className="mt-0.5 h-3.5 w-3.5 shrink-0 text-[#06B6D4]" aria-hidden="true" />
            <span>
              <strong>Offline-First Architecture:</strong> All core detection, scoring, and PDF generation run locally without requiring paid third-party threat feeds.
            </span>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

