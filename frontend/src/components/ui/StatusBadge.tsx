const STATUS_LABELS_AR: Record<string, string> = {
  scheduled: "مجدولة",
  checked_in: "تم تسجيل الحضور",
  in_progress: "جارية",
  completed: "مكتملة",
  cancelled: "ملغاة",
  no_show: "لم يحضر",
  available: "متاح",
  in_use: "قيد الاستخدام",
  maintenance: "صيانة",
  out_of_service: "خارج الخدمة",
};

const STATUS_STYLES: Record<string, string> = {
  scheduled: "bg-surface-100 text-ink-600",
  checked_in: "bg-brand-50 text-brand-700",
  in_progress: "bg-amber-50 text-amber-700",
  completed: "bg-emerald-50 text-emerald-700",
  cancelled: "bg-coral-50 text-coral-700",
  no_show: "bg-coral-50 text-coral-700",
};

export function StatusBadge({ status }: { status: string }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold ${
        STATUS_STYLES[status] ?? "bg-surface-100 text-ink-600"
      }`}
    >
      <span className="h-1.5 w-1.5 rounded-full bg-current" />
      {STATUS_LABELS_AR[status] ?? status}
    </span>
  );
}
