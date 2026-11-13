import React from "react";
import { AlertCircle, ShieldCheck } from "lucide-react";
import { cn, getRiskColor } from "../../lib/utils";

export function Card({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "cs-card rounded-2xl border border-slate-700/60 transition-[border-color,box-shadow] duration-200 hover:border-slate-600/80",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div className={cn("flex items-center justify-between gap-3 border-b border-slate-800/80 px-5 py-4", className)}>
      {children}
    </div>
  );
}

export function CardContent({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return <div className={cn("p-5", className)}>{children}</div>;
}

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
}

export function Button({
  variant = "primary",
  size = "md",
  className,
  children,
  ...props
}: ButtonProps) {
  const variants = {
    primary:
      "bg-gradient-to-r from-[#6366F1] via-[#5558E6] to-[#0891B2] text-white hover:brightness-110 border border-indigo-400/30 shadow-[0_6px_18px_-6px_rgba(99,102,241,0.55)]",
    secondary:
      "bg-[#182640]/90 text-slate-100 hover:bg-[#213354] border border-slate-700/80 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.05)]",
    ghost:
      "bg-transparent text-slate-300 hover:bg-[#1B2942]/70 hover:text-white border border-transparent",
    danger:
      "bg-red-500/15 text-red-200 hover:bg-red-500/25 border border-red-500/40",
  };
  const sizes = {
    sm: "px-3 py-1.5 text-xs min-h-[32px]",
    md: "px-4 py-2 text-sm min-h-[38px]",
    lg: "px-5 py-2.5 text-sm font-semibold min-h-[44px]",
  };
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-xl font-medium transition-all active:scale-[0.99] disabled:cursor-not-allowed disabled:opacity-50",
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}

export function RiskBadge({
  category,
  className,
}: {
  category: string;
  className?: string;
}) {
  const palette = getRiskColor(category);
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium",
        palette.bg,
        palette.text,
        palette.border,
        className
      )}
    >
      <span
        className="h-1.5 w-1.5 rounded-full"
        style={{ backgroundColor: palette.hex }}
        aria-hidden="true"
      />
      {category}
    </span>
  );
}

export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn("animate-pulse rounded-lg bg-[#1B2942]/80", className)}
      aria-hidden="true"
    />
  );
}

export function ErrorBanner({
  message,
  onDismiss,
}: {
  message: string;
  onDismiss?: () => void;
}) {
  return (
    <div
      role="alert"
      className="flex items-start justify-between gap-3 rounded-xl border border-red-500/35 bg-red-500/10 px-4 py-3 text-sm text-red-200"
    >
      <div className="flex items-start gap-2.5">
        <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-red-400" aria-hidden="true" />
        <span>{message}</span>
      </div>
      {onDismiss && (
        <button
          type="button"
          onClick={onDismiss}
          className="text-xs text-red-300 underline hover:text-white"
        >
          Dismiss
        </button>
      )}
    </div>
  );
}

export function EmptyState({
  title,
  description,
  action,
}: {
  title: string;
  description: string;
  action?: React.ReactNode;
}) {
  return (
    <Card className="border-dashed border-slate-700/80 bg-[#10182B]/70">
      <div className="flex flex-col items-center justify-center px-6 py-12 text-center">
        <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-xl border border-indigo-500/30 bg-indigo-500/10 text-indigo-400">
          <ShieldCheck className="h-6 w-6" aria-hidden="true" />
        </div>
        <h3 className="text-base font-semibold text-slate-100">{title}</h3>
        <p className="mt-1.5 max-w-md text-sm text-slate-400">{description}</p>
        {action && <div className="mt-5">{action}</div>}
      </div>
    </Card>
  );
}

