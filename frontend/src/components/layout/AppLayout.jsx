import Sidebar from "./Sidebar";
import Header from "./Header";

export default function AppLayout({children}) {
    return (
        <div className="flex min-h-screen bg-slate-100">
            <Sidebar />
            <div className="flex-1">
                <Header />
                <main className="p-6">{children}</main>
            </div>
        </div>
    )
}
