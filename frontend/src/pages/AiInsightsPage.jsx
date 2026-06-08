import { useEffect, useState } from "react";
import { getTaskInsights, getRecommendedAssignee } from "../api/aiApi";

export default function AiInsightsPage() {
  const [insights, setInsights] = useState([]);
  const [recommended, setRecommended] = useState(null);

  useEffect(() => {
    async function loadAiData() {
      const taskData = await getTaskInsights();
      const assigneeData = await getRecommendedAssignee();

      setInsights(taskData.insights || []);
      setRecommended(assigneeData.recommended_user);
    }

    loadAiData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="rounded-2xl bg-gradient-to-r from-indigo-600 to-fuchsia-600 p-5 text-white shadow-xl">
        <p className="text-sm font-bold uppercase tracking-widest">
          AI Insights
        </p>
        <h1 className="mt-3 text-3xl font-black">
          Intelligent Task Analysis
        </h1>
        <p className="mt-2 text-white/80">
          Detect delay risks and recommend smart task assignment.
        </p>
      </div>

      {recommended && (
        <div className="rounded-2xl bg-white p-6 shadow-xl">
          <h2 className="text-xl font-black text-slate-900">
            Smart Task Assignment Recommendation
          </h2>

          <p className="mt-3 text-slate-700">
            Recommended Assignee:
            <span className="ml-2 font-black">
              {recommended.name}
            </span>
          </p>

          <div className="mt-4 grid gap-4 md:grid-cols-4">
            <div>Pending: {recommended.pending_tasks}</div>
            <div>Completed: {recommended.completed_tasks}</div>
            <div>Overdue: {recommended.overdue_tasks}</div>
            <div>Score: {recommended.assignment_score}</div>
          </div>
        </div>
      )}

      <div className="rounded-2xl bg-white p-6 shadow-xl">
        <h2 className="text-xl font-black text-slate-900">
          High Priority / Delay Risk Tasks
        </h2>

        <div className="mt-5 space-y-4">
          {insights.length === 0 ? (
            <p className="text-slate-500">
              No risky tasks detected.
            </p>
          ) : (
            insights.map((item) => (
              <div
                key={item.task_id}
                className="rounded-2xl border border-slate-200 p-4"
              >
                <div className="flex justify-between">
                  <h3 className="font-black">{item.title}</h3>
                  <span className="rounded-full bg-rose-100 px-3 py-1 text-xs font-bold text-rose-700">
                    {item.risk_level}
                  </span>
                </div>

                <p className="mt-2 text-sm text-slate-500">
                  Risk Score: {item.risk_score}
                </p>

                <ul className="mt-2 list-disc pl-5 text-sm text-slate-600">
                  {item.reasons.map((reason, index) => (
                    <li key={index}>{reason}</li>
                  ))}
                </ul>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
