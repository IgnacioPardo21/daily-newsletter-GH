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

            # Obtener la descripción original de la noticia
            description = article.get("description") or ""

            # Generar resumen de 2-3 líneas usando GPT
            if description:
                prompt = f"Resume en 2-3 líneas esta noticia para una newsletter profesional: {description}"
                try:
                    response_ai = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role":"user","content":prompt}],
                        temperature=0.5,
                        max_tokens=60
                    )
                    resumen = response_ai.choices[0].message.content.strip()
                except Exception as e:
                    resumen = description  # fallback si hay error
            else:
                resumen = "No hay descripción disponible."

            # Añadir noticia al HTML de la newsletter
            newsletter += f"""
            <li>
                <a href="{link}"><b>{title}</b></a><br>
                <small>{source}</small><br>
                <em>{resumen}</em>
            </li>
            """

    newsletter += "</ul>"  # cerrar la lista del tema

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

print("Email enviado")
