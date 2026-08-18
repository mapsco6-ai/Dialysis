import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/useAuth";
import { Logo } from "../components/ui/Logo";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await login(username, password);
      navigate("/", { replace: true });
    } catch {
      setError("اسم المستخدم أو كلمة المرور غير صحيحة");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-ink-900 p-4">
      <div className="relative w-full max-w-md">
        <div className="absolute -inset-6 -z-10 rounded-[2rem] bg-brand-700/30 blur-2xl" />
        <div className="rounded-3xl bg-white p-8 shadow-2xl">
          <Logo className="mb-1" />
          <p className="mb-8 mt-1 text-sm text-ink-500">نظام إدارة مركز الديلزة</p>

          <h1 className="mb-6 text-xl font-bold text-ink-900">تسجيل الدخول</h1>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <div>
              <label className="mb-1.5 block text-sm font-medium text-ink-700">
                اسم المستخدم
              </label>
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                autoFocus
                className="w-full rounded-xl border border-surface-300 bg-surface-50 px-4 py-2.5 text-sm outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100"
                placeholder="ادخل اسم المستخدم"
              />
            </div>
            <div>
              <label className="mb-1.5 block text-sm font-medium text-ink-700">
                كلمة المرور
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full rounded-xl border border-surface-300 bg-surface-50 px-4 py-2.5 text-sm outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100"
                placeholder="••••••••"
              />
            </div>

            {error && (
              <p className="rounded-lg bg-coral-50 px-3 py-2 text-sm text-coral-700">{error}</p>
            )}

            <button
              type="submit"
              disabled={isSubmitting}
              className="mt-2 rounded-xl bg-brand-600 py-2.5 text-sm font-semibold text-white transition hover:bg-brand-700 disabled:opacity-60"
            >
              {isSubmitting ? "جارٍ الدخول..." : "دخول"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
