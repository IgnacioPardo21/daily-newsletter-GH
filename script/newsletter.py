import requests
import os
import smtplib
from email.mime.text import MIMEText
import openai
import subprocess

API_KEY = os.environ.get("NEWS_API_KEY")
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

sent_urls_file = "data/sent_urls.txt"

if os.path.exists(sent_urls_file):
    with open(sent_urls_file, "r") as f:
        sent_urls = set(line.strip() for line in f.readlines())
else:
    sent_urls = set()

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

candidates = []

for topic in topics:

    url = f"https://newsapi.org/v2/everything?q={topic}&language=es&pageSize=10&sortBy=publishedAt&apiKey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if "articles" not in data:
        continue

    for article in data["articles"]:

        link = article["url"]
        title = article["title"]
        source = article["source"]["name"]
        description = article.get("description") or ""

        if link in sent_urls:
            continue

        if len(description) < 50:
            continue

        candidates.append({
            "title": title,
            "link": link,
            "source": source,
            "description": description
        })

# Si no hay noticias
if len(candidates) == 0:
    print("No hay noticias nuevas")
    exit()

# PREPARAR TEXTO PARA IA
news_text = ""

for i, c in enumerate(candidates):

    news_text += f"""
Noticia {i}

Título: {c['title']}
Descripción: {c['description']}
"""

prompt = f"""
Selecciona las 15 noticias MÁS IMPORTANTES para una newsletter diaria.

Temas prioritarios:
real estate España
bolsa
pádel
fútbol
política España
sucesos España
Valencia
tecnología
inteligencia artificial
innovación empresarial

Devuelve SOLO los números de las noticias seleccionadas separados por coma.

Noticias:

{news_text}
"""

response_ai = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

selected = response_ai.choices[0].message.content

indexes = []

for x in selected.replace(" ", "").split(","):
    try:
        indexes.append(int(x))
    except:
        pass

selected_news = [candidates[i] for i in indexes if i < len(candidates)]

newsletter = """
<html>
<body style="font-family:Arial, sans-serif;">
<h1 style="color:#000;">☕ Buenos días</h1>
<p>Estas son las noticias más relevantes de hoy.</p>
<hr>
<ul>
"""

for news in selected_news:

    try:

        prompt = f"Resume esta noticia en 2 líneas: {news['description']}"

        resumen = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=60
        )

        resumen = resumen.choices[0].message.content.strip()

    except:
        resumen = news["description"]

    newsletter += f"""
<li>
<a href="{news['link']}"><b>{news['title']}</b></a><br>
<small>{news['source']}</small><br>
{resumen}
</li><br>
"""

    sent_urls.add(news["link"])

newsletter += """
</ul>
<hr>
<p>Newsletter automática.</p>
</body>
</html>
"""

msg = MIMEText(newsletter, "html")
msg["Subject"] = "Tu newsletter diaria"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(EMAIL_USER, EMAIL_PASS)
server.send_message(msg)
server.quit()

os.makedirs("data", exist_ok=True)

with open(sent_urls_file, "w") as f:
    for url in sent_urls:
        f.write(url + "\n")

try:

    subprocess.run(["git", "config", "--global", "user.email", "bot@github.com"])
    subprocess.run(["git", "config", "--global", "user.name", "github-actions"])

    subprocess.run(["git", "add", sent_urls_file])
    subprocess.run(["git", "commit", "-m", "update sent urls"])
    subprocess.run(["git", "push"])

except:
    pass

print("Email enviado")
