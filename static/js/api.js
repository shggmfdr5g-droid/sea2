const API_BASE = "";

export async function queryVoyages(origin, destination, vessel) {
  const res = await fetch(`${API_BASE}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ origin, destination, vessel }),
  });
  return res.json();
}

export async function getMonitors() {
  const res = await fetch(`${API_BASE}/api/monitors`);
  return res.json();
}

export async function addMonitor(origin, destination) {
  const res = await fetch(`${API_BASE}/api/monitors`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ origin, destination }),
  });
  return res.json();
}

export async function deleteMonitor(id) {
  const res = await fetch(`${API_BASE}/api/monitors/${id}`, { method: "DELETE" });
  return res.json();
}

export async function getHistory() {
  const res = await fetch(`${API_BASE}/api/history`);
  return res.json();
}

export async function getSettings() {
  const res = await fetch(`${API_BASE}/api/settings`);
  return res.json();
}

export async function saveSettings(data) {
  const res = await fetch(`${API_BASE}/api/settings`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function loadPorts() {
  const res = await fetch(`${API_BASE}/api/ports`);
  return res.json();
}

export function connectSSE(onMessage) {
  const es = new EventSource(`${API_BASE}/api/stream`);
  es.onmessage = (e) => {
    try { onMessage(JSON.parse(e.data)); } catch (err) { /* keepalive */ }
  };
  es.onerror = () => { /* auto-reconnect */ };
  return es;
}
