import sqlite3, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from routes import get_route_waypoints_simple
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "voyages.db")
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("DELETE FROM voyages")

now = datetime.now()
today = now.strftime("%Y-%m-%d")

sample_voyages = [
    # in_transit voyages with PAST etd (ship is currently en route)
    ("COSCO SHIPPING ARIES", "065E", "中远海运", "上海", "洛杉矶", (now - timedelta(days=8)).strftime("%Y-%m-%d"), (now + timedelta(days=7)).strftime("%Y-%m-%d"), "in_transit"),
    ("ONE CONTINUITY", "061W", "ONE LINE", "上海", "洛杉矶", (now - timedelta(days=5)).strftime("%Y-%m-%d"), (now + timedelta(days=10)).strftime("%Y-%m-%d"), "in_transit"),
    ("EVER GIVEN", "128W", "长荣海运", "上海", "洛杉矶", (now - timedelta(days=3)).strftime("%Y-%m-%d"), (now + timedelta(days=12)).strftime("%Y-%m-%d"), "in_transit"),
    ("COSCO SHIPPING SAGITTARIUS", "071E", "中远海运", "宁波", "温哥华", (now - timedelta(days=6)).strftime("%Y-%m-%d"), (now + timedelta(days=8)).strftime("%Y-%m-%d"), "in_transit"),
    ("HMM COPENHAGEN", "006E", "HMM", "深圳", "汉堡", (now - timedelta(days=10)).strftime("%Y-%m-%d"), (now + timedelta(days=10)).strftime("%Y-%m-%d"), "in_transit"),
    ("COSCO SHIPPING TAURUS", "073E", "中远海运", "上海", "温哥华", (now - timedelta(days=4)).strftime("%Y-%m-%d"), (now + timedelta(days=10)).strftime("%Y-%m-%d"), "in_transit"),
    ("MSC DIANA", "FD622W", "MSC", "上海", "洛杉矶", (now - timedelta(days=2)).strftime("%Y-%m-%d"), (now + timedelta(days=13)).strftime("%Y-%m-%d"), "in_transit"),
    
    # scheduled (future) voyages
    ("CMA CGM TITAN", "0MEGHW1", "CMA CGM", "上海", "洛杉矶", (now + timedelta(days=5)).strftime("%Y-%m-%d"), (now + timedelta(days=20)).strftime("%Y-%m-%d"), "scheduled"),
    ("HMM ALGECIRAS", "004W", "HMM", "上海", "洛杉矶", (now + timedelta(days=7)).strftime("%Y-%m-%d"), (now + timedelta(days=22)).strftime("%Y-%m-%d"), "scheduled"),
    ("MAERSK ESSEN", "622E", "MAERSK", "宁波", "温哥华", (now + timedelta(days=2)).strftime("%Y-%m-%d"), (now + timedelta(days=16)).strftime("%Y-%m-%d"), "scheduled"),
    ("CMA CGM CHRISTOPHE COLOMB", "0MEG4W1", "CMA CGM", "上海", "鹿特丹", (now + timedelta(days=10)).strftime("%Y-%m-%d"), (now + timedelta(days=40)).strftime("%Y-%m-%d"), "scheduled"),
    ("MSC OSCAR", "FD624W", "MSC", "上海", "鹿特丹", (now + timedelta(days=13)).strftime("%Y-%m-%d"), (now + timedelta(days=43)).strftime("%Y-%m-%d"), "scheduled"),
    ("OOCL HONG KONG", "065E", "OOCL", "深圳", "洛杉矶", (now + timedelta(days=3)).strftime("%Y-%m-%d"), (now + timedelta(days=20)).strftime("%Y-%m-%d"), "scheduled"),
    ("MAERSK MC-KINNEY MOLLER", "630W", "MAERSK", "天津", "汉堡", (now + timedelta(days=4)).strftime("%Y-%m-%d"), (now + timedelta(days=24)).strftime("%Y-%m-%d"), "scheduled"),
    ("APL VANDA", "018E", "APL", "青岛", "温哥华", (now + timedelta(days=2)).strftime("%Y-%m-%d"), (now + timedelta(days=16)).strftime("%Y-%m-%d"), "scheduled"),
    ("ONE EAGLE", "063E", "ONE LINE", "宁波", "洛杉矶", (now + timedelta(days=6)).strftime("%Y-%m-%d"), (now + timedelta(days=21)).strftime("%Y-%m-%d"), "scheduled"),
    ("MSC GULSUN", "FD626W", "MSC", "青岛", "鹿特丹", (now + timedelta(days=8)).strftime("%Y-%m-%d"), (now + timedelta(days=38)).strftime("%Y-%m-%d"), "scheduled"),
    ("CMA CGM ANTOINE DE SAINT EXUPERY", "0MEG5W1", "CMA CGM", "上海", "温哥华", (now + timedelta(days=9)).strftime("%Y-%m-%d"), (now + timedelta(days=23)).strftime("%Y-%m-%d"), "scheduled"),
    ("EVER ACE", "130W", "长荣海运", "深圳", "鹿特丹", (now + timedelta(days=12)).strftime("%Y-%m-%d"), (now + timedelta(days=42)).strftime("%Y-%m-%d"), "scheduled"),
    ("HMM ST. PETERSBURG", "008E", "HMM", "上海", "汉堡", (now + timedelta(days=6)).strftime("%Y-%m-%d"), (now + timedelta(days=26)).strftime("%Y-%m-%d"), "scheduled"),
]

count = 0
for v in sample_voyages:
    vessel, voyage_no, carrier, origin, dest, etd, eta, status = v
    route_points = get_route_waypoints_simple(origin, dest)
    if route_points is None:
        from ports import get_port_coords
        o = get_port_coords(origin)
        d = get_port_coords(dest)
        route_points = [o, d] if o and d else [[31.23,121.47],[33.77,-118.22]]
    
    conn.execute(
        "INSERT INTO voyages (vessel, voyage, carrier, origin, destination, etd, eta, status, route_points, source) VALUES (?,?,?,?,?,?,?,?,?,?)",
        [vessel, voyage_no, carrier, origin, dest, etd, eta, status, json.dumps(route_points), ""]
    )
    count += 1

conn.commit()
conn.close()
print(f"Seeded {count} voyages")
print(f"7 in_transit (past etd), 13 scheduled (future)")
