import { createContext, useEffect, useMemo, useState } from "react";
import { loginUser } from "../authApi";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("enterprise_access_token") || null);
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("enterprise_user");
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    if (token) localStorage.setItem("enterprise_access_token", token);
    else localStorage.removeItem("enterprise_access_token");
  }, [token]);

  useEffect(() => {
    if (user) localStorage.setItem("enterprise_user", JSON.stringify(user));
    else localStorage.removeItem("enterprise_user");
  }, [user]);

  const login = async (email, password) => {
    const data = await loginUser({ email, password });
    setToken(data.access_token);
    setUser(data.user || null);
    return data;
  };

  const logout = () => {
    setToken(null);
    setUser(null);
  };

  const value = useMemo(() => ({ user, token, login, logout, isAuthenticated: Boolean(token) }), [user, token]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
