import type { ReactNode } from "react";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen bg-surface-100">
      <Sidebar />
      <div className="min-w-0 flex-1">
        <Topbar />
        <main className="px-8 pb-8 pt-6">{children}</main>
      </div>
    </div>
  );
}
