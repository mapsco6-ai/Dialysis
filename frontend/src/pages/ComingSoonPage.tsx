import { AppShell } from "../components/layout/AppShell";

export function ComingSoonPage({ title }: { title: string }) {
  return (
    <AppShell>
      <h1 className="mb-6 text-2xl font-bold text-ink-900">{title}</h1>
      <div className="flex h-96 flex-col items-center justify-center gap-3 rounded-3xl bg-white text-center shadow-sm">
        <div className="text-4xl">🚧</div>
        <p className="text-lg font-semibold text-ink-900">هذه الشاشة قيد الإنشاء</p>
        <p className="text-sm text-surface-300">سيتم بناء وحدة {title} في المرحلة القادمة</p>
      </div>
    </AppShell>
  );
}
