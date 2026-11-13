import React, { useCallback, useEffect, useState } from "react";
import {
  Building2,
  CheckCircle2,
  CreditCard,
  Info,
  PlugZap,
  Plus,
  Save,
  ShieldCheck,
} from "lucide-react";
import { useAuth, UserProfile } from "../context/AuthContext";
import { useLanguage } from "../i18n/LanguageContext";
import { apiRequest, ApiError } from "../lib/api";
import { Button, Card, CardContent, CardHeader, ErrorBanner } from "../components/ui/Primitives";

interface IntegrationItem {
  provider_key: string;
  name: string;
  category: string;
  description: string;
  requires_external_oauth: boolean;
  enabled: boolean;
  endpoint_or_account?: string | null;
  notes?: string | null;
  runtime_status: "active_server_env" | "configured_awaiting_oauth_gateway" | "unconfigured" | string;
}

interface SubscriptionPlan {
  key?: string;
  tier?: string;
  name: string;
  monthly_scan_quota: number;
  max_workspaces?: number;
  max_businesses?: number;
  features: string[];
}

type SettingsTab = "plan" | "integrations" | "safeguards";

export function SettingsPage() {
  const { user, setUserDirect, switchBusiness, createBusiness, workspaceNotice, clearWorkspaceNotice } = useAuth();
  const { language, setLanguage, t } = useLanguage();
  const isBn = language === "bn";

  const [name, setName] = useState(user?.business.name || "");
  const [industry, setIndustry] = useState(user?.business.industry || "Retail & Local Shop");
  const [employeeCount, setEmployeeCount] = useState(user?.business.employee_count || 5);
  const [city, setCity] = useState(user?.business.city || "Guwahati");
  const [domain, setDomain] = useState(user?.business.primary_email_domain || "");
  const [subscriptionTier, setSubscriptionTier] = useState(
    user?.business.subscription_tier || "free"
  );
  const [prefLang, setPrefLang] = useState<"en" | "bn">(language);
  const [saving, setSaving] = useState(false);
  const [savedMsg, setSavedMsg] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<SettingsTab>("plan");

  // Additional Workspace Form
  const [newBizName, setNewBizName] = useState("");
  const [newBizIndustry, setNewBizIndustry] = useState("Pharmacy / Healthcare");
  const [newBizCity, setNewBizCity] = useState("Guwahati");
  const [creatingBiz, setCreatingBiz] = useState(false);

  // Governance SaaS Subscription + Integrations
  const [integrations, setIntegrations] = useState<IntegrationItem[]>([]);
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [monthlyScansUsed, setMonthlyScansUsed] = useState(0);
  const [monthlyQuota, setMonthlyQuota] = useState(user?.business.monthly_scan_quota || 100);
  const [savingIntegrationKey, setSavingIntegrationKey] = useState<string | null>(null);

  const loadGovernanceConfig = useCallback(async () => {
    try {
      const res = await apiRequest<{
        integrations?: IntegrationItem[];
        available_plans?: SubscriptionPlan[];
        subscription?: { monthly_scans_used?: number; monthly_scan_quota?: number };
      }>(`/api/governance/overview?language=${language}`);
      if (Array.isArray(res.integrations)) setIntegrations(res.integrations);
      if (Array.isArray(res.available_plans)) setPlans(res.available_plans);
      if (res.subscription) {
        setMonthlyScansUsed(res.subscription.monthly_scans_used ?? 0);
        setMonthlyQuota(res.subscription.monthly_scan_quota ?? 100);
      }
    } catch {
      // Optional SaaS config load
    }
  }, [language]);

  useEffect(() => {
    loadGovernanceConfig();
  }, [loadGovernanceConfig, user?.business?.id]);

  useEffect(() => {
    if (user?.business) {
      setName(user.business.name || "");
      setIndustry(user.business.industry || "Retail & Local Shop");
      setEmployeeCount(user.business.employee_count || 5);
      setCity(user.business.city || "Guwahati");
      setDomain(user.business.primary_email_domain || "");
      setSubscriptionTier(user.business.subscription_tier || "free");
      setMonthlyQuota(user.business.monthly_scan_quota || 100);
    }
  }, [user]);

  useEffect(() => {
    setPrefLang(language);
  }, [language]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSavedMsg(null);
    setSaving(true);
    try {
      const updated = await apiRequest<UserProfile>("/api/auth/business", {
        method: "PUT",
        body: JSON.stringify({
          name,
          industry,
          employee_count: Number(employeeCount) || 1,
          city,
          primary_email_domain: domain.trim() || null,
          subscription_tier: subscriptionTier,
          preferred_language: prefLang,
        }),
      });
      setUserDirect(updated);
      setLanguage(prefLang);
      setSavedMsg("Business profile, subscription plan, and preferences updated.");
      await loadGovernanceConfig();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to save settings.");
    } finally {
      setSaving(false);
    }
  };

  const handleCreateBusiness = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSavedMsg(null);
    clearWorkspaceNotice?.();
    setCreatingBiz(true);
    try {
      const created = await createBusiness({
        name: newBizName.trim(),
        industry: newBizIndustry,
        employee_count: 5,
        city: newBizCity.trim() || "Guwahati",
      });
      setNewBizName("");
      setSavedMsg(`Switched to new business workspace: ${created.name}`);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not create business workspace.");
    } finally {
      setCreatingBiz(false);
    }
  };

  const handleSaveIntegration = async (item: IntegrationItem, nextEnabled: boolean, endpointVal?: string) => {
    setSavingIntegrationKey(item.provider_key);
    setError(null);
    try {
      const updated = await apiRequest<IntegrationItem>(
        `/api/governance/integrations/${item.provider_key}`,
        {
          method: "PUT",
          body: JSON.stringify({
            enabled: nextEnabled,
            endpoint_or_account: endpointVal ?? item.endpoint_or_account ?? null,
            notes: item.notes ?? null,
          }),
        }
      );
      setIntegrations((prev) =>
        prev.map((it) => (it.provider_key === updated.provider_key ? { ...it, ...updated } : it))
      );
      setSavedMsg(
        `${item.name} configuration saved (${updated.runtime_status.replace(/_/g, " ")}).`
      );
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Could not update integration configuration.");
    } finally {
      setSavingIntegrationKey(null);
    }
  };

  const usagePercent = Math.min(100, Math.round((monthlyScansUsed / Math.max(1, monthlyQuota)) * 100));

  return (
    <div className="min-w-0 space-y-6">
      {/* Page Header */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">{t.settings.title}</h2>
          <p className="mt-1 text-sm text-slate-400">{t.settings.subtitle}</p>
        </div>
        <span
          className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium ${
            user?.is_demo
              ? "border-cyan-500/35 bg-cyan-500/10 text-cyan-200"
              : "border-emerald-500/35 bg-emerald-500/10 text-emerald-200"
          }`}
        >
          <span
            className={`h-2 w-2 rounded-full ${user?.is_demo ? "bg-cyan-400" : "bg-emerald-400"}`}
            aria-hidden="true"
          />
          {user?.is_demo
            ? isBn
              ? "ডেমো অ্যাকাউন্ট মোড"
              : "Demo Workspace Mode"
            : isBn
            ? "লাইভ বিজনেস অ্যাকাউন্ট"
            : "Live Business Account"}
        </span>
      </div>

      {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
      {(savedMsg || workspaceNotice) && (
        <div className="flex items-center gap-2 rounded-xl border border-emerald-500/35 bg-emerald-500/10 px-4 py-3 text-xs text-emerald-200">
          <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-400" aria-hidden="true" />
          <span>{savedMsg || workspaceNotice}</span>
        </div>
      )}

      {/* Row 1: Business Profile (Left) + Workspaces & Branches (Right) */}
      <div className="grid min-w-0 gap-6 lg:grid-cols-12">
        <Card className="min-w-0 lg:col-span-7">
          <CardHeader>
            <div>
              <h3 className="text-sm font-semibold text-white">{t.settings.profileCard}</h3>
              <p className="text-xs text-slate-400">
                {isBn
                  ? "আপনার দোকান বা অফিসের নাম, ভাষা ও তথ্য হালনাগাদ করুন"
                  : "Update your shop or office details and default report language"}
              </p>
            </div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSave} className="space-y-4">
              <div>
                <label htmlFor="set-biz-name" className="block text-xs font-medium text-slate-300">
                  Business Name
                </label>
                <input
                  id="set-biz-name"
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white focus:border-[#6366F1] focus:outline-none"
                />
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label htmlFor="set-industry" className="block text-xs font-medium text-slate-300">
                    Industry
                  </label>
                  <input
                    id="set-industry"
                    type="text"
                    required
                    value={industry}
                    onChange={(e) => setIndustry(e.target.value)}
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white focus:border-[#6366F1] focus:outline-none"
                  />
                </div>
                <div>
                  <label htmlFor="set-city" className="block text-xs font-medium text-slate-300">
                    City
                  </label>
                  <input
                    id="set-city"
                    type="text"
                    required
                    value={city}
                    onChange={(e) => setCity(e.target.value)}
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white focus:border-[#6366F1] focus:outline-none"
                  />
                </div>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label htmlFor="set-emp" className="block text-xs font-medium text-slate-300">
                    Employee Count
                  </label>
                  <input
                    id="set-emp"
                    type="number"
                    min={1}
                    max={5000}
                    required
                    value={employeeCount}
                    onChange={(e) => setEmployeeCount(Number(e.target.value))}
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white focus:border-[#6366F1] focus:outline-none"
                  />
                </div>
                <div>
                  <label htmlFor="set-lang" className="block text-xs font-medium text-slate-300">
                    Default Language
                  </label>
                  <select
                    id="set-lang"
                    value={prefLang}
                    onChange={(e) => setPrefLang(e.target.value as "en" | "bn")}
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white focus:border-[#6366F1] focus:outline-none"
                  >
                    <option value="en">English (EN)</option>
                    <option value="bn">Bengali (বাংলা)</option>
                  </select>
                </div>
              </div>

              <div>
                <label htmlFor="set-domain" className="block text-xs font-medium text-slate-300">
                  Primary Business Email Domain (Optional)
                </label>
                <input
                  id="set-domain"
                  type="text"
                  value={domain}
                  onChange={(e) => setDomain(e.target.value)}
                  placeholder="e.g., myshop.in"
                  className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
                />
              </div>

              <div className="flex justify-end border-t border-slate-800/80 pt-4">
                <Button type="submit" disabled={saving}>
                  <Save className="h-4 w-4" aria-hidden="true" />
                  <span>{saving ? t.settings.savingBtn : t.settings.saveBtn}</span>
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        {/* Right Card: Branches & Multi-Business Workspaces */}
        <Card className="flex min-w-0 flex-col lg:col-span-5">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Building2 className="h-4 w-4 text-[#06B6D4]" aria-hidden="true" />
              <div>
                <h3 className="text-sm font-semibold text-white">
                  {isBn ? "শাখা ও ওয়ার্কস্পেস" : "Branches & Workspaces"} ({user?.businesses?.length ?? 1})
                </h3>
                <p className="text-xs text-slate-400">
                  {isBn ? "প্রতিটি শাখার ডেটা সম্পূর্ণ আলাদা থাকে" : "Switch or add separate shops"}
                </p>
              </div>
            </div>
          </CardHeader>
          <CardContent className="flex flex-1 flex-col justify-between gap-4">
            {Array.isArray(user?.businesses) && user.businesses.length > 0 && (
              <div className="max-h-52 space-y-2 overflow-y-auto pr-1">
                {user.businesses.map((biz) => {
                  const active = biz.id === user.business.id;
                  return (
                    <div
                      key={biz.id}
                      className={`flex items-center justify-between gap-2 rounded-xl border px-3 py-2.5 text-xs ${
                        active
                          ? "border-indigo-500/50 bg-indigo-500/15 text-white"
                          : "border-slate-800 bg-[#0B1224] text-slate-300"
                      }`}
                    >
                      <div className="min-w-0">
                        <div className="truncate font-semibold">{biz.name}</div>
                        <div className="truncate text-[11px] text-slate-400">
                          {biz.industry} • {biz.city}
                        </div>
                      </div>
                      {active ? (
                        <span className="shrink-0 rounded-full border border-emerald-500/35 bg-emerald-500/15 px-2.5 py-0.5 text-[10px] font-semibold text-emerald-300">
                          {isBn ? "সক্রিয়" : "Active"}
                        </span>
                      ) : (
                        <Button
                          size="sm"
                          variant="secondary"
                          onClick={() => void switchBusiness(biz.id)}
                        >
                          {isBn ? "সুইচ" : "Switch"}
                        </Button>
                      )}
                    </div>
                  );
                })}
              </div>
            )}

            <form onSubmit={handleCreateBusiness} className="space-y-3 border-t border-slate-800/80 pt-4">
              <div className="text-xs font-semibold text-slate-200">
                {isBn ? "নতুন শাখা বা ব্যবসা যোগ করুন" : "Add Branch or Business Profile"}
              </div>
              <div className="space-y-2">
                <input
                  type="text"
                  required
                  minLength={2}
                  value={newBizName}
                  onChange={(e) => setNewBizName(e.target.value)}
                  placeholder="Branch / Shop Name"
                  className="w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-xs text-white placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
                />
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="text"
                    required
                    value={newBizIndustry}
                    onChange={(e) => setNewBizIndustry(e.target.value)}
                    placeholder="Industry"
                    className="w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-xs text-white focus:border-[#6366F1] focus:outline-none"
                  />
                  <input
                    type="text"
                    required
                    value={newBizCity}
                    onChange={(e) => setNewBizCity(e.target.value)}
                    placeholder="City"
                    className="w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-xs text-white focus:border-[#6366F1] focus:outline-none"
                  />
                </div>
              </div>
              <div className="flex justify-end">
                <Button type="submit" size="sm" variant="secondary" disabled={creatingBiz}>
                  <Plus className="h-3.5 w-3.5" aria-hidden="true" />
                  <span>{creatingBiz ? "Creating..." : "Create & Switch Workspace"}</span>
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>

      {/* Row 2: Clean Segmented Tabs for Plan, Integrations & Security Safeguards */}
      <Card className="min-w-0 overflow-hidden">
        <CardHeader className="flex-wrap">
          <div className="flex flex-wrap items-center gap-2">
            {[
              {
                id: "plan" as SettingsTab,
                icon: CreditCard,
                label: isBn ? "প্ল্যান ও কোটা" : "Plan & Quota",
              },
              {
                id: "integrations" as SettingsTab,
                icon: PlugZap,
                label: isBn ? "কানেক্টর ও ইন্টিগ্রেশন" : "Integrations",
              },
              {
                id: "safeguards" as SettingsTab,
                icon: ShieldCheck,
                label: t.settings.safeguardsCard,
              },
            ].map((tabItem) => {
              const TabIcon = tabItem.icon;
              const isCurrent = activeTab === tabItem.id;
              return (
                <button
                  key={tabItem.id}
                  type="button"
                  onClick={() => setActiveTab(tabItem.id)}
                  className={`inline-flex items-center gap-2 rounded-lg px-3.5 py-2 text-xs font-medium transition-colors ${
                    isCurrent
                      ? "bg-[#6366F1] text-white shadow-sm"
                      : "bg-[#0B1224] text-slate-300 hover:bg-slate-800 hover:text-white"
                  }`}
                >
                  <TabIcon className="h-3.5 w-3.5" aria-hidden="true" />
                  <span>{tabItem.label}</span>
                </button>
              );
            })}
          </div>
          {activeTab === "plan" && (
            <span className="font-mono text-xs text-cyan-300">
              {monthlyScansUsed}/{monthlyQuota} scans this month ({usagePercent}%)
            </span>
          )}
        </CardHeader>

        <CardContent>
          {activeTab === "plan" && (
            <div className="space-y-4">
              <div className="grid gap-3 md:grid-cols-3">
                {(plans.length > 0
                  ? plans
                  : [
                      {
                        key: "free",
                        name: "Free SME Starter",
                        monthly_scan_quota: 50,
                        max_workspaces: 2,
                        features: ["50 monthly scans", "Up to 2 workspaces"],
                      },
                      {
                        key: "pro_sme",
                        name: "Pro SME Shield",
                        monthly_scan_quota: 500,
                        max_workspaces: 10,
                        features: ["500 monthly scans", "Up to 10 branches"],
                      },
                      {
                        key: "enterprise_ready",
                        name: "Multi-Tenant Enterprise",
                        monthly_scan_quota: 5000,
                        max_workspaces: 50,
                        features: ["5,000 scans/mo", "SSO & OAuth readiness"],
                      },
                    ]
                ).map((p) => {
                  const planKey = p.key || p.tier || "free";
                  const selected = subscriptionTier === planKey;
                  const maxWs = p.max_workspaces ?? p.max_businesses ?? 2;
                  return (
                    <button
                      key={planKey}
                      type="button"
                      onClick={() => setSubscriptionTier(planKey)}
                      className={`rounded-xl border p-4 text-left transition-all ${
                        selected
                          ? "border-indigo-400 bg-indigo-500/15 ring-1 ring-indigo-400/40"
                          : "border-slate-800 bg-[#0B1224] hover:border-slate-700"
                      }`}
                    >
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-xs font-bold text-white">{p.name}</span>
                        {selected && (
                          <span className="rounded-full bg-indigo-500/25 px-2 py-0.5 text-[10px] font-semibold text-indigo-200">
                            Selected
                          </span>
                        )}
                      </div>
                      <div className="mt-2 font-mono text-sm font-semibold text-[#06B6D4]">
                        {p.monthly_scan_quota.toLocaleString()} scans/mo
                      </div>
                      <div className="mt-1 text-[11px] text-slate-400">
                        Up to {maxWs} workspace{maxWs === 1 ? "" : "s"}
                      </div>
                    </button>
                  );
                })}
              </div>

              <div className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-800/80 pt-4">
                <span className="text-xs text-slate-400">
                  {isBn
                    ? "পছন্দের প্ল্যান বেছে নিয়ে Apply Plan বাটনে ক্লিক করুন।"
                    : "Choose a tier above and click Apply Plan to update workspace quota."}
                </span>
                <Button
                  size="sm"
                  onClick={(e) => void handleSave(e as unknown as React.FormEvent)}
                  disabled={saving}
                >
                  {saving ? "..." : "Apply Plan"}
                </Button>
              </div>
            </div>
          )}

          {activeTab === "integrations" && (
            <div className="space-y-4">
              <div className="flex items-start gap-2 rounded-xl border border-cyan-500/25 bg-cyan-500/5 p-3 text-xs text-cyan-200">
                <Info className="mt-0.5 h-4 w-4 shrink-0 text-[#06B6D4]" aria-hidden="true" />
                <span>
                  {isBn
                    ? "এখানে বাইরের টুলের অ্যাকাউন্ট কনফিগার করা যায়; OAuth বা সার্ভার কী ছাড়া কোনো বাইরের ডেটা অটোমেটিক সিঙ্ক হয় না।"
                    : "Connectors save target accounts and readiness state cleanly without claiming live polling until external OAuth or API keys are provisioned."}
                </span>
              </div>

              {integrations.length === 0 ? (
                <div className="rounded-xl border border-dashed border-slate-800 p-6 text-center text-xs text-slate-400">
                  {isBn ? "কোনো ইন্টিগ্রেশন কনফিগার পাওয়া যায়নি।" : "No external connector schemas loaded."}
                </div>
              ) : (
                <div className="grid gap-3 md:grid-cols-2">
                  {integrations.map((item) => (
                    <div
                      key={item.provider_key}
                      className="min-w-0 space-y-2.5 rounded-xl border border-slate-800 bg-[#0B1224] p-4 text-xs"
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="min-w-0">
                          <div className="truncate font-semibold text-slate-100">{item.name}</div>
                          <div className="text-[10px] uppercase tracking-wider text-slate-400">
                            {item.category}
                          </div>
                        </div>
                        <span
                          className={`shrink-0 rounded-md border px-2 py-0.5 text-[10px] font-semibold ${
                            item.runtime_status === "active_server_env"
                              ? "border-emerald-500/40 bg-emerald-500/15 text-emerald-300"
                              : item.runtime_status === "configured_awaiting_oauth_gateway"
                              ? "border-amber-500/40 bg-amber-500/15 text-amber-200"
                              : "border-slate-700 bg-slate-800/80 text-slate-400"
                          }`}
                        >
                          {item.runtime_status === "active_server_env"
                            ? "Active (Server Env)"
                            : item.runtime_status === "configured_awaiting_oauth_gateway"
                            ? "Saved (Awaiting OAuth)"
                            : "Unconfigured"}
                        </span>
                      </div>
                      <p className="text-[11px] leading-relaxed text-slate-300">{item.description}</p>
                      <div className="flex flex-wrap items-center gap-2 pt-1">
                        <input
                          type="text"
                          value={item.endpoint_or_account || ""}
                          onChange={(e) => {
                            const v = e.target.value;
                            setIntegrations((prev) =>
                              prev.map((it) =>
                                it.provider_key === item.provider_key
                                  ? { ...it, endpoint_or_account: v }
                                  : it
                              )
                            );
                          }}
                          placeholder="Target domain, mailbox, or webhook URL..."
                          className="min-w-0 flex-1 rounded-lg border border-slate-700 bg-[#080D1B] px-2.5 py-1.5 text-[11px] text-white"
                        />
                        <Button
                          size="sm"
                          variant={item.enabled ? "secondary" : "primary"}
                          disabled={savingIntegrationKey === item.provider_key}
                          onClick={() => void handleSaveIntegration(item, !item.enabled)}
                        >
                          {savingIntegrationKey === item.provider_key
                            ? "Saving..."
                            : item.enabled
                            ? "Disable"
                            : "Save Config"}
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === "safeguards" && (
            <div className="grid gap-4 md:grid-cols-3 text-xs text-slate-300">
              <div className="rounded-xl border border-slate-800 bg-[#0B1224] p-4">
                <div className="font-semibold text-white">Password & Session Security</div>
                <p className="mt-1.5 leading-relaxed text-slate-400">
                  Argon2 password hashing with signed JWT session tokens and strict per-business data isolation.
                </p>
              </div>
              <div className="rounded-xl border border-slate-800 bg-[#0B1224] p-4">
                <div className="font-semibold text-white">SSRF-Safe URL Inspection</div>
                <p className="mt-1.5 leading-relaxed text-slate-400">
                  Blocks localhost, RFC1918 private IPs, link-local metadata endpoints, and non-HTTP schemes; never executes target content.
                </p>
              </div>
              <div className="rounded-xl border border-slate-800 bg-[#0B1224] p-4">
                <div className="font-semibold text-white">API Rate Limiting</div>
                <p className="mt-1.5 leading-relaxed text-slate-400">
                  Sliding-window per-IP rate limits protect authentication and analysis endpoints from abuse.
                </p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
