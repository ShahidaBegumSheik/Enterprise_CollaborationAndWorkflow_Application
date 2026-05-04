import Router from "./app/router";
import { AuthProvider } from "./api/context/AuthContext";
import "./index.css";

export default function App() {
  return (
    <AuthProvider>
      <div className="min-h-screen bg-slate-100 text-slate-800">
        <Router />
      </div>
    </AuthProvider>
  );
}