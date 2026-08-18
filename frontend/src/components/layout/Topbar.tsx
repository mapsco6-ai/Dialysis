import { Search, Bell } from "lucide-react";
import { useAuth } from "../../auth/useAuth";
import { ROLE_LABELS_AR } from "../../auth/roles";

export function Topbar() {
  const { user } = useAuth();
  const primaryRole = user?.roles[0];
  const initials = (user?.fullName ?? "؟").trim().charAt(0);

  return (
    <header className="flex items-center justify-end gap-3 px-8 pt-6">
      <div className="hidden items-center gap-2 rounded-full bg-white px-4 py-2 shadow-sm md:flex">
        <Search size={16} className="text-surface-300" />
        <input
          placeholder="بحث..."
          className="w-40 bg-transparent text-sm outline-none placeholder:text-surface-300"
        />
      </div>

      <button className="relative flex h-10 w-10 items-center justify-center rounded-full bg-white shadow-sm">
        <Bell size={18} className="text-ink-700" />
        <span className="absolute end-2 top-2 h-2 w-2 rounded-full bg-coral-500" />
      </button>

      <div className="flex items-center gap-2.5 rounded-full bg-white py-1.5 ps-1.5 pe-4 shadow-sm">
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-brand-100 text-sm font-bold text-brand-700">
          {initials}
        </div>
        <div className="leading-tight">
          <div className="text-sm font-semibold text-ink-900">{user?.fullName}</div>
          <div className="text-xs text-surface-300">
            {primaryRole ? ROLE_LABELS_AR[primaryRole] : ""}
          </div>
        </div>
      </div>
    </header>
  );
}
