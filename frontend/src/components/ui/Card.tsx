import type { ReactNode } from "react";

export function Card({
  title,
  subtitle,
  action,
  children,
  className,
}: {
  title?: string;
  subtitle?: string;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={`rounded-2xl bg-white p-5 shadow-sm ${className ?? ""}`}>
      {(title || action) && (
        <div className="mb-4 flex items-start justify-between">
          <div>
            {title && <h3 className="text-base font-bold text-ink-900">{title}</h3>}
            {subtitle && <p className="text-xs text-surface-300">{subtitle}</p>}
          </div>
          {action}
        </div>
      )}
      {children}
    </div>
  );
}
