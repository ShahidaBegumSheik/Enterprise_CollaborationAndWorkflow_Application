import { useEffect, useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import { getDashboardSummary } from "../api/dashboardApi";

function StatCard({ title, value, icon, gradient }) {
  return (
    <div className={`rounded-3xl bg-linear-to-br ${gradient} p-6 text-white shadow-xl`}>
      <div className="flex items-center justify-between">
        <p className="text-sm font-bold uppercase tracking-wide text-white/80">{title}</p>
        <span className="text-3xl">{icon}</span>
      </div>
      <h3 className="mt-5 text-4xl font-black">{value ?? 0}</h3>
    </div>
  );
}

function DistributionBar({ label, value, total, color }) {
  const percent = total ? Math.round((value / total) * 100) : 0;
  return (
    <div>
      <div className="mb-2 flex justify-between text-sm font-bold text-slate-700">
        <span>{label}</span>
        <span>{value} • {percent}%</span>
      </div>
      <div className="h-3 overflow-hidden rounded-full bg-slate-100">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${percent}%` }} />
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");

  /* async function loadData() {
    try {
      const data = await getDashboardSummary();
      setSummary(data);
    } catch (err) {
      console.error(err);
      setError("Unable to load dashboard summary");
    }
  } */

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getDashboardSummary();
        setSummary(data);
      } catch (err) {
        console.error(err);
        setError('Unable to laod dashboard summary");')
      }
    }
    fetchData();
  }, []);

  const total = summary?.total_tasks || 0;

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="overflow-hidden rounded-4xl bg-linear-to-r from-indigo-600 via-violet-600 to-sky-500 p-8 text-white shadow-2xl">
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-white/75">Dashboard</p>
          <h2 className="mt-3 text-3xl font-black md:text-4xl">Role-based enterprise overview</h2>
          <p className="mt-3 max-w-2xl text-white/80">Track task progress, pending workload and delivery distribution across the workflow.</p>
        </div>

        {error && <div className="rounded-2xl bg-rose-50 p-4 font-semibold text-rose-700">{error}</div>}

        {!summary ? (
          <div className="rounded-3xl bg-white p-8 text-center font-bold text-slate-500 shadow">Loading dashboard...</div>
        ) : (
          <>
            <div className="grid gap-4 md:grid-cols-3">
              <StatCard title="Total Tasks" value={summary.total_tasks} icon="📋" gradient="from-indigo-600 to-blue-500" />
              <StatCard title="Completed" value={summary.done_tasks} icon="✅" gradient="from-emerald-500 to-teal-500" />
              <StatCard title="Pending" value={summary.pending_tasks} icon="⏳" gradient="from-rose-500 to-orange-500" />
            </div>

            <div className="grid gap-6 lg:grid-cols-3">
              <div className="rounded-3xl bg-white p-6 shadow-xl lg:col-span-2">
                <h3 className="text-xl font-black text-slate-900">Task Distribution</h3>
                <div className="mt-6 space-y-5">
                  <DistributionBar label="To Do" value={summary.todo_tasks} total={total} color="bg-sky-500" />
                  <DistributionBar label="In Progress" value={summary.in_progress_tasks} total={total} color="bg-indigo-500" />
                  <DistributionBar label="Review" value={summary.review_tasks} total={total} color="bg-amber-500" />
                  <DistributionBar label="Done" value={summary.done_tasks} total={total} color="bg-emerald-500" />
                </div>
              </div>

              <div className="rounded-3xl bg-slate-950 p-6 text-white shadow-xl">
                <p className="text-sm font-bold uppercase tracking-widest text-indigo-300">AI Summary</p>
                <h3 className="mt-4 text-2xl font-black">Focus Area</h3>
                <p className="mt-3 text-sm leading-6 text-slate-300">
                  {summary.pending_tasks > summary.done_tasks
                    ? "Prioritize pending and review tasks. Move high-priority items through the Kanban board first."
                    : "Good progress. Keep monitoring review-stage tasks before final completion."}
                </p>
              </div>
            </div>
          </>
        )}
      </div>
    </AppLayout>
  );
}
