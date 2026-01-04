import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";
import api from "../../api/axios";
import { useEffect, useState } from "react";
import "./studentSidebar.css";

export default function StudentSidebar() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [alertCount, setAlertCount] = useState(0);

  useEffect(() => {
    api.get("/alerts/self")
      .then(res => setAlertCount(res.data?.length || 0))
      .catch(() => setAlertCount(0));
  }, []);

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <aside className="sidebar">
      <div className="nav-group">
        <NavLink end to="" className="nav-link">Dashboard</NavLink>
        <NavLink to="twin" className="nav-link">Digital Twin</NavLink>
        <NavLink to="risk" className="nav-link">Risk Insights</NavLink>

        <NavLink to="alerts" className="nav-link">
          Alerts
          {alertCount > 0 && <span className="badge">{alertCount}</span>}
        </NavLink>

        <NavLink to="events" className="nav-link">Submit Event</NavLink>
        <NavLink to="profile" className="nav-link">Profile</NavLink>
      </div>

      <button className="logout" onClick={handleLogout}>
        Logout
      </button>
    </aside>
  );
}
