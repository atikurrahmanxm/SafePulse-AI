import React, { useEffect, useMemo, useRef, useState } from "react";
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import {
  Bell,
  BookOpen,
  Building2,
  ChevronLeft,
  ChevronRight,
  ClipboardCheck,
  FileBarChart2,
  FileWarning,
  Globe,
  GraduationCap,
  History,
  LayoutDashboard,
  Link2,
  LogOut,
  Menu,
  MessageSquareWarning,
  Search,
  Settings,
  ShieldCheck,
  User,
  X,
} from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import { useLanguage } from "../../i18n/LanguageContext";
import { apiRequest } from "../../lib/api";
import { cn } from "../../lib/utils";
import { Logo } from "./Logo";

interface AlertSummary {
  highRiskCount: number;
  activeIncidents: number;
}

export function AppShell() {
  const { user, logout, switchBusiness } = useAuth();
  const { language, setLanguage, t } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();

  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [notifOpen, setNotifOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const searchInputRef = useRef<HTMLInputElement>(null);
  const searchBoxRef = useRef<HTMLDivElement>(null);
  const notifRef = useRef<HTMLDivElement>(null);
  const profileRef = useRef<HTMLDivElement>(null);
  const [alertSummary, setAlertSummary] = useState<AlertSummary>({
    highRiskCount: 0,
    activeIncidents: 0,
  });

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setNotifOpen(false);
        setProfileOpen(false);
        setSearchQuery("");
        setMobileOpen(false);
      } else if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        searchInputRef.current?.focus();
      }
    };
    const handlePointerDown = (e: MouseEvent) => {
      const target = e.target as Node;
      if (notifRef.current && !notifRef.current.contains(target)) {
        setNotifOpen(false);
      }
      if (profileRef.current && !profileRef.current.contains(target)) {
        setProfileOpen(false);
      }
      if (searchBoxRef.current && !searchBoxRef.current.contains(target)) {
        setSearchQuery("");
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    document.addEventListener("mousedown", handlePointerDown);
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("mousedown", handlePointerDown);
    };
  }, []);

  const navItems = useMemo(
    () => [
      {
        to: "/app",
        label: t.nav.overview,
        icon: LayoutDashboard,
        end: true,
        group: language === "bn" ? "সুরক্ষা ও স্ক্যান" : "Protect & Scan",
      },
      {
        to: "/app/phishing",
        label: t.nav.phishing,
        icon: MessageSquareWarning,
        group: language === "bn" ? "সুরক্ষা ও স্ক্যান" : "Protect & Scan",
      },
      {
        to: "/app/url-scanner",
        label: t.nav.urlScanner,
        icon: Link2,
        group: language === "bn" ? "সুরক্ষা ও স্ক্যান" : "Protect & Scan",
      },
      {
        to: "/app/assessment",
        label: t.nav.assessment,
        icon: ClipboardCheck,
        group: language === "bn" ? "টিম ও রেসপন্স" : "Team & Response",
      },
      {
        to: "/app/governance",
        label: t.nav.governance,
        icon: ShieldCheck,
        group: language === "bn" ? "টিম ও রেসপন্স" : "Team & Response",
      },
      {
        to: "/app/incidents",
        label: t.nav.incidents,
        icon: FileWarning,
        group: language === "bn" ? "টিম ও রেসপন্স" : "Team & Response",
      },
      {
        to: "/app/awareness",
        label: t.nav.awareness,
        icon: GraduationCap,
        group: language === "bn" ? "টিম ও রেসপন্স" : "Team & Response",
      },
      {
        to: "/app/reports",
        label: t.nav.reports,
        icon: FileBarChart2,
        group: language === "bn" ? "রিপোর্ট ও সেটিংস" : "Reports & Settings",
      },
      {
        to: "/app/history",
        label: t.nav.history,
        icon: History,
        group: language === "bn" ? "রিপোর্ট ও সেটিংস" : "Reports & Settings",
      },
      {
        to: "/app/settings",
        label: t.nav.settings,
        icon: Settings,
        group: language === "bn" ? "রিপোর্ট ও সেটিংস" : "Reports & Settings",
      },
      {
        to: "/app/docs",
        label: t.nav.docs,
        icon: BookOpen,
        group: language === "bn" ? "রিপোর্ট ও সেটিংস" : "Reports & Settings",
      },
    ],
    [t, language]
  );

  const currentNav =
    navItems.find((item) =>
      item.end ? location.pathname === item.to : location.pathname.startsWith(item.to)
    ) || navItems[0];

  useEffect(() => {
    document.title = `${currentNav.label} | CyberShield AI`;
    setMobileOpen(false);
  }, [location.pathname, currentNav.label]);

  useEffect(() => {
    let active = true;
    apiRequest<{ summary: { high_risk_findings: number; active_incidents: number } }>(
      `/api/dashboard/overview?language=${language}`
    )
      .then((res) => {
        if (active) {
          setAlertSummary({
            highRiskCount: res.summary.high_risk_findings,
            activeIncidents: res.summary.active_incidents,
          });
        }
      })
      .catch(() => {});
    return () => {
      active = false;
    };
  }, [location.pathname, language, user?.business?.id]);

  const searchMatches = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    if (!q) return [];
    return navItems.filter((item) => item.label.toLowerCase().includes(q));
  }, [searchQuery, navItems]);

  const totalNotifications = alertSummary.highRiskCount + alertSummary.activeIncidents;

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  const renderSidebarLinks = (isMobile = false) => (
    <nav aria-label="Primary" className="flex-1 space-y-1 px-2.5 py-3 overflow-y-auto">
      {navItems.map((item, idx) => {
        const Icon = item.icon;
        const showGroupHeader =
          (!collapsed || isMobile) &&
          (idx === 0 || navItems[idx - 1].group !== item.group);
        return (
          <React.Fragment key={item.to}>
            {showGroupHeader && (
              <div
                className={cn(
                  "px-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500",
                  idx === 0 ? "pb-1 pt-0.5" : "pb-1 pt-3"
                )}
              >
                {item.group}
              </div>
            )}
            <NavLink
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                cn(
                  "group flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium transition-all",
                  isActive
                    ? "bg-gradient-to-r from-[#6366F1]/25 to-[#06B6D4]/12 text-white border border-indigo-400/35 shadow-[0_6px_18px_-10px_rgba(99,102,241,0.75)]"
                    : "text-slate-400 hover:bg-[#1B2942]/75 hover:text-slate-100 border border-transparent"
                )
              }
            >
              <Icon className="h-4 w-4 shrink-0 text-[#06B6D4]" aria-hidden="true" />
              {(!collapsed || isMobile) && <span className="truncate">{item.label}</span>}
            </NavLink>
          </React.Fragment>
        );
      })}
    </nav>
  );

  return (
    <div className="flex min-h-[100dvh] bg-[#080D1B] text-[#F8FAFC]">
      <a
        href="#main-content"
        className="visually-hidden fixed left-4 top-4 z-50 rounded-lg bg-[#6366F1] px-4 py-2 text-sm font-semibold text-white"
      >
        Skip to main content
      </a>

      {/* Desktop Sidebar */}
      <aside
        className={cn(
          "hidden lg:flex lg:flex-col lg:shrink-0 border-r border-slate-800/80 bg-[#10182B] transition-[width] duration-200",
          collapsed ? "lg:w-[72px]" : "lg:w-64"
        )}
      >
        <div className="flex h-16 items-center justify-between border-b border-slate-800/80 px-4">
          <button
            type="button"
            onClick={() => navigate("/app")}
            className="text-left focus-visible:rounded-lg"
            aria-label="CyberShield AI Home"
          >
            <Logo compact={collapsed} />
          </button>
          <button
            type="button"
            onClick={() => setCollapsed((c) => !c)}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-[#1B2942] hover:text-white"
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
          </button>
        </div>

        {renderSidebarLinks(false)}

        <div className="border-t border-slate-800/80 p-3">
          {!collapsed && user && (
            <div className="mb-2.5 rounded-lg border border-slate-800 bg-[#141F35] px-3 py-2 space-y-1.5">
              <div className="flex items-center justify-between gap-2">
                <div className="truncate text-xs font-semibold text-slate-100">{user.full_name}</div>
                <span className="shrink-0 rounded bg-indigo-500/15 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-indigo-300 border border-indigo-500/25">
                  {user.business.subscription_tier === "pro_sme"
                    ? "Pro SME"
                    : user.business.subscription_tier === "enterprise_ready"
                    ? "Multi-Site"
                    : "Free"}
                </span>
              </div>
              {Array.isArray(user.businesses) && user.businesses.length > 1 ? (
                <div className="flex items-center gap-1.5 pt-0.5">
                  <Building2 className="h-3.5 w-3.5 shrink-0 text-[#06B6D4]" aria-hidden="true" />
                  <select
                    aria-label="Switch business workspace"
                    value={user.business.id}
                    onChange={(e) => {
                      const id = Number(e.target.value);
                      if (id && id !== user.business.id) {
                        void switchBusiness(id);
                      }
                    }}
                    className="w-full truncate rounded border border-slate-700 bg-[#080D1B] px-1.5 py-1 text-[11px] font-medium text-slate-200"
                  >
                    {user.businesses.map((b) => (
                      <option key={b.id} value={b.id}>
                        {b.name} ({b.city})
                      </option>
                    ))}
                  </select>
                </div>
              ) : (
                <div className="truncate text-[11px] text-slate-400">{user.business.name}</div>
              )}
            </div>
          )}
          <button
            type="button"
            onClick={handleLogout}
            className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-slate-300 hover:bg-red-500/10 hover:text-red-300 transition-colors"
          >
            <LogOut className="h-4 w-4 shrink-0" aria-hidden="true" />
            {!collapsed && <span>{t.nav.logout}</span>}
          </button>
        </div>
      </aside>

      {/* Mobile Drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 flex lg:hidden">
          <div
            className="fixed inset-0 bg-black/70 backdrop-blur-sm"
            onClick={() => setMobileOpen(false)}
            aria-hidden="true"
          />
          <aside className="relative z-10 flex w-72 max-w-[85vw] flex-col border-r border-slate-800 bg-[#10182B]">
            <div className="flex h-16 items-center justify-between border-b border-slate-800 px-4">
              <Logo />
              <button
                type="button"
                onClick={() => setMobileOpen(false)}
                className="rounded-lg p-1.5 text-slate-300 hover:bg-[#1B2942]"
                aria-label="Close navigation menu"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            {renderSidebarLinks(true)}
            <div className="border-t border-slate-800 p-3">
              <button
                type="button"
                onClick={handleLogout}
                className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-red-300 hover:bg-red-500/10"
              >
                <LogOut className="h-4 w-4" aria-hidden="true" />
                <span>{t.nav.logout}</span>
              </button>
            </div>
          </aside>
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between gap-3 border-b border-slate-800/80 bg-[#080D1B]/90 px-4 backdrop-blur-md sm:px-6">
          <div className="flex min-w-0 items-center gap-3">
            <button
              type="button"
              onClick={() => setMobileOpen(true)}
              className="rounded-lg p-2 text-slate-300 hover:bg-[#1B2942] lg:hidden"
              aria-label="Open navigation menu"
            >
              <Menu className="h-5 w-5" />
            </button>
            <div className="min-w-0">
              <h1 className="truncate text-base font-semibold text-slate-50 sm:text-lg">
                {currentNav.label}
              </h1>
            </div>
            {user?.is_demo && (
              <span className="hidden sm:inline-flex items-center rounded-full border border-cyan-500/40 bg-cyan-500/10 px-2.5 py-0.5 text-[11px] font-medium text-cyan-300">
                {t.topbar.demoBadge}
              </span>
            )}
          </div>

          <div className="flex items-center gap-2 sm:gap-3">
            {/* Quick Search / Command Jump */}
            <div ref={searchBoxRef} className="relative hidden md:block w-60">
              <Search
                className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
                aria-hidden="true"
              />
              <input
                ref={searchInputRef}
                type="search"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={t.topbar.searchPlaceholder}
                aria-label={t.topbar.searchPlaceholder}
                className="w-full rounded-lg border border-slate-800 bg-[#10182B] py-1.5 pl-9 pr-3 text-xs text-slate-100 placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
              />
              {searchMatches.length > 0 && (
                <div className="absolute left-0 right-0 top-10 z-40 rounded-lg border border-slate-700 bg-[#141F35] p-1 shadow-xl">
                  {searchMatches.map((m) => (
                    <button
                      key={m.to}
                      type="button"
                      onClick={() => {
                        navigate(m.to);
                        setSearchQuery("");
                      }}
                      className="flex w-full items-center gap-2 rounded-md px-2.5 py-1.5 text-left text-xs text-slate-200 hover:bg-[#1B2942]"
                    >
                      <m.icon className="h-3.5 w-3.5 text-[#06B6D4]" aria-hidden="true" />
                      <span>{m.label}</span>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Quick Easy Reports Hub Shortcut */}
            <button
              type="button"
              onClick={() => navigate("/app/reports")}
              className="hidden sm:inline-flex h-9 items-center gap-1.5 rounded-lg border border-cyan-500/35 bg-cyan-500/10 px-3 text-xs font-medium text-cyan-200 transition-colors hover:bg-cyan-500/20"
            >
              <FileBarChart2 className="h-3.5 w-3.5 text-cyan-300" aria-hidden="true" />
              <span>{language === "bn" ? "রিপোর্ট (PDF)" : "Reports"}</span>
            </button>

            {/* Bilingual EN/BN Toggle */}
            <button
              type="button"
              onClick={() => setLanguage(language === "en" ? "bn" : "en")}
              className="inline-flex h-9 items-center gap-1.5 rounded-lg border border-slate-700/80 bg-[#141F35] px-3 text-xs font-medium text-slate-200 transition-colors hover:bg-[#1B2942]"
              aria-label="Toggle language between English and Bengali"
            >
              <Globe className="h-3.5 w-3.5 text-[#06B6D4]" aria-hidden="true" />
              <span>{language === "en" ? "EN / বাংলা" : "বাংলা / EN"}</span>
            </button>

            {/* Notifications Indicator */}
            <div ref={notifRef} className="relative">
              <button
                type="button"
                onClick={() => {
                  setNotifOpen((v) => !v);
                  setProfileOpen(false);
                }}
                className="relative inline-flex h-9 w-9 items-center justify-center rounded-lg border border-slate-800 bg-[#141F35] text-slate-300 transition-colors hover:bg-[#1B2942] hover:text-white"
                aria-label={t.topbar.notifications}
                aria-expanded={notifOpen}
              >
                <Bell className="h-4 w-4" aria-hidden="true" />
                {totalNotifications > 0 && (
                  <span className="absolute -right-1 -top-1 flex h-4 min-w-[16px] items-center justify-center rounded-full bg-[#EF4444] px-1 text-[10px] font-bold text-white">
                    {totalNotifications}
                  </span>
                )}
              </button>
              {notifOpen && (
                <div className="absolute right-0 top-11 z-40 w-72 rounded-xl border border-slate-700 bg-[#141F35] p-3.5 shadow-xl">
                  <div className="mb-2 text-xs font-semibold text-slate-200">{t.topbar.notifications}</div>
                  {totalNotifications === 0 ? (
                    <p className="text-xs text-slate-400">{t.topbar.noAlerts}</p>
                  ) : (
                    <div className="space-y-2 text-xs">
                      {alertSummary.highRiskCount > 0 && (
                        <button
                          type="button"
                          onClick={() => {
                            setNotifOpen(false);
                            navigate("/app/history");
                          }}
                          className="w-full rounded-lg border border-red-500/30 bg-red-500/10 p-2.5 text-left text-red-200 hover:bg-red-500/20"
                        >
                          {language === "bn"
                            ? `${alertSummary.highRiskCount}টি উচ্চ/মারাত্মক ঝুঁকির তথ্য রেকর্ড করা হয়েছে।`
                            : `${alertSummary.highRiskCount} high/critical threat finding(s) recorded.`}
                        </button>
                      )}
                      {alertSummary.activeIncidents > 0 && (
                        <button
                          type="button"
                          onClick={() => {
                            setNotifOpen(false);
                            navigate("/app/incidents");
                          }}
                          className="w-full rounded-lg border border-amber-500/30 bg-amber-500/10 p-2.5 text-left text-amber-200 hover:bg-amber-500/20"
                        >
                          {language === "bn"
                            ? `${alertSummary.activeIncidents}টি চলমান ইনসিডেন্ট চেকলিস্ট বাকি আছে।`
                            : `${alertSummary.activeIncidents} active incident checklist(s) in progress.`}
                        </button>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Profile Menu */}
            <div ref={profileRef} className="relative">
              <button
                type="button"
                onClick={() => {
                  setProfileOpen((v) => !v);
                  setNotifOpen(false);
                }}
                className="inline-flex h-9 items-center gap-2 rounded-lg border border-slate-800 bg-[#141F35] px-2.5 text-xs font-medium text-slate-200 transition-colors hover:bg-[#1B2942]"
                aria-expanded={profileOpen}
              >
                <User className="h-3.5 w-3.5 text-[#6366F1]" aria-hidden="true" />
                <span className="hidden sm:inline max-w-[120px] truncate">{user?.full_name}</span>
              </button>
              {profileOpen && (
                <div className="absolute right-0 top-11 z-40 w-56 rounded-xl border border-slate-700 bg-[#141F35] p-2 shadow-xl">
                  <div className="border-b border-slate-800 px-2.5 py-2">
                    <div className="truncate text-xs font-semibold text-white">{user?.full_name}</div>
                    <div className="truncate text-[11px] text-slate-400">{user?.email}</div>
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      setProfileOpen(false);
                      navigate("/app/settings");
                    }}
                    className="mt-1 flex w-full items-center gap-2 rounded-lg px-2.5 py-2 text-left text-xs text-slate-200 hover:bg-[#1B2942]"
                  >
                    <Settings className="h-3.5 w-3.5" aria-hidden="true" />
                    <span>{t.nav.settings}</span>
                  </button>
                  <button
                    type="button"
                    onClick={handleLogout}
                    className="flex w-full items-center gap-2 rounded-lg px-2.5 py-2 text-left text-xs text-red-300 hover:bg-red-500/10"
                  >
                    <LogOut className="h-3.5 w-3.5" aria-hidden="true" />
                    <span>{t.nav.logout}</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        </header>

        {user?.is_demo && (
          <div className="border-b border-cyan-500/20 bg-cyan-500/5 px-4 py-1.5 text-xs text-cyan-200 sm:px-6">
            <span className="font-semibold">
              {language === "bn"
                ? `ডেমো ওয়ার্কস্পেস চালু আছে (${user.business.name}):`
                : `Demo Workspace Active (${user.business.name}):`}
            </span>{" "}
            {language === "bn"
              ? "এখানে দেখানো নমুনা ডেটা শুধু প্রদর্শনের জন্য — আসল ব্যবসার জন্য নিজস্ব অ্যাকাউন্ট তৈরি করতে পারেন।"
              : "Sample records are clearly tagged as demonstrations for AdtU Innovation Mela 2026 evaluation."}
          </div>
        )}

        <main id="main-content" tabIndex={-1} className="flex-1 p-4 sm:p-6 focus:outline-none">
          <div className="mx-auto max-w-7xl">
            <Outlet key={user?.business?.id ?? 0} />
          </div>
        </main>
      </div>
    </div>
  );
}

