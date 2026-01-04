import "./profile.css";

export default function Profile({ user }) {
  return (
    <div className="profile-page">
      <header className="profile-header">
        <div>
          <h1>Profile</h1>
          <p>Manage your account details and preferences.</p>
        </div>

        <div className="user-pill">
          <span>{user?.email}</span>
          <div className="avatar">S</div>
        </div>
      </header>

      <div className="profile-banner">
        <div className="avatar-lg">👤</div>
        <div>
          <h2>{user?.name || "Student User"}</h2>
          <p>Computer Science Department</p>
        </div>
        <button className="primary">Edit Profile</button>
      </div>

      <div className="info-grid">
        <div className="info-card">
          <strong>User ID (UUID)</strong>
          <p>{user?.id}</p>
        </div>

        <div className="info-card">
          <strong>Assigned Role</strong>
          <span className="status active">Student</span>
        </div>
      </div>

      <div className="panel-grid">
        <div className="panel">
          <h3>Personal Information</h3>

          <label>Full Name</label>
          <input value={user?.name || ""} disabled />

          <label>Email</label>
          <input value={user?.email || ""} disabled />

          <label>Phone</label>
          <input value="+1 (555) 123-4567" disabled />

          <label>Location</label>
          <input value="Campus Dorm A, Room 101" disabled />
        </div>

        <div className="panel">
          <h3>Account Security</h3>

          <div className="security-item">Password →</div>
          <div className="security-item">Sessions (2 devices)</div>

          <p className="login-log">
            Recent Login: Today, 09:41 AM (IP: 192.168.1.1)
          </p>
        </div>
      </div>

      <div className="privacy">
        Your profile information is securely stored and used only for Digital Twin
        verification purposes.
      </div>
    </div>
  );
}
