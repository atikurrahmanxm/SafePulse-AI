const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api";
const TOKEN_KEY = "cybershield_token";
const BUSINESS_KEY = "cybershield_business_id";

export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string | null): void {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    localStorage.removeItem(TOKEN_KEY);
  }
}

export function getStoredBusinessId(): number | null {
  const raw = localStorage.getItem(BUSINESS_KEY);
  if (!raw) return null;
  const parsed = Number(raw);
  return Number.isInteger(parsed) && parsed > 0 ? parsed : null;
}

export function setStoredBusinessId(businessId: number | null): void {
  if (businessId && businessId > 0) {
    localStorage.setItem(BUSINESS_KEY, String(businessId));
  } else {
    localStorage.removeItem(BUSINESS_KEY);
  }
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getStoredToken();
  const businessId = getStoredBusinessId();
  const headers = new Headers(options.headers || {});
  if (!headers.has("Content-Type") && options.body) {
    headers.set("Content-Type", "application/json");
  }
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  if (businessId && !headers.has("X-Business-Id")) {
    headers.set("X-Business-Id", String(businessId));
  }

  const normalizedPath = path.startsWith("/api") ? path : `${API_BASE}${path}`;
  const res = await fetch(normalizedPath, { ...options, headers });

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const body = await res.json();
      if (typeof body.detail === "string") {
        detail = body.detail;
      } else if (Array.isArray(body.detail) && body.detail.length > 0) {
        detail = body.detail.map((d: { msg?: string }) => d.msg || "Validation error").join("; ");
      }
    } catch {
      // Fallback to status text
    }
    throw new ApiError(res.status, detail);
  }

  return (await res.json()) as T;
}

export async function downloadPdfReport(path: string, filename: string): Promise<void> {
  const token = getStoredToken();
  const businessId = getStoredBusinessId();
  const headers: Record<string, string> = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  if (businessId) headers["X-Business-Id"] = String(businessId);
  const normalizedPath = path.startsWith("/api") ? path : `${API_BASE}${path}`;
  const res = await fetch(normalizedPath, { headers });
  if (!res.ok) {
    throw new ApiError(res.status, "Unable to generate PDF report.");
  }
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

