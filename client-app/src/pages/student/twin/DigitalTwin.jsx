import { Line } from "react-chartjs-2";
import { useEffect, useState } from "react";
import api from "../../../api/axios";
import "./digitalTwin.css";

export default function DigitalTwin() {
  const [twin, setTwin] = useState(null);

  useEffect(() => {
    api.get("/twins/self").then(res => setTwin(res.data));
  }, []);

  if (!twin) return <p>Loading Digital Twin...</p>;

  const chartData = {
    labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
    datasets: [
      {
        label: "Attendance",
        data: [92, 90, 94, 93],
        borderColor: "#34D399",
        backgroundColor: "rgba(52,211,153,0.15)",
        fill: true,
        tension: 0.4
      },
      {
        label: "Academic",
        data: [70, 72, 75, 78],
        borderColor: "#6C63FF",
        backgroundColor: "rgba(108,99,255,0.15)",
        fill: true,
        tension: 0.4
      },
      {
        label: "Behavior",
        data: [85, 80, 82, 88],
        borderColor: "#F59E0B",
        backgroundColor: "rgba(245,158,11,0.15)",
        fill: true,
        tension: 0.4
      }
    ]
  };

  return (
    <div className="twin-page">
      {/* HEADER */}
      <div className="twin-header">
        <div>
          <h1>Timeline Overview ✨</h1>
          <p>Track your academic journey and performance trends.</p>
        </div>
        <span className="status-pill">System Online</span>
      </div>

      {/* METRIC CARDS */}
      <section className="twin-metrics">
        <div className="metric-card">
          <p>Attendance Rate</p>
          <h2>96%</h2>
          <span className="metric-positive">+2.4%</span>
        </div>

        <div className="metric-card">
          <p>Academic Score</p>
          <h2>78 / 100</h2>
          <span className="metric-neutral">Stable</span>
        </div>

        <div className="metric-card warning">
          <p>Behavior Index</p>
          <h2>88 / 100</h2>
          <span className="metric-warning">High</span>
        </div>
      </section>

      {/* CHART */}
      <section className="twin-chart-card">
        <div className="chart-title">
          <h3>Performance Trends</h3>
          <div className="chart-legend">
            <span className="dot green">Attendance</span>
            <span className="dot blue">Academic</span>
            <span className="dot orange">Behavior</span>
          </div>
        </div>

        <div className="chart-wrapper">
          <Line
            data={chartData}
            options={{
              maintainAspectRatio: false,
              plugins: { legend: { display: false } }
            }}
          />
        </div>
      </section>
    </div>
  );
}
