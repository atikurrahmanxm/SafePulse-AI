import React, { useCallback, useEffect, useState } from "react";
import {
  CheckSquare,
  Download,
  Info,
  KeyRound,
  Plus,
  ShieldCheck,
  Square,
  Trash2,
  Users,
} from "lucide-react";
import { useLanguage } from "../i18n/LanguageContext";
import { apiRequest, ApiError, downloadPdfReport } from "../lib/api";
import {
  Button,
  Card,
  CardContent,
  CardHeader,
  ErrorBanner,
  Skeleton,
} from "../components/ui/Primitives";

interface MemberItem {
  id: number;
  full_name: string;
  email: string;
  role: string;
  department: string;
  mfa_enabled: boolean;
  awareness_trained: boolean;
  created_at: string;
}

interface ControlItem {
  id: number;
  category: "backup" | "updates" | "policy" | "roadmap" | string;
  control_key: string;
  title: string;
  guidance: string;
  priority: string;
  is_completed: boolean;
  owner_name?: string | null;
  target_date?: string | null;
  last_verified_at?: string | null;
}

interface GovernanceOverview {
  mfa_stats: {
    total_members: number;
    mfa_enabled_count: number;
    mfa_adoption_percent: number;
    awareness_trained_count: number;
  };
  controls_stats: {
    completed_count: number;
    total_count: number;
    completion_percent: number;
  };
  members: MemberItem[];
  controls: ControlItem[];
}

const CATEGORY_TABS = [
  { key: "all", label: "All Controls" },
  { key: "backup", label: "Backup" },
  { key: "updates", label: "Software Updates" },
  { key: "policy", label: "Policies" },
  { key: "roadmap", label: "Roadmap" },
] as const;

