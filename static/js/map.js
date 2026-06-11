let map = null;
let routeLayers = [];
let markers = [];
let waypointMarkers = [];
let shipMarker = null;

export function initMap() {
  map = L.map("map-container", { zoomControl: true }).setView([28, 118], 5);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap",
    maxZoom: 18,
  }).addTo(map);

  setTimeout(() => map.invalidateSize(), 300);
  window.addEventListener("resize", () => map.invalidateSize());
}

export function showRoutes(results) {
  clearRoutes();
  if (!results || !results.length) return;

  const bounds = [];
  const colors = ["#0D4B7C", "#E53935", "#00A86B", "#8E44AD", "#FF6D00", "#00897B"];

  // Fetch transit info for the first (active) result
  fetchTransitAndDraw(results);

  results.forEach((r, idx) => {
    if (!r.route_points || !r.route_points.length) return;

    const coords = r.route_points;
    const color = colors[idx % colors.length];

    // Draw route line
    const line = L.polyline(coords, {
      color: color,
      weight: idx === 0 ? 4 : 2,
      opacity: idx === 0 ? 0.85 : 0.5,
      dashArray: idx === 0 ? "" : "8 4",
    }).addTo(map);
    routeLayers.push(line);

    // Direction arrows along route
    if (coords.length >= 2) {
      const step = Math.max(1, Math.floor(coords.length / 6));
      for (let i = 0; i < coords.length - 1; i += step) {
        const mid = [(coords[i][0] + coords[i+1][0]) / 2, (coords[i][1] + coords[i+1][1]) / 2];
        const angle = Math.atan2(coords[i+1][0] - coords[i][0], coords[i+1][1] - coords[i][1]) * 180 / Math.PI;
        L.marker(mid, {
          icon: L.divIcon({
            html: '<div style="color:' + color + ';font-size:9px;transform:rotate(' + (90-angle) + 'deg);opacity:0.6">▶</div>',
            className: "route-arrow",
            iconSize: [10, 10],
            iconAnchor: [5, 5],
          })
        }).addTo(map);
        waypointMarkers.push({remove: () => {}});  // will be cleaned up
      }
    }

    // Start port marker
    const startIcon = L.divIcon({
      html: '<div style="background:' + color + ';color:#fff;border-radius:50%;width:28px;height:28px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;border:2.5px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,0.3)">' + (idx + 1) + '</div>',
      className: "port-marker",
      iconSize: [28, 28],
      iconAnchor: [14, 14],
    });
    const startMarker = L.marker(coords[0], { icon: startIcon })
      .bindPopup('<b>' + esc(r.origin) + '</b><br/>' + esc(r.vessel||"") + ' ' + esc(r.voyage||"") + '<br/>ETD: ' + esc(r.etd||"TBD"))
      .addTo(map);
    markers.push(startMarker);

    // End port marker
    const endIcon = L.divIcon({
      html: '<div style="background:' + color + ';color:#fff;border-radius:50%;width:28px;height:28px;display:flex;align-items:center;justify-content:center;font-size:14px;border:2.5px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,0.3)">📍</div>',
      className: "port-marker",
      iconSize: [28, 28],
      iconAnchor: [14, 14],
    });
    const endMarker = L.marker(coords[coords.length - 1], { icon: endIcon })
      .bindPopup('<b>' + esc(r.destination) + '</b><br/>' + esc(r.vessel||"") + ' ' + esc(r.voyage||"") + '<br/>ETA: ' + esc(r.eta||"TBD"))
      .addTo(map);
    markers.push(endMarker);

    coords.forEach(c => bounds.push(c));
  });

  if (bounds.length) {
    map.fitBounds(bounds, { padding: [50, 50], maxZoom: 6 });
  }
}

async function fetchTransitAndDraw(results) {
  if (!results || !results.length) return;
  const r = results[0];
  
  try {
    // Fetch transit info for the first result
    const resp = await fetch("/api/transit/" + encodeURIComponent(r.origin) + "/" + encodeURIComponent(r.destination));
    if (!resp.ok) return;
    const transit = await resp.json();
    if (!transit.stops) return;

    // Draw waypoint labels
    const mainColor = "#0D4B7C";
    transit.stops.forEach((stop, i) => {
      if (i === 0 || i === transit.stops.length - 1) return; // Skip start/end (already labeled)

      const labelIcon = L.divIcon({
        html: '<div style="background:rgba(255,255,255,0.9);border:1px solid ' + mainColor + ';border-radius:4px;padding:2px 6px;font-size:10px;color:' + mainColor + ';white-space:nowrap;font-weight:500;box-shadow:0 1px 3px rgba(0,0,0,0.15)">' + esc(stop.name) + '</div>',
        className: "waypoint-label",
        iconSize: [0, 0],
        iconAnchor: [0, 0],
      });
      L.marker([stop.lat, stop.lng], { icon: labelIcon }).addTo(map);
      waypointMarkers.push({remove: () => {}});

      // Small dot for waypoint
      L.circleMarker([stop.lat, stop.lng], {
        radius: 2.5,
        fillColor: mainColor,
        color: "#fff",
        weight: 1,
        fillOpacity: 0.8,
      }).addTo(map);
      waypointMarkers.push({remove: () => {}});
    });

    // Draw ship position if in transit
    if (r.status === "in_transit") {
      try {
        const posResp = await fetch("/api/ship-position/" + 
          encodeURIComponent(r.origin) + "/" + encodeURIComponent(r.destination) + "/" +
          encodeURIComponent(r.etd) + "/" + encodeURIComponent(r.eta) + "/" + r.status);
        if (posResp.ok) {
          const pos = await posResp.json();
          if (pos.lat && pos.lng) {
            const shipIcon = L.divIcon({
              html: '<div style="font-size:22px;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.4))">🚢</div>',
              className: "ship-icon",
              iconSize: [28, 28],
              iconAnchor: [14, 14],
            });
            shipMarker = L.marker([pos.lat, pos.lng], { icon: shipIcon, zIndexOffset: 1000 })
              .bindPopup('<b>' + esc(r.vessel) + '</b><br/>📍 当前位置<br/>进度: ' + pos.progress + '%<br/>下一站: ' + esc(pos.next_stop) + (pos.days_to_next ? '<br/>预计 ' + pos.days_to_next + ' 天后到达' : ''))
              .addTo(map);
            markers.push(shipMarker);
          }
        }
      } catch(e) {}
    }
  } catch(e) { console.log("transit info fetch failed", e); }
}

export function clearRoutes() {
  if (shipMarker) { map.removeLayer(shipMarker); shipMarker = null; }
  routeLayers.forEach(l => map.removeLayer(l));
  routeLayers = [];
  markers.forEach(m => map.removeLayer(m));
  markers = [];
  waypointMarkers.forEach(m => { try { map.removeLayer(m); } catch(e) {} });
  waypointMarkers = [];
}

export function focusRoute(result) {
  if (result && result.route_points && result.route_points.length) {
    map.fitBounds(result.route_points, { padding: [50, 50], maxZoom: 6 });
  }
}

export function getMap() {
  return map;
}

function esc(s) {
  if (!s) return "";
  const div = document.createElement("div");
  div.textContent = s;
  return div.innerHTML;
}
