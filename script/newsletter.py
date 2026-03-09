import requests
import os
import smtplib
from email.mime.text import MIMEText
import openai

# Variables de entorno
API_KEY = os.environ.get("NEWS_API_KEY")
EMAIL_USER = os.environ.get("EMAIL_USER")  # remitente
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")      # receptor
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Archivo para controlar duplicados
sent_urls_file = "data/sent_urls.txt"
if os.path.exists(sent_urls_file):
    with open(sent_urls_file, "r") as f:
        sent_urls = set(line.strip() for line in f.readlines())
else:
    sent_urls = set()

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
newsletter = """
<html>
<body>
<h2>☕ Buenos días</h2>
<p>Aquí tienes tu resumen diario de noticias.</p>
<hr>
"""

# Recorremos los temas
for topic in topics:

    url = f"https://newsapi.org/v2/everything?q={topic}&language=es&pageSize=3&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    newsletter += f"<h3>{topic.title()}</h3><ul>"

    if "articles" in data:
        for article in data["articles"][:3]:
            title = article["title"]
            link = article["url"]
            source = article["source"]["name"]
            description = article.get("description") or ""

            # Filtrar duplicados y noticias irrelevantes
            if link in sent_urls:
                continue
            if len(description) < 50:  # menos de 50 caracteres → irrelevante
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
                resumen = description  # fallback si hay error

            # Añadir al newsletter
            newsletter += f"""
            <li>
                <a href="{link}"><b>{title}</b></a><br>
                <small>{source}</small><br>
                <em>{resumen}</em>
            </li>
            """

            # Añadir a URLs enviadas
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

# Guardar URLs enviadas hoy
os.makedirs("data", exist_ok=True)
with open(sent_urls_file, "w") as f:
    for url in sent_urls:
        f.write(url + "\n")

print("Email enviado")
