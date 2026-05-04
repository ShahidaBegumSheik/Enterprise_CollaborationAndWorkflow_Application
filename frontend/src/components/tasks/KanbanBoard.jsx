const columns = [
  { key: "todo", title: "To Do", accent: "border-sky-400", badge: "bg-sky-100 text-sky-700" },
  { key: "in_progress", title: "In Progress", accent: "border-indigo-400", badge: "bg-indigo-100 text-indigo-700" },
  { key: "review", title: "Review", accent: "border-amber-400", badge: "bg-amber-100 text-amber-700" },
  { key: "done", title: "Done", accent: "border-emerald-400", badge: "bg-emerald-100 text-emerald-700" },
];

const priorityClasses = {
  low: "bg-emerald-100 text-emerald-700 ring-emerald-200",
  medium: "bg-amber-100 text-amber-700 ring-amber-200",
  high: "bg-rose-100 text-rose-700 ring-rose-200",
};

export default function KanbanBoard({ tasks, onMoveTask }) {
  return (
    <div className="grid gap-4 xl:grid-cols-4">
      {columns.map((column) => {
        const columnTasks = tasks.filter((task) => task.status === column.key);
        return (
          <div
            key={column.key}
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              const taskId = e.dataTransfer.getData("taskId");
              if (taskId) onMoveTask(taskId, column.key);
            }}
            className={`min-h-120 rounded-3xl border-t-4 ${column.accent} bg-white/80 p-4 shadow-xl backdrop-blur`}
          >
            <div className="mb-4 flex items-center justify-between">
              <h3 className="font-black text-slate-800">{column.title}</h3>
              <span className={`rounded-full px-3 py-1 text-xs font-black ${column.badge}`}>{columnTasks.length}</span>
            </div>

            <div className="space-y-3">
              {columnTasks.map((task) => (
                <div
                  key={task.id}
                  draggable
                  onDragStart={(e) => e.dataTransfer.setData("taskId", String(task.id))}
                  className="cursor-grab rounded-2xl border border-slate-100 bg-white p-4 shadow-md transition hover:-translate-y-1 hover:shadow-xl active:cursor-grabbing"
                >
                  <div className="flex items-start justify-between gap-3">
                    <h4 className="font-black text-slate-900">{task.title}</h4>
                    <span className={`rounded-full px-2 py-1 text-[10px] font-black uppercase ring-1 ${priorityClasses[task.priority] || priorityClasses.medium}`}>
                      {task.priority}
                    </span>
                  </div>
                  <p className="mt-2 line-clamp-3 text-sm leading-6 text-slate-500">{task.description || "No description added."}</p>
                  {task.due_date && <p className="mt-3 text-xs font-bold text-slate-400">Due: {new Date(task.due_date).toLocaleDateString()}</p>}
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}
