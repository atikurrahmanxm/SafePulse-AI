import React, { Suspense, lazy } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { LanguageProvider } from "./i18n/LanguageContext";
import { AppShell } from "./components/layout/AppShell";
import { Skeleton } from "./components/ui/Primitives";
import { LandingPage } from "./pages/LandingPage";
import { AuthPage } from "./pages/AuthPage";

const OverviewPage = lazy(() =>
  import("./pages/OverviewPage").then((m) => ({ default: m.OverviewPage }))
);
const PhishingDetectorPage = lazy(() =>
  import("./pages/PhishingDetectorPage").then((m) => ({ default: m.PhishingDetectorPage }))
);
const UrlScannerPage = lazy(() =>
  import("./pages/UrlScannerPage").then((m) => ({ default: m.UrlScannerPage }))
);
const AssessmentPage = lazy(() =>
  import("./pages/AssessmentPage").then((m) => ({ default: m.AssessmentPage }))
);
const GovernancePage = lazy(() =>
  import("./pages/GovernancePage").then((m) => ({ default: m.GovernancePage }))
);
const IncidentsPage = lazy(() =>
  import("./pages/IncidentsPage").then((m) => ({ default: m.IncidentsPage }))
);
const AwarenessPage = lazy(() =>
  import("./pages/AwarenessPage").then((m) => ({ default: m.AwarenessPage }))
);
const HistoryPage = lazy(() =>
  import("./pages/HistoryPage").then((m) => ({ default: m.HistoryPage }))
);
const ReportsPage = lazy(() =>
  import("./pages/ReportsPage").then((m) => ({ default: m.ReportsPage }))
);
const SettingsPage = lazy(() =>
  import("./pages/SettingsPage").then((m) => ({ default: m.SettingsPage }))
);
const DocsPage = lazy(() =>
  import("./pages/DocsPage").then((m) => ({ default: m.DocsPage }))
);

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) {
    return (
      <div className="flex min-h-[100dvh] items-center justify-center bg-[#080D1B] p-6">
        <Skeleton className="h-32 w-full max-w-md" />
      </div>
    );
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
}

export function AppRoutes() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-[100dvh] items-center justify-center bg-[#080D1B] p-6">
          <Skeleton className="h-32 w-full max-w-md" />
        </div>
      }
    >
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<AuthPage mode="login" />} />
        <Route path="/register" element={<AuthPage mode="register" />} />

        <Route
          path="/app"
          element={
            <ProtectedRoute>
              <AppShell />
            </ProtectedRoute>
          }
        >
          <Route index element={<OverviewPage />} />
          <Route path="phishing" element={<PhishingDetectorPage />} />
          <Route path="url-scanner" element={<UrlScannerPage />} />
          <Route path="assessment" element={<AssessmentPage />} />
          <Route path="governance" element={<GovernancePage />} />
          <Route path="incidents" element={<IncidentsPage />} />
          <Route path="awareness" element={<AwarenessPage />} />
          <Route path="history" element={<HistoryPage />} />
          <Route path="reports" element={<ReportsPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="docs" element={<DocsPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </LanguageProvider>
  );
}

