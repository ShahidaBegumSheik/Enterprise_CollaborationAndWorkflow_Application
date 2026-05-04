import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(form.email, form.password);
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-linear-to-br from-indigo-950 via-slate-900 to-sky-900 p-4">
      <div className="grid w-full max-w-5xl overflow-hidden rounded-4xl bg-white shadow-2xl md:grid-cols-2">
        <div className="hidden bg-linear-to-br from-indigo-600 to-sky-500 p-10 text-white md:block">
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-indigo-100">Mini Enterprise Collaboration and Workflow APPLICATION</p>
          <h1 className="mt-8 text-5xl font-black leading-tight">Manage tasks, approvals and documents.</h1>
          <p className="mt-6 text-indigo-100">A role-based collaboration system for Admins, Managers and Employees.</p>
          <div className="mt-10 grid gap-3 text-sm font-semibold">
            <div className="rounded-2xl bg-white/15 p-4">✅ Task assignment and tracking</div>
            <div className="rounded-2xl bg-white/15 p-4">🧩 Kanban workflow board</div>
            <div className="rounded-2xl bg-white/15 p-4">🔄 Multi-level approvals</div>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="p-8 md:p-10">
          <h2 className="text-3xl font-black text-slate-900">Welcome back</h2>
          <p className="mt-2 text-sm text-slate-500">Login to continue to your workspace.</p>

          {error && <p className="mt-5 rounded-2xl bg-rose-50 p-3 text-sm font-semibold text-rose-700">{error}</p>}

          <label className="mt-6 block text-sm font-bold text-slate-700">Email</label>
          <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-indigo-500 transition focus:ring-2" required />

          <label className="mt-4 block text-sm font-bold text-slate-700">Password</label>
          <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-indigo-500 transition focus:ring-2" required />

          <button disabled={loading} className="mt-6 w-full rounded-2xl bg-indigo-600 py-3 font-black text-white shadow-lg shadow-indigo-600/25 transition hover:bg-indigo-700 disabled:opacity-60">
            {loading ? "Signing in..." : "Sign In"}
          </button>

          <p className="mt-6 text-center text-sm text-slate-600">
            Don&apos;t have an account? <Link to="/register" className="font-black text-indigo-600 hover:underline">Register</Link>
          </p>
        </form>
      </div>
    </div>
  );
}
