import { useEffect, useState } from "react";
import AppLayout from "../components/layout/AppLayout";
import { createTask, deleteTask, getTasks, updateTask } from "../api/taskApi";
import { getAllUsers } from "../api/adminApi"

const emptyForm = {
  title: "",
  description: "",
  priority: "medium",
  status: "todo",
  due_date: "",
  assignee_id: "",
};

const statusOptions = ["todo", "in_progress", "review", "done"];

function priorityBadge(priority) {
  if (priority === "high") return "bg-rose-100 text-rose-700";
  if (priority === "low") return "bg-emerald-100 text-emerald-700";
  return "bg-amber-100 text-amber-700";
}

export default function TasksPage() {
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([])
  const [form, setForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const currentUser = JSON.parse(localStorage.getItem("enterprise_user") || "{}");

  const assignableUsers = users.filter((user) => {
    const currentRole = String(currentUser.role || "").toLowerCase();
    const userRole = String(user.role || "").toLowerCase();

    if (currentRole === "admin") {
      return ["admin", "manager", "employee"].includes(userRole);
    }

    if (currentRole === "manager") {
      return ["manager", "employee"].includes(userRole);
    }

    if (currentRole === "employee") {
      return (
        user.role === "employee" && 
        Number(user.id) !== Number(currentUser.id)
      );
    }

    return false;
  });

  useEffect(() => {
    loadTasks();
    loadUsers();
  }, []);

  async function loadTasks() {
    try {
      const data = await getTasks();
      setTasks(data);
    } catch (err) {
      console.error(err);
      setError("Unable to load tasks");
    }
  }

  async function loadUsers() {
    try {
      const data = await getAllUsers();
      //setUsers(data.filter((user) => user.role === "employee"));
      setUsers(data);
    } catch (err) {
      console.error(err);
      setError("Unable to load users for assignee dropdown");
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    const payload = {
      title: form.title,
      description: form.description,
      priority: form.priority,
      status: form.status,
      due_date: form.due_date ? new Date(form.due_date).toISOString() : null,
      assignee_id: form.assignee_id ? Number(form.assignee_id) : null,
    };

    try {
      await createTask(payload);
      setForm(emptyForm);
      loadTasks();
    } catch (err) {
      console.error(err);
      setError("Task creation failed. Admin/Manager role may be required by backend rules.");
    } finally {
      setLoading(false);
    }
  }

  async function handleStatusChange(taskId, status) {
    await updateTask(taskId, { status });
    loadTasks();
  }

  async function handleDelete(taskId) {
    await deleteTask(taskId);
    loadTasks();
  }

  return (
    <AppLayout>
      <div className="space-y-6">
        <div className="rounded-4xl bg-linear-to-r from-slate-950 to-indigo-900 p-8 text-white shadow-2xl">
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-indigo-200">Task Management</p>
          <h2 className="mt-3 text-3xl font-black">Create, assign, track and complete tasks</h2>
        </div>

        {error && <div className="rounded-2xl bg-rose-50 p-4 font-semibold text-rose-700">{error}</div>}

        <form onSubmit={handleSubmit} className="rounded-3xl bg-white p-6 shadow-xl">
          <h3 className="mb-5 text-xl font-black text-slate-900">Create Task</h3>
          <div className="grid gap-4 md:grid-cols-2">
            <input className="rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-indigo-500 focus:ring-2" placeholder="Task title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
            <input type="datetime-local" className="rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-indigo-500 focus:ring-2" value={form.due_date} onChange={(e) => setForm({ ...form, due_date: e.target.value })} />
            <select className="rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-indigo-500 focus:ring-2" value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>
              <option value="low">Low Priority</option>
              <option value="medium">Medium Priority</option>
              <option value="high">High Priority</option>
            </select>
            <select
              className="rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-indigo-500 focus:ring-2"
              value={form.assignee_id} 
              onChange={(e) => 
                setForm({ 
                  ...form, 
                  assignee_id: e.target.value,
                })
              } >
                <option value="">Select Assigness</option>
                {assignableUsers.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.full_name} ({user.email})
                  </option>
                ))}
            </select>
            <textarea className="md:col-span-2 rounded-2xl border border-slate-200 bg-slate-50 p-3 outline-none ring-indigo-500 focus:ring-2" placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          </div>
          <button disabled={loading} className="mt-5 rounded-2xl bg-indigo-600 px-6 py-3 font-black text-white shadow-lg shadow-indigo-600/25 hover:bg-indigo-700 disabled:opacity-60">
            {loading ? "Creating..." : "Create Task"}
          </button>
        </form>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {tasks.map((task) => (
            <div key={task.id} className="rounded-3xl bg-white p-5 shadow-xl transition hover:-translate-y-1 hover:shadow-2xl">
              <div className="flex items-start justify-between gap-4">
                <h3 className="text-lg font-black text-slate-900">{task.title}</h3>
                <span className={`rounded-full px-3 py-1 text-xs font-black uppercase ${priorityBadge(task.priority)}`}>{task.priority}</span>
              </div>
              <p className="mt-3 min-h-12 text-sm leading-6 text-slate-500">{task.description || "No description"}</p>
              <div className="mt-4 grid grid-cols-2 gap-3 text-xs font-bold text-slate-500">
                <div className="rounded-2xl bg-slate-50 p-3">Status<br /><span className="text-slate-900">{task.status}</span></div>
                <div className="rounded-2xl bg-slate-50 p-3">Assignee<br /><span className="text-slate-900">{task.assignee_name || "Unassigned"}</span></div>
              </div>
              <div className="mt-4 flex gap-2">
                <select value={task.status} onChange={(e) => handleStatusChange(task.id, e.target.value)} className="flex-1 rounded-2xl border border-slate-200 p-2 text-sm font-bold">
                  {statusOptions.map((status) => <option key={status} value={status}>{status}</option>)}
                </select>
                <button onClick={() => handleDelete(task.id)} className="rounded-2xl bg-rose-50 px-4 py-2 text-sm font-black text-rose-700 hover:bg-rose-100">Delete</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </AppLayout>
  );
}
