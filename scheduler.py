from apscheduler.schedulers.background import BackgroundScheduler
import json
from database import get_db
from crawler import search_voyages

scheduler = BackgroundScheduler()

def check_monitors():
    db = get_db()
    monitors = db.execute("SELECT * FROM monitors WHERE active = 1").fetchall()
    db.close()

    for m in monitors:
        try:
            results = search_voyages(origin=m["origin"], destination=m["destination"])
            if results:
                notify_clients({
                    "type": "monitor_update",
                    "monitor_id": m["id"],
                    "origin": m["origin"],
                    "destination": m["destination"],
                    "count": len(results),
                    "results": results[:5]
                })
        except Exception as e:
            print(f"[scheduler] Error checking monitor {m['id']}: {e}")

        db = get_db()
        db.execute("UPDATE monitors SET last_check = datetime('now', 'localtime') WHERE id = ?", [m["id"]])
        db.commit()
        db.close()

def notify_clients(msg):
    from flask import current_app
    try:
        clients = current_app.config.get("sse_clients", [])
        for q in clients:
            try:
                q.put_nowait(msg)
            except:
                pass
    except:
        pass

def start_scheduler(app):
    scheduler.add_job(check_monitors, "interval", minutes=30, id="monitor_check")
    scheduler.start()
    print("[scheduler] Started, checking every 30 minutes")

def stop_scheduler():
    scheduler.shutdown()
