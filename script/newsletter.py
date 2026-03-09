import requests
import os
import smtplib
from email.mime.text import MIMEText

API_KEY = os.environ.get("NEWS_API_KEY")
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")

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

newsletter = ""

for topic in topics:

    url = f"https://newsapi.org/v2/everything?q={topic}&language=es&pageSize=3&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    newsletter += f"\n\n=== {topic.upper()} ===\n"

    if "articles" in data:
        for article in data["articles"][:3]:
            newsletter += "- " + article["title"] + "\n"

msg = MIMEText(newsletter)
msg["Subject"] = "Tu newsletter diaria"
msg["From"] = EMAIL_USER
msg["To"] = os.environ.get("EMAIL_TO")

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL_USER, EMAIL_PASS)
server.send_message(msg)
server.quit()

print("Email enviado")
