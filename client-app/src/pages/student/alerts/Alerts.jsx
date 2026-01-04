import "./alerts.css";

export default function Alerts({ alerts = [] }) {
  return (
    <div className="alerts-page">
      <header className="alerts-header">
        <div>
          <h1>Alerts</h1>
          <p>Stay updated with critical system notifications and academic alerts.</p>
        </div>

        <div className="actions">
          <button className="ghost">Filter</button>
          <button className="ghost">Mark all read</button>
        </div>
      </header>

      <div className="system-banner">
        <span className="dot green" />
        <div>
          <strong>System Online</strong>
          <p>All monitoring services are active.</p>
        </div>
        <span className="sync">Last sync: Just now</span>
      </div>

      <div className="tabs">
        <span className="active">All Alerts (3)</span>
        <span>Academic Risk</span>
        <span>Behavioral</span>
        <span>System</span>
      </div>

      <div className="alert critical">
        <span className="badge">CRITICAL</span>
        <h2>Attention Needed: Grade Drop Detected</h2>
        <p>
          Academic performance in Mathematics has decreased by 15% over the last month.
          This triggers an automated intervention suggestion.
        </p>

        <div className="buttons">
          <button className="primary">Review Report →</button>
          <button className="secondary">Dismiss</button>
        </div>
      </div>

      <div className="alert-grid">
        <div className="alert-card">
          <strong>Attendance Warning</strong>
          <span>Yesterday, 2:30 PM</span>
          <p>Late arrival recorded for Physics Class. 2nd instance this week.</p>
          <a>View Details →</a>
        </div>

        <div className="alert-card">
          <strong>Assignment Due Soon</strong>
          <span>Today, 9:00 AM</span>
          <p>“History of AI” essay submission deadline in 24 hours.</p>
          <a>Go to Canvas ↗</a>
        </div>
      </div>
    </div>
  );
}
