import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api/authApi";

export default function RegisterPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ full_name: "", email: "", password: "", role: "employee" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await registerUser(form);
      navigate("/login");
    } catch (err) {
      console.error(err);
      setError("Registration failed. Please check backend validation and try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-linear-to-br from-sky-950 via-indigo-950 to-slate-900 p-4">
      <form onSubmit={handleSubmit} className="w-full max-w-lg rounded-4xl bg-white p-8 shadow-2xl md:p-10">
        <p className="text-sm font-semibold uppercase tracking-[0.25em] text-indigo-600">Create account</p>
        <h1 className="mt-2 text-3xl font-black text-slate-900">Join Enterprise Collaboration and Workflow</h1>
        <p className="mt-2 text-sm text-slate-500">Register as Employee, Manager or Admin.</p>

        {error && <p className="mt-5 rounded-2xl bg-rose-50 p-3 text-sm font-semibold text-rose-700">{error}</p>}

        <label className="mt-6 block text-sm font-bold text-slate-700">Full Name</label>
        <input value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-indigo-500 focus:ring-2" required />

        <label className="mt-4 block text-sm font-bold text-slate-700">Email</label>
        <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-indigo-500 focus:ring-2" required />

        <label className="mt-4 block text-sm font-bold text-slate-700">Password</label>
        <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-indigo-500 focus:ring-2" required />

        <label className="mt-4 block text-sm font-bold text-slate-700">Role</label>
        <select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-indigo-500 focus:ring-2">
          <option value="employee">Employee</option>
          <option value="manager">Manager</option>
          <option value="admin">Admin</option>
        </select>

        <button disabled={loading} className="mt-6 w-full rounded-2xl bg-indigo-600 py-3 font-black text-white shadow-lg shadow-indigo-600/25 transition hover:bg-indigo-700 disabled:opacity-60">
          {loading ? "Creating..." : "Register"}
        </button>

        <p className="mt-6 text-center text-sm text-slate-600">Already have an account? <Link to="/login" className="font-black text-indigo-600 hover:underline">Login</Link></p>
      </form>
    </div>
  );
}
