import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import StudentRoutes from "./pages/student/StudentRoutes";
import "./utils/chartSetup";

import { useAuth } from "./auth/AuthContext";

export default function App() {
  const { loading } = useAuth();
  if (loading) return null;

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/*" element={<StudentRoutes />} />
    </Routes>
  );
}
