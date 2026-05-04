import useAuth from "../../hooks/useAuth";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-10 border-b border-slate-200/80 bg-white/85 px-6 py-4 shadow-sm backdrop-blur">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.25em] text-indigo-600">Enterprise Workspace</p>
          <h1 className="text-xl font-black text-slate-900 md:text-2xl">Mini Enterprise Collaboration And Workflow App</h1>
        </div>
        <div className="flex items-center gap-3">
          <div className="hidden rounded-2xl bg-indigo-50 px-4 py-2 text-right md:block">
            <p className="text-sm font-bold text-slate-900">{user?.email || "User"}</p>
            <p className="text-xs font-semibold capitalize text-indigo-700">{user?.role || "logged in"}</p>
          </div>
          <button onClick={logout} className="rounded-2xl bg-rose-500 px-4 py-2 text-sm font-bold text-white shadow-lg shadow-rose-500/25 transition hover:bg-rose-600">
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}
