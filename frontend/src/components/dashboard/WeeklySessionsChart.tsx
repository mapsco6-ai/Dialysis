import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis } from "recharts";
import { lastNDays } from "../../lib/dates";
import type { DialysisSession } from "../../api/types";

export function WeeklySessionsChart({ sessions }: { sessions: DialysisSession[] }) {
  const days = lastNDays(7);
  const data = days.map(({ iso, label }) => ({
    label,
    count: sessions.filter((s) => s.scheduled_date === iso).length,
  }));

  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data} barCategoryGap="28%">
        <XAxis
          dataKey="label"
          axisLine={false}
          tickLine={false}
          tick={{ fill: "#8a9a97", fontSize: 12 }}
        />
        <Tooltip
          cursor={{ fill: "#f6f8f7" }}
          contentStyle={{ borderRadius: 12, border: "1px solid #e2e8e6", direction: "rtl" }}
          formatter={(value) => [`${value} جلسة`, ""]}
        />
        <Bar dataKey="count" radius={[8, 8, 8, 8]} fill="#23978a" maxBarSize={36} />
      </BarChart>
    </ResponsiveContainer>
  );
}
