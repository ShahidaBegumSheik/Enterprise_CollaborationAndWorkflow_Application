import { useEffect, useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import KanbanBoard from "../components/tasks/KanbanBoard";
import { getTasks, updateTask } from "../api/taskApi";

export default function KanbanPage() {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchTasks() {
      try {
        const data = await getTasks();
        setTasks(data);
      } catch (err) {
        console.error(err);
        setError("Unable to laod Kanban tasks")
      }
    }
    fetchTasks();
  }, []);

  async function loadTasks() {
    try {
      const data = await getTasks();
      setTasks(data);
    } catch (err) {
      console.error(err);
      setError("Unable to load Kanban tasks");
    }
  }

  async function handleMoveTask(taskId, status) {
    const id = Number(taskId);

    const oldTasks = tasks;

    setTasks((prev) =>
      prev.map((task) =>
        task.id === id ? { ...task, status } : task
      )
    );

    try {
      await updateTask(id, { status });
      await loadTasks();
    } catch (err) {
      console.error(err);
      setError("Unable to update task status");
      setTasks(oldTasks);
    }
  }


  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="flex flex-col justify-between gap-4 rounded-4xl bg-white p-6 shadow-xl md:flex-row md:items-center">
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.25em] text-indigo-600">Kanban Board</p>
            <h2 className="mt-2 text-3xl font-black text-slate-900">Drag tasks across workflow stages</h2>
          </div>
          <div className="rounded-2xl bg-indigo-50 px-4 py-3 text-sm font-bold text-indigo-700">Drag and drop to update status</div>
        </div>
        {error && <div className="rounded-2xl bg-rose-50 p-4 font-semibold text-rose-700">{error}</div>}
        <KanbanBoard tasks={tasks} onMoveTask={handleMoveTask} />
      </div>
    </AppLayout>
  );
}
