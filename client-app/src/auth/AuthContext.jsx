import { createContext, useContext, useEffect, useState } from "react";
import {jwtDecode} from "jwt-decode";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (token) {
      try {
        const decoded = jwtDecode(token);
        setUser({
          user_id: decoded.sub,
          role: decoded.role,
          email: decoded.email,
        });
      } catch {
        localStorage.removeItem("token");
        setUser(null);
      }
    }

    setLoading(false); // 🔥 only AFTER hydration
  }, []);

  const login = (data) => {
    localStorage.setItem("token", data.access_token);
    const decoded = jwtDecode(data.access_token);
    setUser({
      user_id: decoded.sub,
      role: decoded.role,
      email: decoded.email,
    });
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
