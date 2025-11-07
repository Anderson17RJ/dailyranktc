# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import cloudscraper

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://thecrims.com"



def get_top50():
    scraper = cloudscraper.create_scraper()
    url = f"{BASE_URL}/api/v1/stats/killers?country=&character=&level="
    r = scraper.get(url)
    return r.json()["killers"][:50]


def fetch_user(scraper, user_id):
    url = f"{BASE_URL}/api/v1/user/{user_id}/stats"
    r = scraper.get(url)
    data = r.json()
    stats_user = data["stats_user"]
    respect_stats = data["respectStats"]

    kills_totais = stats_user["kills"]
    kills_ontem = respect_stats[-1]["kills"] if respect_stats else 0
    kills_hoje = kills_totais - kills_ontem

    return {
        "username": stats_user["username"],
        "kills_hoje": kills_hoje
    }

@app.get("/api/top50")
def api_top50():
    scraper = cloudscraper.create_scraper()
    top50 = get_top50()
    ranking = [fetch_user(scraper, p["user"]["id"]) for p in top50]
    ranking.sort(key=lambda x: x["kills_hoje"], reverse=True)
    return ranking