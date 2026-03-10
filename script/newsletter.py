import requests
import os
import smtplib
from email.mime.text import MIMEText
import openai
import subprocess

# Variables de entorno
API_KEY = os.environ.get("NEWS_API_KEY")
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")
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
<body style="font-family:Arial, sans-serif; line-height:1.4; color:#333;">
<h1 style="color:#000;">☕ Buenos días</h1>
<p>Aquí tienes tu resumen diario de noticias.</p>
<hr>
"""

# Recorremos los temas
for topic in topics:

    url = f"https://newsapi.org/v2/everything?q={topic}&language=es&pageSize=5&sortBy=publishedAt&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    newsletter += f"<h2 style='color:#000;'>📌 {topic.title()}</h2><ul>"

    if "articles" in data:
        for article in data["articles"]:

            title = article["title"]
            link = article["url"]
            source = article["source"]["name"]
            description = article.get("description") or ""

            if link in sent_urls:
                continue

            if len(description) < 50:
                continue

            # IA decide si es relevante
            try:
                relevance_prompt = f"""
                Esta noticia es relevante para una newsletter informativa diaria?
                Responde SOLO SI o NO.

                Titular: {title}
                Descripción: {description}
                """

                relevance = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": relevance_prompt}],
                    temperature=0,
                    max_tokens=5
                )

                decision = relevance.choices[0].message.content.strip().upper()

                if "NO" in decision:
                    continue

            except:
                pass

            # Generar resumen con IA
            try:
                prompt = f"Resume en 2-3 líneas esta noticia para una newsletter profesional: {description}"

                response_ai = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=60
                )

                resumen = response_ai.choices[0].message.content.strip()

            except:
                resumen = description

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

# Hacer commit automático para persistir duplicados
try:
    subprocess.run(["git", "config", "--global", "user.email", "bot@github.com"])
    subprocess.run(["git", "config", "--global", "user.name", "github-actions"])
    subprocess.run(["git", "add", sent_urls_file])
    subprocess.run(["git", "commit", "-m", "update sent urls"])
    subprocess.run(["git", "push"])
except:
    pass

print("Email enviado")
