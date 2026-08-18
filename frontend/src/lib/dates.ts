const WEEKDAY_LABELS_AR = ["أحد", "اثنين", "ثلاثاء", "أربعاء", "خميس", "جمعة", "سبت"];

export function todayIso(): string {
  return new Date().toISOString().slice(0, 10);
}

export function lastNDays(n: number): { iso: string; label: string }[] {
  const days: { iso: string; label: string }[] = [];
  for (let i = n - 1; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    days.push({ iso: d.toISOString().slice(0, 10), label: WEEKDAY_LABELS_AR[d.getDay()] });
  }
  return days;
}
