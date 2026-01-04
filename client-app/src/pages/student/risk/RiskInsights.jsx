import { Line } from "react-chartjs-2";
import { useEffect, useState } from "react";
import api from "../../../api/axios";
import "./riskInsights.css";

export default function RiskInsights() {
  const [risk, setRisk] = useState(null);

  useEffect(() => {
    api.get("/insights/self")
      .then(res => setRisk(res.data))
      .catch(() => setRisk(null));
  }, []);

  if (!risk) {
    return <p style={{ padding: 24 }}>Loading risk insights...</p>;
  }

  const trendData = {
    labels: ["Jan", "Feb", "Mar", "Apr"],
    datasets: [
      {
        label: "Risk Score",
        data: risk.trend ?? [62, 61, 66, 77],
        borderColor: "#7c3aed",
        backgroundColor: "rgba(124,58,237,0.2)",
        tension: 0.4,
        fill: true,
        pointRadius: 4,
      },
    ],
  };

  return (
    <div className="risk-page">
      <div className="risk-header">
        <div>
          <h1>Risk Insights</h1>
          <p>Detailed analysis of student risk factors and trends.</p>
        </div>
        <span className="status">● System Online</span>
      </div>

      <div className="risk-grid">
        {/* Risk Trend */}
        <div className="card large">
          <h3>Risk Trend</h3>
          <Line
            data={trendData}
            options={{ maintainAspectRatio: false }}
          />
        </div>

        {/* Risk Breakdown */}
        <div className="card">
          <h3>Risk Breakdown</h3>

          <div className="bar-row">
            <span>Academic</span><span>{risk.academic}%</span>
            <div className="bar blue" style={{ width: `${risk.academic}%` }} />
          </div>

          <div className="bar-row">
            <span>Attendance</span><span>{risk.attendance}%</span>
            <div className="bar green" style={{ width: `${risk.attendance}%` }} />
          </div>

          <div className="bar-row">
            <span>Behavior</span><span>{risk.behavior}%</span>
            <div className="bar purple" style={{ width: `${risk.behavior}%` }} />
          </div>
        </div>

        {/* Attention Needed */}
        <div className="card highlight">
          <h3>Attention Needed</h3>
          <p>Academic risk has increased by 5% this month.</p>
          <button>Review Now</button>
        </div>

        {/* Pending Review */}
        <div className="card">
          <h3>Pending Review</h3>
          <p>2 incidents unclassified</p>
        </div>
      </div>
    </div>
  );
}
