import { Line, Doughnut } from "react-chartjs-2";
import api from "../../../api/axios";
import { useEffect, useState } from "react";
import "./dashboard.css";

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.get("/dashboard/student").then(res => setData(res.data));
  }, []);

  if (!data) return <p>Loading...</p>;

  const attendanceTrend = {
    labels: ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb"],
    datasets: [
      {
        label: "Attendance %",
        data: [98, 95, 92, 96, 88, 94],
        borderColor: "#6C63FF",
        backgroundColor: "rgba(108,99,255,0.15)",
        tension: 0.4,
        fill: true,
        pointRadius: 4,
        pointBackgroundColor: "#6C63FF"
      }
    ]
  };

  const riskBreakdown = {
    labels: ["Academic", "Behavioral", "Attendance"],
    datasets: [
      {
        data: [45, 35, 20],
        backgroundColor: ["#6C63FF", "#A855F7", "#34D399"],
        borderWidth: 0
      }
    ]
  };

  return (
    <div className="dashboard-page">
      {/* HEADER */}
      <div className="dashboard-header">
        <div>
          <h1>Welcome back</h1>
          <p>Here’s what’s happening with your digital twin today.</p>
        </div>
        <span className="status-pill">System Online</span>
      </div>

      {/* KPI CARDS */}
      <section className="kpi-grid">
        <div className="kpi-card gradient">
          <p>GPA Projection</p>
          <h2>3.8</h2>
          <span className="kpi-badge">+2.4%</span>
        </div>

        <div className="kpi-card">
          <p>Attendance</p>
          <h2>96%</h2>
        </div>

        <div className="kpi-card">
          <p>Academic Score</p>
          <h2>78 / 100</h2>
        </div>

        <div className="kpi-card warning">
          <p>Risk Level</p>
          <h2>Medium</h2>
        </div>
      </section>

      {/* CHARTS */}
      <section className="chart-grid">
        <div className="chart-card">
          <div className="chart-title">
            <h3>Attendance Trend</h3>
            <span>Last 6 Months</span>
          </div>
          <div className="chart-wrapper">
            <Line
              data={attendanceTrend}
              options={{
                maintainAspectRatio: false,
                plugins: { legend: { display: false } }
              }}
            />
          </div>
        </div>

        <div className="chart-card">
          <div className="chart-title">
            <h3>Risk Breakdown</h3>
            <span>Current Assessment</span>
          </div>
          <div className="chart-wrapper">
            <Doughnut
              data={riskBreakdown}
              options={{
                maintainAspectRatio: false,
                cutout: "70%",
                plugins: { legend: { position: "bottom" } }
              }}
            />
          </div>
        </div>
      </section>
    </div>
  );
}
