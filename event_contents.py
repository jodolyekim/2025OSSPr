import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def get_today_contents(json_path="static_event_contents.json", test_date=None):
    today = test_date or datetime.date.today()
    key = f"{today.month}-{today.day}"
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            db = json.load(f)
        return db.get(key, [])
    except FileNotFoundError:
        return []






