import { queryVoyages, getMonitors, addMonitor, deleteMonitor, getHistory, getSettings, saveSettings, loadPorts, connectSSE } from "./api.js";
import { initMap, showRoutes, focusRoute, getMap } from "./map.js";
import { renderResultList, renderMonitorList, renderHistoryList, notifyBrowser } from "./ui.js";

var vesselSuggestTimer = null;
var lastVesselData = [];

// Suggest vessels in datalist when typing vessel name
async function suggestVessels() {
  const origin = document.getElementById("origin-input").value.trim();
  const dest = document.getElementById("dest-input").value.trim();
  if (!origin || !dest) return;
  clearTimeout(vesselSuggestTimer);
  vesselSuggestTimer = setTimeout(async () => {
    try {
      const data = await queryVoyages(origin, dest, "");
      if (!data.results || !data.results.length) return;
      lastVesselData = data.results;
      const names = [...new Set(data.results.map(r => r.vessel).filter(Boolean))];
      const dl = document.getElementById("vessel-suggestions");
      if (dl) dl.innerHTML = names.map(n => '<option value="' + n + '">').join("");
    } catch (e) {}
  }, 500);
}

// Show vessel selection popup when origin+dest entered and no vessel specified
function showVesselPopup(results) {
  const modal = document.getElementById("vessel-modal");
  if (!modal) return;
  const list = document.getElementById("vessel-pick-list");
  if (!list) return;

  const vesselMap = {};
  results.forEach(r => {
    const key = r.vessel || "Unknown";
    if (!vesselMap[key]) {
      vesselMap[key] = { vessel: key, voyages: [], carriers: new Set() };
    }
    vesselMap[key].voyages.push(r);
    if (r.carrier) vesselMap[key].carriers.add(r.carrier);
  });

  const vessels = Object.values(vesselMap);
  if (vessels.length <= 1) return;

  list.innerHTML = vessels.map((v, i) => `
    <div class="vessel-pick-card" data-vessel="${escHtml(v.vessel)}">
      <div class="vp-name">🚢 ${escHtml(v.vessel)}</div>
      <div class="vp-info">
        ${[...v.carriers].map(c => escHtml(c)).join(' / ') || '未知船公司'}
        <span class="vp-count">${v.voyages.length} 条船期</span>
      </div>
    </div>
  `).join("");

  list.querySelectorAll(".vessel-pick-card").forEach(card => {
    card.addEventListener("click", () => {
      const vesselName = card.dataset.vessel;
      document.getElementById("vessel-input").value = vesselName;
      modal.style.display = "none";
      doSearch(vesselName);
    });
  });

  modal.style.display = "flex";
}

function escHtml(s) {
  if (!s) return "";
  const div = document.createElement("div");
  div.textContent = s;
  return div.innerHTML;
}

// Unified search function
async function doSearch(vesselOverride) {
  const origin = document.getElementById("origin-input").value.trim();
  const dest = document.getElementById("dest-input").value.trim();
  const vessel = vesselOverride || document.getElementById("vessel-input").value.trim();
  const status = document.getElementById("search-status");

  if (!origin && !dest) { /* allow empty for initial load */ }

  status.textContent = "查询中...";
  try {
    const data = await queryVoyages(origin, dest, vessel);
    if (!vesselOverride && !vessel && origin && dest && data.results && data.results.length > 1) {
      const vesselNames = [...new Set(data.results.map(r => r.vessel).filter(Boolean))];
      if (vesselNames.length > 1) {
        showVesselPopup(data.results);
        status.textContent = "请选择船名";
        return;
      }
    }
    renderResultList(data.results, (r) => focusRoute(r));
    showRoutes(data.results);
  } catch (err) {
    status.textContent = "查询失败";
    console.error(err);
  }
}

// === Routing ===
function navigate() {
  const hash = location.hash || "#query";
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-tab").forEach(t => t.classList.remove("active"));
  const page = document.getElementById("page-" + hash.slice(1));
  if (page) page.classList.add("active");
  const tab = document.querySelector('.nav-tab[href="' + hash + '"]');
  if (tab) tab.classList.add("active");
  if (hash === "#query") { setTimeout(() => getMap() && getMap().invalidateSize(), 100); }
  if (hash === "#monitor") loadMonitors();
  if (hash === "#history") loadHistory();
  if (hash === "#settings") loadSettings();
}
window.addEventListener("hashchange", navigate);

