export function renderResultList(results, onSelect) {
  const list = document.getElementById("result-list");
  const count = document.getElementById("result-count");
  const status = document.getElementById("search-status");

  if (!results || !results.length) {
    count.textContent = "0";
    status.textContent = "";
    list.innerHTML = '<div class="empty-hint">未找到匹配的船期数据</div>';
    return;
  }

  count.textContent = results.length;
  status.textContent = "查询完成";

  list.innerHTML = results.map((r, i) => {
    const statusLabel = r.status === "in_transit" ? "航行中" : r.status === "arrived" ? "已到港" : "计划中";
    const statusClass = "status-" + (r.status || "scheduled");
    
    // Build transit timeline
    let transitHtml = "";
    if (r.route_points && r.route_points.length > 2) {
      transitHtml = '<div class="transit-timeline">';
      const showPoints = Math.min(5, r.route_points.length);
      const step = Math.max(1, Math.floor((r.route_points.length - 1) / (showPoints - 1)));
      for (let j = 0; j < showPoints; j++) {
        const idx = Math.min(j * step, r.route_points.length - 1);
        const label = idx === 0 ? r.origin : idx === r.route_points.length - 1 ? r.destination : "●";
        const isPort = idx === 0 || idx === r.route_points.length - 1;
        transitHtml += '<div class="tl-stop' + (isPort ? ' tl-port' : ' tl-way') + '">' +
          '<span class="tl-label">' + esc(label) + '</span>' +
        '</div>';
        if (j < showPoints - 1) transitHtml += '<div class="tl-connector"><span class="tl-days">~' + Math.round((r.route_points.length - 1) / (showPoints - 1) * (j+1)) + 'd</span></div>';
      }
      transitHtml += '</div>';
    }

    return `
    <div class="result-card" data-index="${i}">
      <div class="vessel-name">${esc(r.vessel)} ${esc(r.voyage)}</div>
      <div class="route">${esc(r.origin)} → ${esc(r.destination)}</div>
      <div class="voyage-info">${esc(r.carrier)}</div>
      ${transitHtml}
      <div class="dates">ETD: ${esc(r.etd || "-")} | ETA: ${esc(r.eta || "-")} | 航程约 ${r.route_points ? Math.floor(r.route_points.length * 1.2) : "?"} 天</div>
      <span class="status ${statusClass}">${statusLabel}</span>
      <button class="itinerary-btn" data-idx="${i}">📋 查看详细行程</button>
    </div>`;
  }).join("");

  // Click handlers for cards
  list.querySelectorAll(".result-card").forEach(card => {
    card.addEventListener("click", (e) => {
      if (e.target.classList.contains("itinerary-btn")) return;
      list.querySelectorAll(".result-card").forEach(c => c.classList.remove("active"));
      card.classList.add("active");
      const idx = parseInt(card.dataset.index);
      onSelect(results[idx]);
    });
  });

  // Click handlers for itinerary buttons
  list.querySelectorAll(".itinerary-btn").forEach(btn => {
    btn.addEventListener("click", async (e) => {
      e.stopPropagation();
      const idx = parseInt(btn.dataset.index);
      const r = results[idx];
      showItineraryPopup(r);
    });
  });

  if (results.length > 0 && onSelect) {
    const firstCard = list.querySelector(".result-card");
    if (firstCard) firstCard.classList.add("active");
    onSelect(results[0]);
  }
}

