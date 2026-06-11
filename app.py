import json, queue, threading
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
from database import init_db, get_db
from ports import load_ports

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)

@app.route("/vtest")
def vtest():
    return send_from_directory("static", "_voyage_test.html")

@app.route("/test")
def test_page():
    return "<!DOCTYPE html><html><head><meta charset=UTF-8><title>Test</title></head><body><h1 style=color:green>OK - Server Works!</h1><p>Time: " + str(__import__("datetime").datetime.now()) + "</p></body></html>"

@app.route("/os")
def os_index():
    return send_from_directory(".", "seafreight-os.html")

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/ports")
def api_ports():
    return jsonify(load_ports())

@app.route("/api/query", methods=["POST"])
def api_query():
    data = request.get_json()
    origin = data.get("origin", "").strip()
    destination = data.get("destination", "").strip()
    vessel = data.get("vessel", "").strip()

    db = get_db()
    conditions = []
    params = []
    if origin:
        conditions.append("origin LIKE ?")
        params.append("%" + origin + "%")
    if destination:
        conditions.append("destination LIKE ?")
        params.append("%" + destination + "%")
    if vessel:
        conditions.append("vessel LIKE ?")
        params.append("%" + vessel + "%")

    where = (" WHERE " + " AND ".join(conditions)) if conditions else ""
    rows = db.execute("SELECT * FROM voyages" + where + " ORDER BY created_at DESC LIMIT 50", params).fetchall()
    results = []
    for row in rows:
        r = dict(row)
        try: r["route_points"] = json.loads(r["route_points"])
        except: r["route_points"] = []
        results.append(r)
    db.close()

    # If DB has no results, try crawler inline (immediate response)
    if not results and (origin or destination):
        try:
            from crawler import search_voyages
            results = search_voyages(origin, destination, vessel)
        except Exception as e:
            print(f"[crawler] {e}")
    # Also background-refresh for next time
    if origin or destination:
        def fetch_external():
            try:
                from crawler import search_voyages
                search_voyages(origin, destination, vessel)
            except Exception as e:
                print(f"[crawler bg] {e}")
        threading.Thread(target=fetch_external, daemon=True).start()

    return jsonify({"results": results, "total": len(results)})

@app.route("/api/monitors", methods=["GET", "POST"])
def api_monitors():
    db = get_db()
    if request.method == "GET":
        rows = db.execute("SELECT * FROM monitors ORDER BY created_at DESC").fetchall()
        db.close()
        return jsonify([dict(r) for r in rows])
    else:
        data = request.get_json()
        db.execute("INSERT INTO monitors (origin, destination) VALUES (?, ?)", [data["origin"], data["destination"]])
        db.commit(); db.close()
        from scheduler import check_monitors
        threading.Thread(target=check_monitors, daemon=True).start()
        return jsonify({"ok": True}), 201

@app.route("/api/monitors/<int:mid>", methods=["DELETE"])
def api_monitor_delete(mid):
    db = get_db()
    db.execute("DELETE FROM monitors WHERE id=?", [mid])
    db.commit(); db.close()
    return jsonify({"ok": True})

@app.route("/api/history")
def api_history():
    db = get_db()
    rows = db.execute("SELECT * FROM voyages ORDER BY created_at DESC LIMIT 200").fetchall()
    db.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/settings", methods=["GET", "PUT"])
def api_settings():
    db = get_db()
    if request.method == "GET":
        rows = db.execute("SELECT key, value FROM settings").fetchall()
        db.close()
        return jsonify({r["key"]: r["value"] for r in rows})
    else:
        data = request.get_json()
        for k, v in data.items():
            db.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", [k, v])
        db.commit(); db.close()
        return jsonify({"ok": True})

@app.route("/api/transit/<origin>/<destination>")
def api_transit(origin, destination):
    from routes import get_transit_info
    return jsonify(get_transit_info(origin, destination))

@app.route("/api/ship-position/<origin>/<destination>/<etd>/<eta>/<status>")
def api_ship_position(origin, destination, etd, eta, status):
    from routes import get_current_position
    return jsonify(get_current_position(origin, destination, etd, eta, status))

@app.route("/api/parse-booking", methods=["POST"])
def api_parse_booking():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    import openpyxl, io
    wb = openpyxl.load_workbook(io.BytesIO(request.files["file"].read()))
    ws = wb.active
    data = {"headers": [], "rows": []}
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            data["headers"] = [str(c) for c in row if c]
        else:
            data["rows"].append([str(c) if c else "" for c in row])
    return jsonify(data)

@app.route("/api/stream")
def api_stream():
    q = queue.Queue()
    def event_stream():
        while True:
            try:
                msg = q.get(timeout=30)
                yield "data: " + json.dumps(msg) + "\n\n"
            except queue.Empty:
                yield ": keepalive\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    init_db()
    # Auto-seed if empty
    db = get_db()
    count = db.execute("SELECT COUNT(*) FROM voyages").fetchone()[0]
    db.close()
    if count == 0:
        from seed_voyages import sample_voyages
        from routes import get_route_waypoints_simple
        from ports import get_port_coords
        db2 = get_db()
        for v in sample_voyages:
            vessel, voyage_no, carrier, origin, dest, etd, eta, status = v
            rp = get_route_waypoints_simple(origin, dest)
            if rp is None:
                o = get_port_coords(origin); d = get_port_coords(dest)
                rp = [o, d] if o and d else [[31.23,121.47],[33.77,-118.22]]
            db2.execute("INSERT INTO voyages(vessel,voyage,carrier,origin,destination,etd,eta,status,route_points,source) VALUES(?,?,?,?,?,?,?,?,?,?)",
                [vessel,voyage_no,carrier,origin,dest,etd,eta,status,json.dumps(rp),""])
        db2.commit(); db2.close()
        print("[init] Seeded initial voyage data")
    from scheduler import start_scheduler
    start_scheduler(app)
    print("Starting server on http://localhost:5090")
    import os
    port = int(os.environ.get('PORT', 5090))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)