import json
from pathlib import Path

path = Path(__file__).parent / "items_db.json"
with path.open("r") as f:
    items_db = json.load(f)
