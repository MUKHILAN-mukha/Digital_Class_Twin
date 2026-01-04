import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { useAuth } from "../auth/AuthContext";
import { Mail, Lock, Eye } from "lucide-react"; // Icons B

import "./login.css"; // CSS A

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const res = await api.post("/auth/login", { email, password });
      login(res.data);
      navigate("/", { replace: true });
    } catch {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">

        <div className="login-logo">
          <div className="logo-icon">◎</div>
        </div>

        <h1 className="login-title">Welcome Back</h1>
        <p className="login-subtitle">
          Sign in to access your digital twin dashboard
        </p>

        <form onSubmit={handleSubmit} className="login-form">

          {error && <div className="login-error">{error}</div>}

          <div className="input-group">
            <Mail size={18} />
            <input
              type="email"
              placeholder="Email Address"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <Lock size={18} />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
            <Eye size={16} className="eye-icon" />
          </div>

          <button type="submit" className="login-button">
            Sign In →
          </button>
        </form>

        <p className="login-footer">
          Protected by Digital Twin Security Systems
        </p>
      </div>
    </div>
  );
}