export function GovernancePage() {
  const { language, t } = useLanguage();
  const [data, setData] = useState<GovernanceOverview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeCategory, setActiveCategory] = useState<string>("all");
  const [pdfLoading, setPdfLoading] = useState(false);

  // Add Member Form
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState<"owner" | "manager" | "staff">("staff");
  const [department, setDepartment] = useState("Operations");
  const [mfaEnabled, setMfaEnabled] = useState(false);
  const [addingMember, setAddingMember] = useState(false);

  const loadGovernance = useCallback(async () => {
    try {
      const res = await apiRequest<GovernanceOverview>(
        `/api/governance/overview?language=${language}`
      );
      setData(res);
      setError(null);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to load governance posture.");
    } finally {
      setLoading(false);
    }
  }, [language]);

  useEffect(() => {
    setLoading(true);
    loadGovernance();
  }, [loadGovernance]);

  const handleAddMember = async (e: React.FormEvent) => {
    e.preventDefault();
    setAddingMember(true);
    setError(null);
    try {
      await apiRequest<MemberItem>("/api/governance/members", {
        method: "POST",
        body: JSON.stringify({
          full_name: fullName.trim(),
          email: email.trim(),
          role,
          department: department.trim() || "General",
          mfa_enabled: mfaEnabled,
          awareness_trained: false,
        }),
      });
      setFullName("");
      setEmail("");
      setMfaEnabled(false);
      await loadGovernance();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not add team member.");
    } finally {
      setAddingMember(false);
    }
  };

  const handleToggleMember = async (
    member: MemberItem,
    field: "mfa_enabled" | "awareness_trained"
  ) => {
    try {
      await apiRequest<MemberItem>(`/api/governance/members/${member.id}`, {
        method: "PATCH",
        body: JSON.stringify({ [field]: !member[field] }),
      });
      await loadGovernance();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to update team member.");
    }
  };

  const handleDeleteMember = async (memberId: number) => {
    try {
      await apiRequest(`/api/governance/members/${memberId}`, { method: "DELETE" });
      await loadGovernance();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to remove team member.");
    }
  };

  const handleToggleControl = async (ctrl: ControlItem) => {
    try {
      await apiRequest<ControlItem>(`/api/governance/controls/${ctrl.id}`, {
        method: "PATCH",
        body: JSON.stringify({ is_completed: !ctrl.is_completed }),
      });
      await loadGovernance();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to update checklist item.");
    }
  };

  const handleMonthlyPdf = async () => {
    setPdfLoading(true);
    try {
      await downloadPdfReport(
        `/api/reports/monthly.pdf?language=${language}`,
        `safepulse-monthly-report-${language}.pdf`
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to download monthly PDF report.");
    } finally {
      setPdfLoading(false);
    }
  };

  if (loading) {
    return <Skeleton className="h-96" />;
  }

  const members = data?.members ?? [];
  const controls = data?.controls ?? [];
  const filteredControls =
    activeCategory === "all"
      ? controls
      : controls.filter((c) => c.category === activeCategory);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-50">{t.governance.title}</h2>
          <p className="mt-1 text-sm text-slate-400">{t.governance.subtitle}</p>
        </div>
        <Button size="sm" variant="secondary" onClick={handleMonthlyPdf} disabled={pdfLoading}>
          <Download className="h-3.5 w-3.5 text-[#06B6D4]" aria-hidden="true" />
          <span>{pdfLoading ? "Exporting..." : t.dashboard.monthlyReport}</span>
        </Button>
      </div>

      <div className="flex items-start gap-2.5 rounded-xl border border-amber-500/35 bg-amber-500/10 p-3.5 text-xs text-amber-200">
        <Info className="mt-0.5 h-4 w-4 shrink-0 text-amber-400" aria-hidden="true" />
        <span>{t.governance.manualNotice}</span>
      </div>

      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}

      {/* KPI Cards */}
      <div className="grid gap-4 sm:grid-cols-3">
        <Card>
          <CardContent>
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Staff MFA Adoption</span>
              <KeyRound className="h-4 w-4 text-[#06B6D4]" aria-hidden="true" />
            </div>
            <div className="mt-2 text-3xl font-bold text-cyan-300">
              {data?.mfa_stats.mfa_adoption_percent ?? 0}%
            </div>
            <p className="mt-1 text-xs text-slate-400">
              {data?.mfa_stats.mfa_enabled_count ?? 0} of {data?.mfa_stats.total_members ?? 0} staff protected
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Security Controls Completed</span>
              <ShieldCheck className="h-4 w-4 text-emerald-400" aria-hidden="true" />
            </div>
            <div className="mt-2 text-3xl font-bold text-emerald-400">
              {data?.controls_stats.completion_percent ?? 0}%
            </div>
            <p className="mt-1 text-xs text-slate-400">
              {data?.controls_stats.completed_count ?? 0} of {data?.controls_stats.total_count ?? 0} controls verified
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Awareness Trained Staff</span>
              <Users className="h-4 w-4 text-[#6366F1]" aria-hidden="true" />
            </div>
            <div className="mt-2 text-3xl font-bold text-slate-100">
              {data?.mfa_stats.awareness_trained_count ?? 0}
            </div>
            <p className="mt-1 text-xs text-slate-400">Out of {data?.mfa_stats.total_members ?? 0} team members</p>
          </CardContent>
        </Card>
      </div>

      {/* Team & MFA Adoption Directory */}
      <div className="grid gap-6 lg:grid-cols-12">
        <Card className="lg:col-span-5">
          <CardHeader>
            <h3 className="text-sm font-semibold text-slate-100">Add Team Member & MFA Record</h3>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleAddMember} className="space-y-3">
              <div>
                <label htmlFor="gov-name" className="block text-xs font-medium text-slate-300">
                  Full Name
                </label>
                <input
                  id="gov-name"
                  type="text"
                  required
                  minLength={2}
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="e.g., Priya Kalita"
                  className="mt-1 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-xs text-white"
                />
              </div>

              <div>
                <label htmlFor="gov-email" className="block text-xs font-medium text-slate-300">
                  Work Email
                </label>
                <input
                  id="gov-email"
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="e.g., priya@shop.in"
                  className="mt-1 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-xs text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label htmlFor="gov-role" className="block text-xs font-medium text-slate-300">
                    Role
                  </label>
                  <select
                    id="gov-role"
                    value={role}
                    onChange={(e) => setRole(e.target.value as typeof role)}
                    className="mt-1 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-2.5 py-2 text-xs text-white"
                  >
                    <option value="owner">Owner / Admin</option>
                    <option value="manager">Manager / Lead</option>
                    <option value="staff">Staff / Billing / Operations</option>
                  </select>
                </div>
                <div>
                  <label htmlFor="gov-dept" className="block text-xs font-medium text-slate-300">
                    Department
                  </label>
                  <input
                    id="gov-dept"
                    type="text"
                    value={department}
                    onChange={(e) => setDepartment(e.target.value)}
                    placeholder="Billing / Pharmacy"
                    className="mt-1 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-xs text-white"
                  />
                </div>
              </div>

              <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer pt-1">
                <input
                  type="checkbox"
                  checked={mfaEnabled}
                  onChange={(e) => setMfaEnabled(e.target.checked)}
                  className="accent-[#06B6D4]"
                />
                <span>2FA / Authenticator MFA enabled on work account</span>
              </label>

              <Button type="submit" className="w-full" disabled={addingMember}>
                <Plus className="h-4 w-4" aria-hidden="true" />
                <span>{addingMember ? "Adding..." : "Add Team Member"}</span>
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card className="lg:col-span-7">
          <CardHeader>
            <h3 className="text-sm font-semibold text-slate-100">
              Employee Role & MFA Directory ({members.length})
            </h3>
          </CardHeader>
          <CardContent className="space-y-2.5">
            {members.length === 0 ? (
              <p className="py-6 text-center text-xs text-slate-400">
                No team members tracked yet. Add your staff on the left to monitor MFA adoption.
              </p>
            ) : (
              members.map((m) => (
                <div
                  key={m.id}
                  className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-800 bg-[#10182B] px-3.5 py-2.5 text-xs"
                >
                  <div className="min-w-0">
                    <div className="font-semibold text-slate-100">
                      {m.full_name}{" "}
                      <span className="ml-1 rounded bg-slate-800 px-1.5 py-0.5 text-[10px] text-slate-300">
                        {m.role}
                      </span>
                    </div>
                    <div className="truncate text-[11px] text-slate-400">
                      {m.email} • {m.department}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => handleToggleMember(m, "mfa_enabled")}
                      className={`rounded-md border px-2 py-1 text-[11px] font-medium transition-colors ${
                        m.mfa_enabled
                          ? "border-emerald-500/40 bg-emerald-500/15 text-emerald-300"
                          : "border-red-500/40 bg-red-500/10 text-red-300"
                      }`}
                    >
                      MFA: {m.mfa_enabled ? "ON" : "OFF"}
                    </button>
                    <button
                      type="button"
                      onClick={() => handleToggleMember(m, "awareness_trained")}
                      className={`rounded-md border px-2 py-1 text-[11px] font-medium transition-colors ${
                        m.awareness_trained
                          ? "border-cyan-500/40 bg-cyan-500/15 text-cyan-200"
                          : "border-slate-700 bg-slate-800/70 text-slate-400"
                      }`}
                    >
                      {m.awareness_trained ? "Trained" : "Untrained"}
                    </button>
                    <button
                      type="button"
                      onClick={() => handleDeleteMember(m.id)}
                      aria-label={`Remove ${m.full_name}`}
                      className="rounded-md p-1.5 text-slate-400 hover:bg-red-500/10 hover:text-red-300"
                    >
                      <Trash2 className="h-3.5 w-3.5" aria-hidden="true" />
                    </button>
                  </div>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>

      {/* Backup, Software Updates, Security Policies & Improvement Roadmap */}
      <Card>
        <CardHeader className="flex-wrap gap-3">
          <div>
            <h3 className="text-sm font-semibold text-slate-100">
              Backup, Software Updates, Policies & Security Roadmap
            </h3>
            <p className="text-xs text-slate-400">
              Check off verified safeguards as your shop or office implements them.
            </p>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {CATEGORY_TABS.map((tab) => (
              <button
                key={tab.key}
                type="button"
                onClick={() => setActiveCategory(tab.key)}
                className={`rounded-lg border px-2.5 py-1 text-xs font-medium transition-colors ${
                  activeCategory === tab.key
                    ? "border-[#6366F1] bg-[#6366F1]/20 text-white"
                    : "border-slate-800 bg-[#10182B] text-slate-400 hover:text-slate-200"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </CardHeader>
        <CardContent className="grid gap-3 md:grid-cols-2">
          {filteredControls.map((ctrl) => (
            <button
              key={ctrl.id}
              type="button"
              onClick={() => handleToggleControl(ctrl)}
              className={`flex items-start gap-3 rounded-xl border p-3.5 text-left transition-colors ${
                ctrl.is_completed
                  ? "border-emerald-500/35 bg-emerald-500/10"
                  : "border-slate-800 bg-[#10182B] hover:border-slate-700"
              }`}
            >
              {ctrl.is_completed ? (
                <CheckSquare className="mt-0.5 h-5 w-5 shrink-0 text-emerald-400" aria-hidden="true" />
              ) : (
                <Square className="mt-0.5 h-5 w-5 shrink-0 text-slate-400" aria-hidden="true" />
              )}
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="rounded bg-slate-800 px-1.5 py-0.5 font-mono text-[10px] uppercase text-[#06B6D4]">
                    {ctrl.category}
                  </span>
                  <span
                    className={`rounded px-1.5 py-0.5 text-[10px] font-semibold ${
                      ctrl.priority === "High"
                        ? "bg-red-500/15 text-red-300"
                        : "bg-amber-500/15 text-amber-300"
                    }`}
                  >
                    {ctrl.priority}
                  </span>
                </div>
                <div
                  className={`mt-1 text-xs font-semibold ${
                    ctrl.is_completed ? "line-through text-slate-400" : "text-slate-100"
                  }`}
                >
                  {ctrl.title}
                </div>
                <p className="mt-1 text-[11px] leading-relaxed text-slate-300">{ctrl.guidance}</p>
              </div>
            </button>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}

