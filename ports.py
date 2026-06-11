import json
import os

PORTS_FILE = os.path.join(os.path.dirname(__file__), "data", "ports.json")

def load_ports():
    with open(PORTS_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def get_port_coords(port_name):
    ports = load_ports()
    for name, coords in ports.items():
        if port_name in name or name in port_name:
            return coords
    return None
