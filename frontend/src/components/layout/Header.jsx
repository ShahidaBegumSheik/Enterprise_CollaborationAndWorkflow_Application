import useAuth from "../../hooks/useAuth";
import NotificationBell from "../common/NotificationBell";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-10 border-b border-slate-200/80 bg-white/90 px-4 py-3 shadow-sm backdrop-blur">
      <div className="flex items-center justify-between gap-3">
        <div className="min-w-0">
          <div>
            <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-indigo-600">Enterprise Workspace</p>
            <h1 className="truncate text-base font-black text-slate-900 lg:text-xl">Mini Enterprise Collaboration And Workflow App</h1>
          </div>
        </div>
        <div className="flex shrink-0 items-center gap-2">
          <NotificationBell />
          <div className="hidden rounded-xl bg-indigo-50 px-3 py-1.5 text-right md:block">
            <p className="max-w-40 truncate text-xs font-bold text-slate-900">{user?.email || "User"}</p>
            <p className="text-[10px] font-semibold capitalize text-indigo-700">{user?.role || "logged in"}</p>
          </div>
          <button onClick={logout} className="rounded-xl bg-rose-500 px-3 py-1.5 text-xs font-bold text-white shadow hover:bg-rose-600">
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}
