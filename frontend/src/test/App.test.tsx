import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";

function renderApp(initialRoute = "/") {
  return render(
    <MemoryRouter
      initialEntries={[initialRoute]}
      future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
    >
      <App />
    </MemoryRouter>
  );
}

describe("CyberShield AI Frontend", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  it("renders landing page and toggles bilingual English / Bengali", async () => {
    const user = userEvent.setup();
    renderApp("/");

    expect(
      screen.getByText("Your Business Deserves Better Cyber Protection.")
    ).toBeInTheDocument();

    const langBtn = screen.getByRole("button", { name: /বাংলা/i });
    await user.click(langBtn);

    expect(
      screen.getByText("আপনার ব্যবসার জন্য আরও শক্তিশালী সাইবার সুরক্ষা।")
    ).toBeInTheDocument();
  });

  it("navigates to login and displays API error state on invalid credentials", async () => {
    const user = userEvent.setup();
    vi.spyOn(globalThis, "fetch").mockResolvedValueOnce(
      new Response(JSON.stringify({ detail: "Invalid email or password." }), {
        status: 401,
        headers: { "Content-Type": "application/json" },
      })
    );

    renderApp("/login");
    await user.type(screen.getByLabelText("Email Address"), "owner@shop.in");
    await user.type(screen.getByLabelText("Password"), "wrongpass");
    await user.click(screen.getByRole("button", { name: "Sign In" }));

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("Invalid email or password.");
    });
  });

  it("loads authenticated phishing detector, submits message, and renders risk score + highlights", async () => {
    const user = userEvent.setup();
    localStorage.setItem("cybershield_token", "test-jwt");

    vi.spyOn(globalThis, "fetch").mockImplementation(async (input) => {
      const url = typeof input === "string" ? input : input instanceof URL ? input.toString() : input.url;
      if (url.includes("/api/auth/me")) {
        return new Response(
          JSON.stringify({
            id: 1,
            email: "priya@shop.in",
            full_name: "Priya Das",
            role: "owner",
            preferred_language: "en",
            is_demo: false,
            business: {
              id: 1,
              name: "Guwahati Care Pharmacy",
              industry: "Pharmacy",
              employee_count: 8,
              city: "Guwahati",
              is_demo_workspace: false,
            },
          }),
          { status: 200 }
        );
      }
      if (url.includes("/api/dashboard/overview")) {
        return new Response(
          JSON.stringify({ summary: { high_risk_findings: 0, active_incidents: 0 } }),
          { status: 200 }
        );
      }
      if (url.includes("/api/phishing/samples")) {
        return new Response(JSON.stringify({ samples: [] }), { status: 200 });
      }
      if (url.includes("/api/phishing/model-evaluation")) {
        return new Response(JSON.stringify(null), { status: 404 });
      }
      if (url.includes("/api/phishing/analyze")) {
        return new Response(
          JSON.stringify({
            id: 42,
            channel: "sms",
            sender_hint: null,
            raw_message: "URGENT: Verify your OTP now at http://sbi-kyc.xyz/login",
            risk_score: 88,
            risk_category: "Critical Risk",
            ml_probability: 0.91,
            model_confidence: 0.9,
            highlighted_phrases: [
              { phrase: "URGENT", category: "urgency_pressure", weight: 16, start: 0, end: 6 },
            ],
            reasons: ["Requests sensitive credentials or OTP."],
            recommendations: ["Do not click any links."],
            created_at: "2026-11-12T10:00:00Z",
          }),
          { status: 201 }
        );
      }
      return new Response("{}", { status: 200 });
    });

    renderApp("/app/phishing");

    await waitFor(() => {
      expect(screen.getByText("AI Phishing & Scam Detector")).toBeInTheDocument();
    });

    await user.type(
      screen.getByLabelText("Paste Suspicious Message"),
      "URGENT: Verify your OTP now at http://sbi-kyc.xyz/login"
    );
    await user.click(screen.getByRole("button", { name: "Analyze Message" }));

    await waitFor(() => {
      expect(screen.getByText("88")).toBeInTheDocument();
      expect(screen.getByText("Critical Risk")).toBeInTheDocument();
      expect(screen.getByText("Requests sensitive credentials or OTP.")).toBeInTheDocument();
    });
  });

  it("displays SSRF error banner when URL scanner rejects localhost", async () => {
    const user = userEvent.setup();
    localStorage.setItem("cybershield_token", "test-jwt");

    vi.spyOn(globalThis, "fetch").mockImplementation(async (input) => {
      const url = typeof input === "string" ? input : input instanceof URL ? input.toString() : input.url;
      if (url.includes("/api/auth/me")) {
        return new Response(
          JSON.stringify({
            id: 1,
            email: "priya@shop.in",
            full_name: "Priya Das",
            role: "owner",
            preferred_language: "en",
            is_demo: false,
            business: {
              id: 1,
              name: "Guwahati Care Pharmacy",
              industry: "Pharmacy",
              employee_count: 8,
              city: "Guwahati",
              is_demo_workspace: false,
            },
          }),
          { status: 200 }
        );
      }
      if (url.includes("/api/dashboard/overview")) {
        return new Response(
          JSON.stringify({ summary: { high_risk_findings: 0, active_incidents: 0 } }),
          { status: 200 }
        );
      }
      if (url.includes("/api/urls/samples")) {
        return new Response(JSON.stringify({ samples: [] }), { status: 200 });
      }
      if (url.includes("/api/urls/scan")) {
        return new Response(
          JSON.stringify({
            detail: "SSRF protection blocked internal/localhost hostname 'localhost'.",
          }),
          { status: 400 }
        );
      }
      return new Response("{}", { status: 200 });
    });

    renderApp("/app/url-scanner");

    await waitFor(() => {
      expect(screen.getByText("Smart URL Security Analyzer")).toBeInTheDocument();
    });

    await user.type(screen.getByLabelText("Website or Link URL"), "http://localhost:8000/admin");
    await user.click(screen.getByRole("button", { name: "Scan URL Safely" }));

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent("SSRF protection blocked");
    });
  });

  it("opens an incident playbook, shows India 1930 escalation, and toggles checklist progress", async () => {
    const user = userEvent.setup();
    localStorage.setItem("cybershield_token", "test-jwt");

    const baseIncident = {
      id: 7,
      scenario_key: "phishing_link_clicked",
      title: "Phishing Link Clicked / Credentials Entered",
      severity: "High",
      status: "in_progress",
      notes: null,
      progress_percent: 0,
      completed_count: 0,
      total_count: 2,
      is_demo_sample: false,
      created_at: "2026-11-12T10:00:00Z",
      updated_at: "2026-11-12T10:00:00Z",
      checklist_items: [
        {
          id: 701,
          phase: "Immediate Actions",
          title: "Reset affected passwords immediately",
          guidance: "Change account password from a clean device.",
          is_completed: false,
          sort_order: 1,
        },
        {
          id: 702,
          phase: "Evidence Preservation",
          title: "Capture screenshot and headers",
          guidance: "Save SMS/email evidence before deleting.",
          is_completed: false,
          sort_order: 2,
        },
      ],
    };

    vi.spyOn(globalThis, "fetch").mockImplementation(async (input, init) => {
      const url = typeof input === "string" ? input : input instanceof URL ? input.toString() : input.url;
      if (url.includes("/api/auth/me")) {
        return new Response(
          JSON.stringify({
            id: 1,
            email: "priya@shop.in",
            full_name: "Priya Das",
            role: "owner",
            preferred_language: "en",
            is_demo: false,
            business: {
              id: 1,
              name: "Guwahati Care Pharmacy",
              industry: "Pharmacy",
              employee_count: 8,
              city: "Guwahati",
              is_demo_workspace: false,
            },
          }),
          { status: 200 }
        );
      }
      if (url.includes("/api/dashboard/overview")) {
        return new Response(
          JSON.stringify({ summary: { high_risk_findings: 0, active_incidents: 0 } }),
          { status: 200 }
        );
      }
      if (url.includes("/api/incidents/scenarios")) {
        return new Response(
          JSON.stringify({
            scenarios: [
              {
                key: "phishing_link_clicked",
                title: "Phishing Link Clicked / Credentials Entered",
                severity: "High",
                summary: "Staff clicked a spoofed login link.",
                steps_count: 2,
              },
            ],
          }),
          { status: 200 }
        );
      }
      if (url.endsWith("/api/incidents") && (!init || !init.method || init.method === "GET")) {
        return new Response(JSON.stringify([baseIncident]), { status: 200 });
      }
      if (url.includes("/api/incidents/7/items/701")) {
        return new Response(
          JSON.stringify({
            ...baseIncident,
            completed_count: 1,
            progress_percent: 50,
            checklist_items: [
              { ...baseIncident.checklist_items[0], is_completed: true },
              baseIncident.checklist_items[1],
            ],
          }),
          { status: 200 }
        );
      }
      return new Response("{}", { status: 200 });
    });

    renderApp("/app/incidents");

    await waitFor(() => {
      expect(screen.getByText(/Urgent India Financial\/Cyber Escalation/i)).toBeInTheDocument();
    });

    await user.click(screen.getByRole("button", { name: /Reset affected passwords immediately/i }));

    await waitFor(() => {
      expect(screen.getByText(/1\/2 steps \(50%\)/i)).toBeInTheDocument();
    });
  });

  it("renders governance team MFA directory and toggles control checklists", async () => {
    const user = userEvent.setup();
    localStorage.setItem("cybershield_token", "test-jwt");

    let memberMfa = false;
    vi.spyOn(globalThis, "fetch").mockImplementation(async (input, init) => {
      const url = typeof input === "string" ? input : input instanceof URL ? input.toString() : input.url;
      if (url.includes("/api/auth/me")) {
        return new Response(
          JSON.stringify({
            id: 1,
            email: "priya@shop.in",
            full_name: "Priya Das",
            role: "owner",
            preferred_language: "en",
            is_demo: false,
            business: {
              id: 1,
              name: "Guwahati Care Pharmacy",
              industry: "Pharmacy",
              employee_count: 8,
              city: "Guwahati",
              subscription_tier: "free",
              monthly_scan_quota: 100,
              is_demo_workspace: false,
            },
          }),
          { status: 200 }
        );
      }
      if (url.includes("/api/dashboard/overview")) {
        return new Response(
          JSON.stringify({ summary: { high_risk_findings: 0, active_incidents: 0 } }),
          { status: 200 }
        );
      }
      if (url.includes("/api/governance/members/11") && init?.method === "PATCH") {
        memberMfa = true;
        return new Response(
          JSON.stringify({
            id: 11,
            full_name: "Ankit Baruah",
            email: "ankit@shop.in",
            role: "Staff",
            department: "Billing",
            mfa_enabled: true,
            awareness_trained: true,
            created_at: new Date().toISOString(),
          }),
          { status: 200 }
        );
      }
      if (url.includes("/api/governance/overview")) {
        return new Response(
          JSON.stringify({
            mfa_stats: {
              total_members: 1,
              mfa_enabled_count: memberMfa ? 1 : 0,
              mfa_adoption_percent: memberMfa ? 100 : 0,
              awareness_trained_count: 1,
            },
            controls_stats: {
              completed_count: 0,
              total_count: 1,
              completion_percent: 0,
            },
            members: [
              {
                id: 11,
                full_name: "Ankit Baruah",
                email: "ankit@shop.in",
                role: "Staff",
                department: "Billing",
                mfa_enabled: memberMfa,
                awareness_trained: true,
                created_at: new Date().toISOString(),
              },
            ],
            controls: [
              {
                id: 501,
                category: "backup",
                control_key: "offline_backup_weekly",
                title: "Maintain offline encrypted billing backup",
                guidance: "Store weekly snapshots offline.",
                priority: "High",
                is_completed: false,
              },
            ],
          }),
          { status: 200 }
        );
      }
      return new Response("{}", { status: 200 });
    });

    renderApp("/app/governance");

    await waitFor(() => {
      expect(screen.getByText(/Ankit Baruah/i)).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "MFA: OFF" })).toBeInTheDocument();
    });

    await user.click(screen.getByRole("button", { name: "MFA: OFF" }));

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "MFA: ON" })).toBeInTheDocument();
    });
  });

  it("renders Easy Security Reports Center with 5 report cards and triggers 1-click monthly PDF download", async () => {
    const user = userEvent.setup();
    localStorage.setItem("cybershield_token", "test-jwt");

    const createObjectUrlSpy = vi.fn().mockReturnValue("blob:monthly");
    const revokeObjectUrlSpy = vi.fn();
    Object.defineProperty(URL, "createObjectURL", {
      configurable: true,
      writable: true,
      value: createObjectUrlSpy,
    });
    Object.defineProperty(URL, "revokeObjectURL", {
      configurable: true,
      writable: true,
      value: revokeObjectUrlSpy,
    });
    const fetchCalls: string[] = [];

    vi.spyOn(globalThis, "fetch").mockImplementation(async (input) => {
      const url = typeof input === "string" ? input : input instanceof URL ? input.toString() : input.url;
      fetchCalls.push(url);
      if (url.includes("/api/auth/me")) {
        return new Response(
          JSON.stringify({
            id: 1,
            email: "priya@shop.in",
            full_name: "Priya Das",
            role: "owner",
            preferred_language: "en",
            is_demo: false,
            business: {
              id: 1,
              name: "Guwahati Care Pharmacy",
              industry: "Pharmacy",
              employee_count: 8,
              city: "Guwahati",
              is_demo_workspace: false,
              subscription_tier: "free",
              monthly_scan_quota: 50,
            },
          }),
          { status: 200 }
        );
      }
      if (url.includes("/api/dashboard/overview")) {
        return new Response(
          JSON.stringify({
            summary: {
              business_security_score: 76,
              security_category: "Good Security Posture",
              total_threat_analyses: 4,
              high_risk_findings: 1,
              completed_assessments: 1,
              active_incidents: 0,
            },
            improvement_progress: { mfa_adoption_percent: 80 },
            business: { name: "Guwahati Care Pharmacy", industry: "Pharmacy", city: "Guwahati" },
          }),
          { status: 200 }
        );
      }
      if (url.includes("/api/history/unified")) {
        return new Response(
          JSON.stringify({
            items: [
              {
                uid: "phishing-1",
                record_id: 1,
                type: "phishing",
                title: "SMS Phishing Scan",
                target: "URGENT KYC OTP",
                score: 88,
                status_label: "Critical Risk",
                is_demo_sample: false,
                created_at: "2026-11-12T10:00:00Z",
                pdf_url: "/api/phishing/1/report.pdf",
              },
            ],
          }),
          { status: 200 }
        );
      }
      if (url.includes("/api/reports/monthly.pdf")) {
        return new Response(new Blob(["%PDF-1.4 fake"], { type: "application/pdf" }), { status: 200 });
      }
      return new Response("{}", { status: 200 });
    });

    renderApp("/app/reports");

    await waitFor(() => {
      expect(screen.getByText("Easy Security Reports Center")).toBeInTheDocument();
      expect(screen.getByText("Monthly Executive Business Security Report")).toBeInTheDocument();
      expect(screen.getByText("Phishing & Scam Analysis Report")).toBeInTheDocument();
      expect(screen.getByText("Website & Link Safety Report")).toBeInTheDocument();
      expect(screen.getByText("Business Security Assessment Report")).toBeInTheDocument();
      expect(screen.getByText("Incident & 1930 Escalation Report")).toBeInTheDocument();
    });

    await user.click(screen.getByRole("button", { name: "Download Monthly Report (PDF)" }));

    await waitFor(() => {
      expect(fetchCalls.some((u) => u.includes("/api/reports/monthly.pdf"))).toBe(true);
      expect(createObjectUrlSpy).toHaveBeenCalled();
      expect(revokeObjectUrlSpy).toHaveBeenCalled();
    });
  });
});
