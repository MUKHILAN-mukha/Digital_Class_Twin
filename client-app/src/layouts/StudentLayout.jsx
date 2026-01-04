import { Outlet } from "react-router-dom";
import StudentSidebar from "../components/sidebar/StudentSidebar";

export default function StudentLayout() {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <StudentSidebar />
      <main style={{ flex: 1, padding: 24 }}>
        <Outlet />
      </main>
    </div>
  );
}
