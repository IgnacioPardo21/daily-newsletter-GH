import requests
import os

API_KEY = os.environ.get("NEWS_API_KEY")

topics = [
    "real estate España",
    "bolsa",
    "pádel",
    "fútbol",
    "política España",
    "sucesos España",
    "Valencia sucesos",
    "tecnología",
    "inteligencia artificial",
    "innovación empresarial España"
]

for topic in topics:

    url = f"https://newsapi.org/v2/everything?q={topic}&language=es&pageSize=3&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    print(f"\n=== {topic.upper()} ===")

    if "articles" in data:
        for article in data["articles"][:3]:
            print("-", article["title"])
