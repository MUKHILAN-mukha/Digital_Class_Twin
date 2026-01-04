import api from "./axios";

export const fetchDashboard = () => api.get("/dashboard/student");
export const fetchTwin = () => api.get("/twins/self");
export const fetchRisk = () => api.get("/insights/self");
export const fetchAlerts = () => api.get("/alerts/self");
export const submitEvent = (data) => api.post("/events/", data);
export const fetchProfile = () => api.get("/profile/me");
