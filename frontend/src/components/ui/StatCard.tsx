import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string;
  icon: LucideIcon;
  hint?: string;
  tone?: "brand" | "coral" | "ink";
}

const TONE_STYLES: Record<NonNullable<StatCardProps["tone"]>, string> = {
  brand: "bg-brand-50 text-brand-600",
  coral: "bg-coral-50 text-coral-600",
  ink: "bg-surface-100 text-ink-700",
};

export function StatCard({ label, value, icon: Icon, hint, tone = "brand" }: StatCardProps) {
  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-surface-300">{label}</span>
        <div className={`flex h-9 w-9 items-center justify-center rounded-xl ${TONE_STYLES[tone]}`}>
          <Icon size={18} />
        </div>
      </div>
      <div className="mt-4 text-3xl font-bold text-ink-900">{value}</div>
      {hint && <div className="mt-1 text-xs text-surface-300">{hint}</div>}
    </div>
  );
}
