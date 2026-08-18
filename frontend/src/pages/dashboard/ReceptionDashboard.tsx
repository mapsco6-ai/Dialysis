import { useMemo } from "react";
import { Users, CalendarCheck2, HeartPulse, Gauge, UserPlus } from "lucide-react";
import { AppShell } from "../../components/layout/AppShell";
import { StatCard } from "../../components/ui/StatCard";
import { Card } from "../../components/ui/Card";
import { StatusBadge } from "../../components/ui/StatusBadge";
import { WeeklySessionsChart } from "../../components/dashboard/WeeklySessionsChart";
import { useAuth } from "../../auth/useAuth";
import { useDialysisSessions, useMachines, usePatients } from "../../api/hooks";
import { todayIso } from "../../lib/dates";

export function ReceptionDashboard() {
  const { user } = useAuth();
  const patientsQuery = usePatients();
  const machinesQuery = useMachines();
  const sessionsQuery = useDialysisSessions();

  const today = todayIso();
  const sessions = sessionsQuery.data?.results ?? [];
  const machines = machinesQuery.data?.results ?? [];

  const todaysSessions = useMemo(
    () => sessions.filter((s) => s.scheduled_date === today),
    [sessions, today],
  );
  const availableMachines = useMemo(
    () => machines.filter((m) => m.status === "available"),
    [machines],
  );
  const occupancyRate = machines.length
    ? Math.round((todaysSessions.filter((s) => s.machine).length / machines.length) * 100)
    : 0;
  const machineCodeById = useMemo(
    () => new Map(machines.map((m) => [m.id, m.code])),
    [machines],
  );

  const todayLabel = new Date().toLocaleDateString("ar-IQ-u-ca-gregory", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <AppShell>
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-ink-900">
            أهلاً بعودتك، <span className="text-brand-600">{user?.fullName}</span>
          </h1>
          <p className="mt-1 text-sm text-surface-300">{todayLabel}</p>
        </div>
        <button className="flex items-center gap-2 rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700">
          <UserPlus size={16} />
          تسجيل مريض جديد
        </button>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          label="إجمالي المرضى"
          value={patientsQuery.isLoading ? "…" : String(patientsQuery.data?.count ?? 0)}
          icon={Users}
          tone="brand"
        />
        <StatCard
          label="جلسات اليوم"
          value={sessionsQuery.isLoading ? "…" : String(todaysSessions.length)}
          icon={CalendarCheck2}
          tone="coral"
        />
        <StatCard
          label="الأجهزة المتاحة"
          value={
            machinesQuery.isLoading
              ? "…"
              : `${availableMachines.length}/${machines.length}`
          }
          icon={HeartPulse}
          tone="ink"
        />
        <StatCard
          label="نسبة إشغال الأجهزة"
          value={`${occupancyRate}%`}
          icon={Gauge}
          tone="brand"
        />
      </div>

      <div className="mt-4 grid grid-cols-1 gap-4 xl:grid-cols-3">
        <Card
          title="الجلسات خلال آخر ٧ أيام"
          subtitle="عدد جلسات الغسيل يوميًا"
          className="xl:col-span-2"
        >
          <WeeklySessionsChart sessions={sessions} />
        </Card>

        <Card title="جلسات اليوم" subtitle={`${todaysSessions.length} جلسة مسجلة`}>
          {todaysSessions.length === 0 ? (
            <p className="py-10 text-center text-sm text-surface-300">
              لا توجد جلسات لهذا اليوم بعد
            </p>
          ) : (
            <ul className="flex flex-col gap-3">
              {todaysSessions.slice(0, 5).map((s) => (
                <li key={s.id} className="flex items-center justify-between">
                  <span className="text-sm font-medium text-ink-800">{s.patient_name}</span>
                  <StatusBadge status={s.status} />
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>

      <Card title="تفاصيل جلسات اليوم" className="mt-4">
        {todaysSessions.length === 0 ? (
          <p className="py-10 text-center text-sm text-surface-300">
            لم يتم تسجيل حضور أي مريض حتى الآن اليوم
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-start text-sm">
              <thead>
                <tr className="border-b border-surface-100 text-surface-300">
                  <th className="py-2 text-start font-medium">المريض</th>
                  <th className="py-2 text-start font-medium">الجهاز</th>
                  <th className="py-2 text-start font-medium">الحالة</th>
                </tr>
              </thead>
              <tbody>
                {todaysSessions.map((s) => (
                  <tr key={s.id} className="border-b border-surface-50 last:border-0">
                    <td className="py-3 font-medium text-ink-800">{s.patient_name}</td>
                    <td className="py-3 text-surface-300">
                      {s.machine ? (machineCodeById.get(s.machine) ?? s.machine) : "—"}
                    </td>
                    <td className="py-3">
                      <StatusBadge status={s.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </AppShell>
  );
}
