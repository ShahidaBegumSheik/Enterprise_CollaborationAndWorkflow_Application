import { NavLink } from "react-router-dom";
import useAuth from "../../hooks/useAuth";
import { Brain, CheckSquare, ClipboardList, CreditCard, Folder, Kanban, LayoutDashboard, Settings } from "lucide-react";

const links = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/tasks", label: "Tasks", icon: CheckSquare },
  { to: "/kanban", label: "Kanban", icon: Kanban },
  { to: "/approvals", label: "Approvals", icon: ClipboardList },
  { to: "/documents", label: "Documents", icon: Folder },
  { to: "/ai-insights", label: "AI Insights", icon: Brain, adminOnly: true},
  { to: "/admin/users", label: "Admin", icon: Settings, adminOnly: true },
  { to: "/billing", label: "Billing", icon: CreditCard, adminOnly: true}
];

export default function Sidebar() {
  const { user } = useAuth();
  const visibleLinks = links.filter((link) => {
    if (link.adminOnly && user?.role !== "admin") {
      return false;
    }
    return true;
  });     

  return (
    <aside className="h-screen w-56 shrink-0 overflow-y-auto bg-gradient-to-b from-indigo-950 via-slate-950 to-slate-900 p-3 text-white shadow-2xl lg:w-60">
      <div className="mb-8 rounded-2xl bg-white/10 p-3 backdrop-blur">
        <div className="text-2x font-medium text-indigo-200">Mini</div>
        <h2 className="text-lg font-black leading-tight tracking-tight">Enterprise Collaboration and Workflow App</h2>
        <p className="mt-1 text-sm text-slate-300">Collaboration & Workflow System</p>
      </div>

      <nav className="space-y-2">
        {visibleLinks.map((link) => {
          const Icon = link.icon;

          return (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `flex items-center gap-2 rounded-xl px-3 py-2 text-xs font-semibold transition ${
                  isActive
                    ? "bg-white text-indigo-950 shadow"
                    : "text-slate-300 hover:bg-white/10 hover:text-white"
                }`
              }
            >
              {typeof Icon === "string" ? (
                <span>{Icon}</span>
              ) : (
                <Icon size={18} />
              )}

              <span>{link.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}
