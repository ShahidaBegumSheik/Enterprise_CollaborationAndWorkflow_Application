import { NavLink } from "react-router-dom";
import useAuth from "../../hooks/useAuth";

const links = [
  { to: "/dashboard", label: "Dashboard", icon: "📊" },
  { to: "/tasks", label: "Tasks", icon: "✅" },
  { to: "/kanban", label: "Kanban", icon: "🧩" },
  { to: "/approvals", label: "Approvals", icon: "🔄" },
  { to: "/documents", label: "Documents", icon: "📁" },
  { to: "/admin/users", label: "Admin", icon: "⚙️", adminOnly: true },
];

export default function Sidebar() {
  const { user } = useAuth();
  const visibleLinks = links.filter((link) => !link.adminOnly || user?.role === "admin");

  return (
    <aside className="hidden min-h-screen w-72 shrink-0 bg-linear-to-b from-indigo-950 via-slate-950 to-slate-900 p-5 text-white shadow-2xl lg:block">
      <div className="mb-8 rounded-3xl bg-white/10 p-4 backdrop-blur">
        <div className="text-2x font-medium text-indigo-200">Mini</div>
        <h2 className="text-2xl font-black tracking-tight">Enterprise Collaboration and Workflow App</h2>
        <p className="mt-2 text-lg text-slate-300">Collaboration & Workflow System</p>
      </div>

      <nav className="space-y-2">
        {visibleLinks.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-semibold transition ${
                isActive
                  ? "bg-white text-indigo-950 shadow-lg shadow-indigo-950/20"
                  : "text-slate-200 hover:bg-white/10 hover:text-white"
              }`
            }
          >
            <span>{link.icon}</span>
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
