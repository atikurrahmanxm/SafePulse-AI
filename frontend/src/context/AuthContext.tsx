import React, { createContext, useCallback, useContext, useEffect, useState } from "react";
import { apiRequest, getStoredBusinessId, getStoredToken, setStoredBusinessId, setStoredToken } from "../lib/api";

export interface BusinessProfile {
  id: number;
  name: string;
  industry: string;
  employee_count: number;
  city: string;
  primary_email_domain?: string | null;
  subscription_tier?: string;
  monthly_scan_quota?: number;
  is_demo_workspace: boolean;
}

export interface UserProfile {
  id: number;
  email: string;
  full_name: string;
  role: string;
  preferred_language: "en" | "bn";
  is_demo: boolean;
  business: BusinessProfile;
  businesses?: BusinessProfile[];
}

interface AuthResponse {
  access_token: string;
  token_type: string;
  user: UserProfile;
}

interface RegisterPayload {
  email: string;
  password: string;
  full_name: string;
  business_name: string;
  industry: string;
  employee_count: number;
  city: string;
}

interface CreateBusinessPayload {
  name: string;
  industry: string;
  employee_count: number;
  city: string;
  primary_email_domain?: string;
}

interface AuthContextValue {
  user: UserProfile | null;
  loading: boolean;
  workspaceNotice: string | null;
  clearWorkspaceNotice: () => void;
  login: (email: string, password: string) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  startDemoMode: () => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  switchBusiness: (businessId: number) => Promise<void>;
  createBusiness: (payload: CreateBusinessPayload) => Promise<BusinessProfile>;
  setUserDirect: (user: UserProfile) => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [workspaceNotice, setWorkspaceNotice] = useState<string | null>(null);

  const refreshUser = useCallback(async () => {
    const token = getStoredToken();
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const me = await apiRequest<UserProfile>("/api/auth/me");
      if (!getStoredBusinessId() && me.business?.id) {
        setStoredBusinessId(me.business.id);
      }
      setUser(me);
    } catch {
      setStoredToken(null);
      setStoredBusinessId(null);
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  const login = async (email: string, password: string) => {
    setStoredBusinessId(null);
    const res = await apiRequest<AuthResponse>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    setStoredToken(res.access_token);
    if (res.user.business?.id) setStoredBusinessId(res.user.business.id);
    setUser(res.user);
  };

  const register = async (payload: RegisterPayload) => {
    setStoredBusinessId(null);
    const res = await apiRequest<AuthResponse>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    setStoredToken(res.access_token);
    if (res.user.business?.id) setStoredBusinessId(res.user.business.id);
    setUser(res.user);
  };

  const startDemoMode = async () => {
    setStoredBusinessId(null);
    const res = await apiRequest<AuthResponse>("/api/auth/demo", {
      method: "POST",
    });
    setStoredToken(res.access_token);
    if (res.user.business?.id) setStoredBusinessId(res.user.business.id);
    setUser(res.user);
  };

  const switchBusiness = async (businessId: number) => {
    setStoredBusinessId(businessId);
    const me = await apiRequest<UserProfile>("/api/auth/me");
    setWorkspaceNotice(`Switched active workspace: ${me.business.name}`);
    setUser(me);
  };

  const createBusiness = async (payload: CreateBusinessPayload) => {
    const created = await apiRequest<BusinessProfile>("/api/auth/businesses", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    setStoredBusinessId(created.id);
    const me = await apiRequest<UserProfile>("/api/auth/me");
    setWorkspaceNotice(`Switched to new business workspace: ${created.name}`);
    setUser(me);
    return created;
  };

  const logout = async () => {
    try {
      if (getStoredToken()) {
        await apiRequest("/api/auth/logout", { method: "POST" });
      }
    } catch {
      // Ignore network errors during logout
    } finally {
      setStoredToken(null);
      setStoredBusinessId(null);
      setWorkspaceNotice(null);
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        workspaceNotice,
        clearWorkspaceNotice: () => setWorkspaceNotice(null),
        login,
        register,
        startDemoMode,
        logout,
        refreshUser,
        switchBusiness,
        createBusiness,
        setUserDirect: setUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}