// === Search Events ===
document.getElementById("search-btn").addEventListener("click", () => doSearch());
document.getElementById("origin-input").addEventListener("input", suggestVessels);
document.getElementById("dest-input").addEventListener("input", suggestVessels);
document.getElementById("origin-input").addEventListener("keydown", (e) => { if (e.key === "Enter") doSearch(); });
document.getElementById("dest-input").addEventListener("keydown", (e) => { if (e.key === "Enter") doSearch(); });
document.getElementById("vessel-input").addEventListener("keydown", (e) => { if (e.key === "Enter") doSearch(); });

// Vessel popup buttons
document.getElementById("vessel-cancel").addEventListener("click", () => {
  document.getElementById("vessel-modal").style.display = "none";
});
document.getElementById("vessel-show-all").addEventListener("click", () => {
  document.getElementById("vessel-modal").style.display = "none";
  renderResultList(lastVesselData, (r) => focusRoute(r));
  showRoutes(lastVesselData);
});

// === Monitor Page ===
document.getElementById("add-monitor-btn").addEventListener("click", () => {
  document.getElementById("monitor-modal").style.display = "flex";
});

document.getElementById("mon-cancel").addEventListener("click", () => {
  document.getElementById("monitor-modal").style.display = "none";
});

document.getElementById("mon-confirm").addEventListener("click", async () => {
  const origin = document.getElementById("mon-origin").value.trim();
  const dest = document.getElementById("mon-dest").value.trim();
  if (!origin || !dest) return;

  await addMonitor(origin, dest);
  document.getElementById("monitor-modal").style.display = "none";
  document.getElementById("mon-origin").value = "";
  document.getElementById("mon-dest").value = "";
  loadMonitors();
});

async function loadMonitors() {
  try {
    const monitors = await getMonitors();
    renderMonitorList(monitors,
      async (id) => { await deleteMonitor(id); loadMonitors(); },
      async (id) => {
        const m = monitors.find(m => m.id === id);
        if (m) {
          try {
            const data = await queryVoyages(m.origin, m.destination, "");
            notifyBrowser("🚢 监控更新", m.origin + " -> " + m.destination + ": " + data.total + " 条结果");
          } catch (err) { console.error(err); }
        }
      }
    );
  } catch (err) { console.error(err); }
}

// === History Page ===
async function loadHistory() {
  try {
    const records = await getHistory();
    renderHistoryList(records);
  } catch (err) { console.error(err); }
}

// === Settings Page ===
async function loadSettings() {
  try {
    const s = await getSettings();
    document.getElementById("setting-interval").value = s.crawl_interval || "30";
    document.getElementById("setting-source").value = s.source_url || "";
    document.getElementById("setting-notify").checked = s.notify_enabled === "1";
  } catch (err) { console.error(err); }
}

document.getElementById("save-settings-btn").addEventListener("click", async () => {
  try {
    await saveSettings({
      crawl_interval: document.getElementById("setting-interval").value,
      source_url: document.getElementById("setting-source").value,
      notify_enabled: document.getElementById("setting-notify").checked ? "1" : "0",
    });
    alert("✅ 设置已保存");
  } catch (err) { console.error(err); }
});

// === SSE ===
connectSSE((msg) => {
  if (msg.type === "monitor_update") {
    notifyBrowser("🚢 船期更新", msg.origin + " -> " + msg.destination + ": " + msg.count + " 条新结果");
  }
});

// === Port Autocomplete ===
async function initPortSuggestions() {
  try {
    const ports = await loadPorts();
    const datalist = document.getElementById("port-list");
    datalist.innerHTML = Object.keys(ports).map(p => '<option value="' + p + '">').join("");
  } catch (err) { /* non-critical */ }
}

// === Init ===
initMap();
navigate();
initPortSuggestions();
// Auto-load all routes and show map on page load
doSearch();

// Request notification permission on first interaction
document.addEventListener("click", () => {
  if ("Notification" in window && Notification.permission === "default") {
    Notification.requestPermission();
  }
}, { once: true });