import { useEffect, useState } from "react";
import { getDashboardSummary } from "../api/dashboardApi";

function StatCard({ title, value, icon, gradient }) {
  return (
    <div className={`rounded-3xl bg-linear-to-br ${gradient} p-6 text-white shadow-xl`}>
      <div className="flex items-center justify-between">
        <p className="text-sm font-bold uppercase tracking-wide text-white/80">{title}</p>
        <span className="text-3xl">{icon}</span>
      </div>
      <h3 className="mt-3 text-3xl font-black">{value ?? 0}</h3>
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

function getCards(summary) {
  if (summary.role === "employee") {
    return [
      ["My Tasks", summary.total_tasks, "📋", "from-indigo-600 to-blue-500"],
      ["Completed", summary.done_tasks, "✅", "from-emerald-500 to-teal-500"],
      ["Pending Requests", summary.pending_requests, "⏳", "from-rose-500 to-orange-500"],
    ];
  }

  if (summary.role === "manager") {
    return [
      ["Team Tasks", summary.team_tasks, "👥", "from-indigo-600 to-blue-500"],
      ["Pending Approvals", summary.pending_approvals, "📝", "from-rose-500 to-orange-500"],
      ["On Hold", summary.on_hold_approvals, "⏸️", "from-amber-500 to-yellow-500"],
    ];
  }

  return [
    ["Total Users", summary.total_users, "👤", "from-indigo-600 to-blue-500"],
    ["Total Tasks", summary.total_tasks, "📋", "from-emerald-500 to-teal-500"],
    ["Admin Approvals", summary.pending_admin_approvals, "⚠️", "from-rose-500 to-orange-500"],
  ];
}


export default function DashboardPage() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchData() {
      try {
        const data = await getDashboardSummary();
        setSummary(data);
      } catch (err) {
        console.error(err);
        setError("Unable to load dashboard summary");
      }
    }

    fetchData();
  }, []);

  const total = summary?.total_tasks || summary?.team_tasks || 0;
  const cards = summary ? getCards(summary) : [];

  return (
    <div className="space-y-6">
      <div className="overflow-hidden rounded-4xl bg-gradient-to-r from-indigo-600 via-violet-600 to-sky-500 p-5 text-white shadow-2xl">
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-white/75">
          Dashboard
        </p>

        <h2 className="mt-3 text-3xl font-black md:text-2xl lg:text-3xl">
          Role-based enterprise overview
        </h2>

        <p className="mt-3 max-w-2xl text-white/80">
          Track tasks, requests, documents and system progress based on your role.
        </p>
      </div>

      {error && (
        <div className="rounded-2xl bg-rose-50 p-4 font-semibold text-rose-700">
          {error}
        </div>
      )}

      {!summary ? (
        <div className="rounded-2xl bg-white p-8 text-center font-bold text-slate-500 shadow">
          Loading dashboard...
        </div>
      ) : (
        <>
          <div className="grid gap-4 md:grid-cols-3">
            {cards.map(([title, value, icon, gradient]) => (
              <StatCard
                key={title}
                title={title}
                value={value}
                icon={icon}
                gradient={gradient}
              />
            ))}
          </div>

          <div className="grid gap-6 lg:grid-cols-3">
            <div className="rounded-2xl bg-white p-6 shadow-xl lg:col-span-2">
              <h3 className="text-xl font-black text-slate-900">
                Task Distribution
              </h3>

              <div className="mt-6 space-y-5">
                <DistributionBar
                  label="To Do"
                  value={summary.todo_tasks}
                  total={total}
                  color="bg-sky-500"
                />

                <DistributionBar
                  label="In Progress"
                  value={summary.in_progress_tasks}
                  total={total}
                  color="bg-indigo-500"
                />

                <DistributionBar
                  label="Review"
                  value={summary.review_tasks}
                  total={total}
                  color="bg-amber-500"
                />

                <DistributionBar
                  label="Done"
                  value={summary.done_tasks}
                  total={total}
                  color="bg-emerald-500"
                />
              </div>
            </div>

            <div className="rounded-xl bg-slate-950 p-6 text-white shadow-xl">
              <p className="text-sm font-bold uppercase tracking-widest text-indigo-300">
                AI Summary
              </p>
              <div className="mt-6 rounded-2xl bg-white/10 p-4 text-sm text-slate-200">
                Role:{" "}
                <span className="font-black uppercase text-white">
                  {summary.role}
                </span>
              </div>
              <h3 className="mt-4 text-2xl font-black">
                Focus Area
              </h3>

              <p className="mt-3 text-sm leading-6 text-slate-300">
                {summary.ai_summary}
              </p>
              </div>
          </div>
        </>
      )}
    </div>
  );
}
