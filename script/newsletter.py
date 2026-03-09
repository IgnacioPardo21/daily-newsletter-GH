import requests
import os
import smtplib
from email.mime.text import MIMEText
import openai

# Variables de entorno
API_KEY = os.environ.get("NEWS_API_KEY")
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")  # OpenWeatherMap

openai.api_key = OPENAI_API_KEY

# Archivo para controlar duplicados
sent_urls_file = "data/sent_urls.txt"
if os.path.exists(sent_urls_file):
    with open(sent_urls_file, "r") as f:
        sent_urls = set(line.strip() for line in f.readlines())
else:
    sent_urls = set()

# --- Datos de mercado usando Finnhub ---
symbols = {
    "IBEX 35": "^IBEX",
    "NASDAQ": "^IXIC",
    "DOW": "^DJI"
}

ibex_summary = []
for name, symbol in symbols.items():
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        price = data.get("c", 0)
        change_pct = data.get("dp", 0)
        ibex_summary.append(f"{name}: {change_pct:+.2f}% ({price})")
    except:
        ibex_summary.append(f"{name}: no disponible")

ibex_summary_str = ", ".join(ibex_summary)

# --- Clima de Valencia ---
try:
    weather_response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q=Valencia,ES&units=metric&appid={WEATHER_API_KEY}"
    )
    weather_data = weather_response.json()
    clima_valencia = f"{weather_data['weather'][0]['description'].title()}, {weather_data['main']['temp']}°C"
except:
    clima_valencia = "No se pudo obtener el clima."

# Temas a buscar
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

# Cabecera del email
newsletter = f"""
<html>
<body style="font-family:Arial, sans-serif; line-height:1.4; color:#333;">
<h1 style="color:#1a73e8;">☕ Buenos días</h1>
<p>Aquí tienes tu resumen diario de noticias.</p>
<hr>

<h2 style="color:#ff5722;">📈 Mercados</h2>
<p>{ibex_summary_str}</p>

<h2 style="color:#03a9f4;">🌤 Clima Valencia</h2>
<p>{clima_valencia}</p>
<hr>
"""

# Recorremos los temas
for topic in topics:
    url = f"https://newsapi.org/v2/everything?q={topic}&language=es&pageSize=3&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    newsletter += f"<h2 style='color:#4caf50;'>📌 {topic.title()}</h2><ul>"

    if "articles" in data:
        for article in data["articles"][:3]:
            title = article["title"]
            link = article["url"]
            source = article["source"]["name"]
            description = article.get("description") or ""

            # Filtrar duplicados y noticias irrelevantes
            if link in sent_urls or len(description) < 50:
                continue

            # Generar resumen con IA
            try:
                prompt = f"Resume en 2-3 líneas esta noticia para una newsletter profesional: {description}"
                response_ai = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role":"user","content":prompt}],
                    temperature=0.5,
                    max_tokens=60
                )
                resumen = response_ai.choices[0].message.content.strip()
            except:
                resumen = description

            # Añadir al newsletter
            newsletter += f"""
            <li style="margin-bottom:10px;">
                <a href="{link}"><b>{title}</b></a><br>
                <small>{source}</small><br>
                <em>{resumen}</em>
            </li>
            """
            sent_urls.add(link)

    newsletter += "</ul>"

# Pie del email
newsletter += """
<hr>
<p>Esta es tu newsletter automática generada desde GitHub Actions.</p>
</body>
</html>
"""

# Preparar email
msg = MIMEText(newsletter, "html")
msg["Subject"] = "Tu newsletter diaria"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO

# Enviar email
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL_USER, EMAIL_PASS)
server.send_message(msg)
server.quit()

# Guardar URLs enviadas
os.makedirs("data", exist_ok=True)
with open(sent_urls_file, "w") as f:
    for url in sent_urls:
        f.write(url + "\n")

print("Email enviado")
