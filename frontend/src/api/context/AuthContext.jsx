import { createContext, useEffect, useMemo, useState } from "react";
import { loginUser } from "../authApi";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem("enterprise_access_token") || null);
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("enterprise_user");
    return saved ? JSON.parse(saved) : null;
  });

  const login = async (email, password) => {
    const data = await loginUser({ email, password });

    localStorage.setItem("enterprise_access_token", data.access_token);

    if(data.refresh_token) {
      localStorage.setItem("enterprise_refresh_token", data.refresh_token);
    }

    if(data.user) {
      localStorage.setItem("enterprise_user", JSON.stringify(data.user));
    }

    setToken(data.access_token);
    setUser(data.user || null);
    return data;
  };

  const logout = () => {
    localStorage.removeItem("enterprise_access_token");
    localStorage.removeItem("enterprise_refresh_token");
    localStorage.removeItem("enterprise_user");

    setToken(null);
    setUser(null);
  };

  const value = useMemo(
    () => ({
      user,
      token,
      login,
      logout,
      isAuthenticated: Boolean(token),
    }),
    [user, token]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}