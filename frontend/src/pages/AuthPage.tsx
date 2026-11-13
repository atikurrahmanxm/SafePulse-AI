import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Shield } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { ApiError } from "../lib/api";
import { Logo } from "../components/layout/Logo";
import { Button, Card, CardContent, ErrorBanner } from "../components/ui/Primitives";

export function AuthPage({ mode }: { mode: "login" | "register" }) {
  const navigate = useNavigate();
  const { login, register, startDemoMode } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [businessName, setBusinessName] = useState("");
  const [industry, setIndustry] = useState("Retail & Local Shop");
  const [employeeCount, setEmployeeCount] = useState(8);
  const [city, setCity] = useState("Guwahati");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      if (mode === "login") {
        await login(email, password);
      } else {
        await register({
          email,
          password,
          full_name: fullName,
          business_name: businessName,
          industry,
          employee_count: Number(employeeCount) || 5,
          city,
        });
      }
      navigate("/app");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Authentication failed. Please check your inputs.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDemo = async () => {
    setError(null);
    setSubmitting(true);
    try {
      await startDemoMode();
      navigate("/app");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Unable to start demo session.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="relative flex min-h-[100dvh] flex-col items-center justify-center overflow-hidden bg-[#080D1B] px-4 py-10">
      <div
        className="pointer-events-none absolute inset-0 opacity-60"
        style={{
          background:
            "radial-gradient(circle at 25% 20%, rgba(99, 102, 241, 0.16), transparent 45%), radial-gradient(circle at 75% 80%, rgba(6, 182, 212, 0.14), transparent 42%)",
        }}
        aria-hidden="true"
      />
      <div className="relative mb-6">
        <Link to="/" aria-label="Back to SafePulse AI landing page">
          <Logo size="lg" />
        </Link>
      </div>

      <Card className="relative w-full max-w-md border-slate-700/70 shadow-2xl shadow-indigo-950/40">
        <CardContent className="p-6 sm:p-7">
          <h1 className="text-xl font-bold text-slate-50">
            {mode === "login" ? "Sign in to SafePulse AI" : "Create your Business Security Account"}
          </h1>
          <p className="mt-1 text-xs text-slate-400">
            {mode === "login"
              ? "Access your business threat scans, security score, and incident playbooks."
              : "Set up an isolated security workspace for your small business."}
          </p>

          {error && (
            <div className="mt-4">
              <ErrorBanner message={error} onDismiss={() => setError(null)} />
            </div>
          )}

          <form onSubmit={handleSubmit} className="mt-5 space-y-4">
            {mode === "register" && (
              <>
                <div>
                  <label htmlFor="full-name" className="block text-xs font-medium text-slate-300">
                    Your Full Name
                  </label>
                  <input
                    id="full-name"
                    type="text"
                    required
                    minLength={2}
                    autoComplete="name"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="e.g., Priya Das"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
                  />
                </div>
                <div>
                  <label htmlFor="biz-name" className="block text-xs font-medium text-slate-300">
                    Business Name
                  </label>
                  <input
                    id="biz-name"
                    type="text"
                    required
                    minLength={2}
                    autoComplete="organization"
                    value={businessName}
                    onChange={(e) => setBusinessName(e.target.value)}
                    placeholder="e.g., Guwahati Care Pharmacy"
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label htmlFor="industry" className="block text-xs font-medium text-slate-300">
                      Industry
                    </label>
                    <select
                      id="industry"
                      value={industry}
                      onChange={(e) => setIndustry(e.target.value)}
                      className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-2.5 py-2 text-sm text-white focus:border-[#6366F1] focus:outline-none"
                    >
                      <option>Retail & Local Shop</option>
                      <option>Pharmacy & Clinic</option>
                      <option>Startup / SaaS</option>
                      <option>Wholesale & Distribution</option>
                      <option>Professional Services</option>
                    </select>
                  </div>
                  <div>
                    <label htmlFor="city" className="block text-xs font-medium text-slate-300">
                      City
                    </label>
                    <input
                      id="city"
                      type="text"
                      required
                      value={city}
                      onChange={(e) => setCity(e.target.value)}
                      className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white focus:border-[#6366F1] focus:outline-none"
                    />
                  </div>
                </div>
                <div>
                  <label htmlFor="employees" className="block text-xs font-medium text-slate-300">
                    Team Size (Employees)
                  </label>
                  <input
                    id="employees"
                    type="number"
                    min={1}
                    max={5000}
                    required
                    value={employeeCount}
                    onChange={(e) => setEmployeeCount(Number(e.target.value))}
                    className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white focus:border-[#6366F1] focus:outline-none"
                  />
                </div>
              </>
            )}

            <div>
              <label htmlFor="auth-email" className="block text-xs font-medium text-slate-300">
                Email Address
              </label>
              <input
                id="auth-email"
                type="email"
                required
                autoComplete="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="owner@yourbusiness.in"
                className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:border-[#6366F1] focus:outline-none"
              />
            </div>

            <div>
              <label htmlFor="auth-password" className="block text-xs font-medium text-slate-300">
                Password
              </label>
              {mode === "register" && (
                <p id="pwd-hint" className="mt-0.5 text-[11px] text-slate-400">
                  Minimum 8 characters with at least one letter and one number.
                </p>
              )}
              <input
                id="auth-password"
                type="password"
                required
                minLength={mode === "register" ? 8 : 1}
                aria-describedby={mode === "register" ? "pwd-hint" : undefined}
                autoComplete={mode === "register" ? "new-password" : "current-password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1.5 w-full rounded-lg border border-slate-700 bg-[#080D1B] px-3 py-2 text-sm text-white focus:border-[#6366F1] focus:outline-none"
              />
            </div>

            <Button type="submit" className="w-full" size="lg" disabled={submitting}>
              {submitting
                ? "Please wait..."
                : mode === "login"
                ? "Sign In"
                : "Create Workspace"}
            </Button>
          </form>

          <div className="my-5 flex items-center gap-3 text-xs text-slate-500">
            <div className="h-px flex-1 bg-slate-800" />
            <span>OR EXPLORE IMMEDIATELY</span>
            <div className="h-px flex-1 bg-slate-800" />
          </div>

          <Button
            type="button"
            variant="secondary"
            className="w-full"
            size="lg"
            onClick={handleDemo}
            disabled={submitting}
          >
            <Shield className="h-4 w-4 text-[#06B6D4]" aria-hidden="true" />
            <span>Launch Hackathon Demo Mode</span>
          </Button>
          <p className="mt-2 text-center text-[11px] text-slate-400">
            Demo mode opens a pre-populated sample pharmacy workspace clearly labeled as demonstration data.
          </p>

          <div className="mt-5 text-center text-xs text-slate-400">
            {mode === "login" ? (
              <>
                New to SafePulse AI?{" "}
                <Link to="/register" className="font-semibold text-[#06B6D4] hover:underline">
                  Create an account
                </Link>
              </>
            ) : (
              <>
                Already have an account?{" "}
                <Link to="/login" className="font-semibold text-[#06B6D4] hover:underline">
                  Sign in
                </Link>
              </>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

