export default function TaskCard({ task }) {
    const priorityClasses = {
        low: "bg-green-100 text-green-700",
        medium: "bg-yellow-100 text-yellow-700",
        high: "bg-red-100 text-red-700",
    };

    return (
        <div className="rounded-xl bg-white p-4 shadow-sm border">
            <div className="flex items-start justify-between gap-2">
                <h3 className="font-semibold text-slate-800">{task.title}</h3>
                <span className={`rounded-full px-2 py-1 text-xs font-medium ${priorityClasses[task.priority] || priorityClasses.medium}`}>
                    {task.priority}
                </span>
            </div>
            <p className="mt-2 text-sm text-slate-600">{task.description}</p>
            <div className="mt-3 text-xs text-slate-500">Status: {task.status}</div>
        </div>
    );
}