async function showItineraryPopup(result) {
  try {
    const resp = await fetch("/api/transit/" + encodeURIComponent(result.origin) + "/" + encodeURIComponent(result.destination));
    if (!resp.ok) { alert("行程数据不可用"); return; }
    const transit = await resp.json();
    if (!transit.stops) { alert("行程数据不可用"); return; }

    let html = '<div class="itinerary-popup-overlay" id="itineraryPopup">' +
      '<div class="itinerary-popup">' +
      '<div class="itinerary-header">' +
      '<h3>🚢 详细行程</h3>' +
      '<span class="itinerary-route">' + esc(result.vessel) + ' ' + esc(result.voyage) + ' | ' + esc(result.origin) + ' → ' + esc(result.destination) + '</span>' +
      '<button class="itinerary-close" id="itineraryClose">✕</button>' +
      '</div>' +
      '<div class="itinerary-list">';

    transit.stops.forEach((stop, i) => {
      const isPort = i === 0 || i === transit.stops.length - 1;
      const icon = isPort ? (i === 0 ? '🚩' : '🏁') : '●';
      const cls = isPort ? 'it-stop-port' : 'it-stop-way';
      const daysToNext = stop.transit_days > 0 ? ' → 下一站 ' + stop.transit_days + ' 天' : '';
      html += '<div class="it-stop ' + cls + '">' +
        '<div class="it-stop-icon">' + icon + '</div>' +
        '<div class="it-stop-info">' +
        '<div class="it-stop-name">' + esc(stop.name) + '</div>' +
        '<div class="it-stop-days">累计 ' + stop.cumulative_days + ' 天' + daysToNext + '</div>' +
        '</div>' +
      '</div>';
      if (i < transit.stops.length - 1) {
        html += '<div class="it-connector"></div>';
      }
    });

    html += '</div><div class="itinerary-footer">总航程约 <b>' + transit.total_days + '</b> 天</div></div></div>';

    document.body.insertAdjacentHTML("beforeend", html);

    document.getElementById("itineraryClose").addEventListener("click", () => {
      document.getElementById("itineraryPopup").remove();
    });
    document.getElementById("itineraryPopup").addEventListener("click", (e) => {
      if (e.target.id === "itineraryPopup") e.target.remove();
    });
  } catch(e) {
    console.error("itinerary fetch failed", e);
  }
}export function renderMonitorList(monitors, onDelete, onCheckNow) {
  const list = document.getElementById("monitor-list");
  if (!monitors || !monitors.length) {
    list.innerHTML = '<p class="empty-hint">暂无监控任务，点击 "+ 添加监控" 开始</p>';
    return;
  }

  list.innerHTML = monitors.map(m => `
    <div class="monitor-card">
      <div class="route">${esc(m.origin)} → ${esc(m.destination)}</div>
      <div class="meta">间隔: ${m.interval_minutes}分钟 | 上次: ${m.last_check || "从未"} | ${m.active ? "运行中" : "已暂停"}</div>
      <div class="actions">
        <button class="check-now" data-id="${m.id}">⚡ 立即查询</button>
        <button class="danger delete-monitor" data-id="${m.id}">删除</button>
      </div>
    </div>
  `).join("");

  list.querySelectorAll(".delete-monitor").forEach(btn =>
    btn.addEventListener("click", () => onDelete(parseInt(btn.dataset.id)))
  );
  list.querySelectorAll(".check-now").forEach(btn =>
    btn.addEventListener("click", () => onCheckNow(parseInt(btn.dataset.id)))
  );
}

export function renderHistoryList(records) {
  const list = document.getElementById("history-list");
  if (!records || !records.length) {
    list.innerHTML = '<p class="empty-hint">暂无历史记录</p>';
    return;
  }

  list.innerHTML = records.map(r => `
    <div class="history-card">
      <div class="vessel-name">${esc(r.vessel)} ${esc(r.voyage)}</div>
      <div class="route">${esc(r.origin)} → ${esc(r.destination)}</div>
      <div class="meta">ETD: ${esc(r.etd || "-")} | ETA: ${esc(r.eta || "-")} | ${r.created_at || ""}</div>
    </div>
  `).join("");
}

export function notifyBrowser(title, body) {
  if (!("Notification" in window)) return;
  if (Notification.permission === "granted") {
    new Notification(title, { body, icon: "🚢" });
  } else if (Notification.permission !== "denied") {
    Notification.requestPermission().then(p => {
      if (p === "granted") new Notification(title, { body, icon: "🚢" });
    });
  }
}

function esc(s) {
  if (!s) return "";
  const div = document.createElement("div");
  div.textContent = s;
  return div.innerHTML;
}
