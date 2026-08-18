import { NavLink } from "react-router-dom";
import { LogOut } from "lucide-react";
import { useAuth } from "../../auth/useAuth";
import { NAV_ITEMS } from "./navConfig";
import { Logo } from "../ui/Logo";

export function Sidebar() {
  const { user, hasRole, logout } = useAuth();

  const visibleItems = NAV_ITEMS.filter(
    (item) => item.roles === "all" || hasRole(...item.roles),
  );

  return (
    <aside className="sticky top-0 flex h-screen w-64 shrink-0 flex-col bg-ink-900 p-4 text-surface-100">
      <div className="mb-8 rounded-2xl bg-white/5 p-3">
        <Logo className="[&_span]:text-white" />
      </div>

      <nav className="flex flex-1 flex-col gap-1">
        {visibleItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-medium transition ${
                isActive
                  ? "bg-brand-500 text-white shadow-sm"
                  : "text-surface-200/80 hover:bg-white/5 hover:text-white"
              }`
            }
          >
            <item.icon size={18} strokeWidth={2} />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="mt-4 border-t border-white/10 pt-4">
        <div className="mb-3 px-1 text-xs text-surface-300/70">{user?.fullName}</div>
        <button
          onClick={logout}
          className="flex w-full items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-medium text-coral-300 transition hover:bg-white/5"
        >
          <LogOut size={18} />
          تسجيل الخروج
        </button>
      </div>
    </aside>
  );
}
