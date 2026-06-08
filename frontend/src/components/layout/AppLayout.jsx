import Sidebar from "./Sidebar";
import Header from "./Header";
import NotificationBell from "../common/NotificationBell";

export default function AppLayout({children}) {
    return (
        <div className="flex h-screen overflow-hidden bg-slate-50">
            <Sidebar />
            <div className="flex min-w-0 flex-1 flex-col overflow-hidden">
                <Header />
                <main className="min-w-0 flex-1 overflow-y-auto p-3 sm:p-4 lg:p-5">{children}</main>
            </div>
        </div>
    )
}
