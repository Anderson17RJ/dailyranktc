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
    scraper = cloudscraper.create_scraper(
        browser={'browser':'chrome', 'platform':'windows', 'mobile': False}
    )
    url = f"{BASE_URL}/api/v1/stats/killers?country=&character=&level="
    r = scraper.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    })

    if r.status_code != 200:
        print(f"Erro HTTP {r.status_code} ao acessar {url}")
        print("Conteudo retornado:")
        print(r.text)
        raise Exception(f"Erro ao buscar dados do top50: {r.status_code}")
    
    try:
        return r.json()["killers"][:50]
    except Exception as e:
        print("Erro ao decodificar JSON:")
        print(r.text)
        raise Exception(f"Erro ao processar JSON do top50: {e}")


def fetch_user(scraper, user_id):
    url = f"{BASE_URL}/api/v1/user/{user_id}/stats"
    r = scraper.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    })

    if r.status_code != 200:
        return {"username": f"ID {user_id}", "kills_hoje": 0}
    
    try:
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
    except Exception:
        return {"username": f"ID {user_id}", "kills_hoje": 0}

@app.get("/api/top50")
def api_top50():
    scraper = cloudscraper.create_scraper(
        browser={'browser':'chrome', 'platform':'windows', 'mobile': False}
    )

    try:
        top50 = get_top50()
        ranking = [fetch_user(scraper, p["user"]["id"]) for p in top50]
        ranking.sort(key=lambda x: x["kills_hoje"], reverse=True)
        return ranking
    except Exception as e:
        return {"error":str(e)}