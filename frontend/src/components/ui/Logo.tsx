export function Logo({ className }: { className?: string }) {
  return (
    <div className={`flex items-center gap-2 ${className ?? ""}`}>
      <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-500 text-white shadow-sm">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
          <path
            d="M2 12h4l2-7 4 14 3-9 2 5h5"
            stroke="currentColor"
            strokeWidth="2.4"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
      <span className="text-lg font-bold text-ink-900">نبض</span>
    </div>
  );
}
