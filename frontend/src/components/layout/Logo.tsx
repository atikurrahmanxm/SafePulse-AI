import { useId } from "react";
import { cn } from "../../lib/utils";

export function Logo({
  compact = false,
  size = "md",
}: {
  compact?: boolean;
  size?: "sm" | "md" | "lg";
}) {
  const uid = useId().replace(/:/g, "");
  const bgId = `sp-bg-${uid}`;
  const shieldId = `sp-shield-${uid}`;
  const pulseId = `sp-pulse-${uid}`;

  const boxSizes = {
    sm: "h-8 w-8 rounded-lg",
    md: "h-10 w-10 rounded-xl",
    lg: "h-12 w-12 rounded-2xl",
  }[size];

  const svgSizes = {
    sm: 20,
    md: 24,
    lg: 28,
  }[size];

  return (
    <div className="flex items-center gap-2.5 select-none">
      <div
        className={cn(
          "relative flex shrink-0 items-center justify-center border border-indigo-400/35 bg-[#0F172A] shadow-[0_6px_22px_-6px_rgba(6,182,212,0.55)]",
          boxSizes
        )}
      >
        <svg
          width={svgSizes}
          height={svgSizes}
          viewBox="0 0 64 64"
          fill="none"
          aria-hidden="true"
        >
          <defs>
            <linearGradient id={bgId} x1="12" y1="8" x2="52" y2="56" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stopColor="#1E1B4B" />
              <stop offset="100%" stopColor="#083344" />
            </linearGradient>
            <linearGradient id={shieldId} x1="15" y1="10" x2="49" y2="54" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stopColor="#818CF8" />
              <stop offset="55%" stopColor="#06B6D4" />
              <stop offset="100%" stopColor="#34D399" />
            </linearGradient>
            <linearGradient id={pulseId} x1="17" y1="33" x2="47" y2="33" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stopColor="#38BDF8" />
              <stop offset="60%" stopColor="#22D3EE" />
              <stop offset="100%" stopColor="#34D399" />
            </linearGradient>
          </defs>
          {/* Shield Base */}
          <path
            d="M32 7L12 15.5V31C12 43.5 20.6 53.5 32 57C43.4 53.5 52 43.5 52 31V15.5L32 7Z"
            fill={`url(#${bgId})`}
            stroke={`url(#${shieldId})`}
            strokeWidth="3.5"
            strokeLinejoin="round"
          />
          {/* Upper Radar/Signal Arc */}
          <path
            d="M23 21C25.8 19 28.8 18 32 18C35.2 18 38.2 19 41 21"
            stroke="#818CF8"
            strokeOpacity="0.7"
            strokeWidth="2.2"
            strokeLinecap="round"
          />
          {/* Dynamic Heartbeat / SafePulse Wave */}
          <path
            d="M19 33.5H25L28.5 25L32.5 41L36 30L38.5 35H45"
            stroke={`url(#${pulseId})`}
            strokeWidth="3.6"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <circle cx="32" cy="13.5" r="2.2" fill="#22D3EE" />
          <circle cx="45" cy="35" r="1.8" fill="#34D399" />
        </svg>
      </div>
      {!compact && (
        <div className="leading-tight">
          <div
            className={cn(
              "flex items-center gap-1.5 font-bold tracking-tight text-slate-50",
              size === "lg" ? "text-lg" : "text-sm"
            )}
          >
            <span>SafePulse</span>
            <span className="rounded-md border border-cyan-400/35 bg-cyan-400/15 px-1.5 py-0.5 text-[11px] font-bold tracking-wide text-cyan-300">
              AI
            </span>
          </div>
          <div className="mt-0.5 text-[11px] font-medium text-slate-400">
            Smart SME Protection
          </div>
        </div>
      )}
    </div>
  );
}
