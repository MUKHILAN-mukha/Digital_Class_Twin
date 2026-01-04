import "./submitEvent.css";

export default function SubmitEvent() {
  return (
    <div className="submit-page">
      <h1>Submit Event</h1>
      <p>Log a new academic or system event manually into the Digital Twin.</p>

      <div className="form-card">
        <label>Event Type</label>
        <select>
          <option>Select an event type...</option>
          <option>Academic</option>
          <option>Attendance</option>
          <option>Behavior</option>
        </select>

        <label>Value / Description</label>
        <textarea placeholder="Enter details associated with the event..." />

        <label className="checkbox">
          <input type="checkbox" /> Mark as critical priority
        </label>

        <div className="actions">
          <button className="ghost">Cancel</button>
          <button className="primary">Submit Event →</button>
        </div>
      </div>

      <div className="help-box">
        <strong>Need Help?</strong>
        <p>
          Events submitted here are processed immediately by the Digital Twin engine.
          Ensure accuracy to prevent skewed risk insights.
        </p>
      </div>
    </div>
  );
}
