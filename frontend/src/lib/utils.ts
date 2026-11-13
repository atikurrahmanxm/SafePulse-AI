import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getRiskColor(category: string): {
  text: string;
  bg: string;
  border: string;
  hex: string;
} {
  const norm = category.toLowerCase();
  if (norm.includes("critical")) {
    return {
      text: "text-red-400",
      bg: "bg-red-500/15",
      border: "border-red-500/35",
      hex: "#EF4444",
    };
  }
  if (norm.includes("high") || norm.includes("weak")) {
    return {
      text: "text-amber-400",
      bg: "bg-amber-500/15",
      border: "border-amber-500/35",
      hex: "#F59E0B",
    };
  }
  if (norm.includes("moderate")) {
    return {
      text: "text-cyan-300",
      bg: "bg-cyan-500/15",
      border: "border-cyan-500/35",
      hex: "#06B6D4",
    };
  }
  if (norm.includes("low") || norm.includes("good") || norm.includes("strong")) {
    return {
      text: "text-emerald-400",
      bg: "bg-emerald-500/15",
      border: "border-emerald-500/35",
      hex: "#22C55E",
    };
  }
  return {
    text: "text-slate-300",
    bg: "bg-slate-500/15",
    border: "border-slate-500/35",
    hex: "#94A3B8",
  };
}

export function getHealthScoreColor(score: number | null | undefined): string {
  if (score === null || score === undefined) return "#94A3B8";
  if (score < 30) return "#EF4444";
  if (score < 50) return "#F59E0B";
  if (score < 70) return "#06B6D4";
  return "#22C55E";
}

export function formatTimestamp(iso: string): string {
  try {
    return new Intl.DateTimeFormat("en-IN", {
      dateStyle: "medium",
      timeStyle: "short",
    }).format(new Date(iso));
  } catch {
    return iso;
  }
}

