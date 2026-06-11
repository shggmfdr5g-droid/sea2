import sqlite3
import os

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "voyages.db")

def get_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS voyages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vessel TEXT, voyage TEXT, carrier TEXT,
            origin TEXT, destination TEXT,
            etd TEXT, eta TEXT, status TEXT,
            route_points TEXT,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS monitors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT, destination TEXT,
            interval_minutes INTEGER DEFAULT 30,
            active INTEGER DEFAULT 1,
            last_check TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        INSERT OR IGNORE INTO settings (key, value) VALUES ('crawl_interval', '30');
        INSERT OR IGNORE INTO settings (key, value) VALUES ('notify_enabled', '1');
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("DB initialized at", DB_PATH)
