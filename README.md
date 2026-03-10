📰 Newsletter automática con IA

Este proyecto genera y envía automáticamente una newsletter diaria de noticias personalizadas, utilizando:

agregación de noticias mediante NewsAPI

filtrado y resumen con IA

envío automático por email

ejecución programada con GitHub Actions

El sistema busca noticias sobre temas definidos, filtra duplicados, usa IA para seleccionar contenido relevante y envía un email diario con un resumen claro y rápido de leer.

⚙️ Cómo funciona

El flujo del sistema es el siguiente:

Búsqueda de noticias

El script consulta la API de noticias y obtiene artículos recientes sobre temas definidos por el usuario.

Ejemplo de temas actuales:

Real Estate en España

Bolsa y economía

Pádel

Fútbol

Política española

Sucesos en España

Sucesos en Valencia

Tecnología

Inteligencia Artificial

Innovación empresarial

Eliminación de duplicados

El sistema guarda todas las URLs ya enviadas en el archivo:

data/sent_urls.txt

Antes de incluir una noticia en la newsletter, el script comprueba si ya ha sido enviada anteriormente.

Si ya existe en el archivo:

se descarta automáticamente

Esto evita recibir la misma noticia en días diferentes.

Filtrado de relevancia con IA

Cada noticia pasa por un filtro de IA que responde a la pregunta:

¿Esta noticia es relevante para una newsletter diaria?

La IA responde únicamente:

SI
NO

Si la respuesta es NO, la noticia se descarta.

Generación de resumen

Para cada noticia relevante, la IA genera un resumen breve de 2-3 líneas, pensado para lectura rápida en email.

Construcción de la newsletter

El email final incluye:

saludo inicial

noticias agrupadas por tema

titular

fuente

resumen generado por IA

enlace a la noticia completa

Ejemplo de estructura:

☕ Buenos días

📌 Tecnología
- Titular
- Fuente
- Resumen IA

📌 Bolsa
- Titular
- Fuente
- Resumen IA

Envío automático por email

El email se envía mediante SMTP usando Gmail.

Persistencia de noticias enviadas

Después del envío, el sistema:

actualiza data/sent_urls.txt

hace commit automáticamente

sube el archivo al repositorio

Esto permite que el sistema recuerde qué noticias ya se enviaron, incluso en ejecuciones futuras.

🕒 Automatización

La ejecución automática se realiza mediante GitHub Actions.

Ejemplo de programación diaria:

schedule:
  - cron: "0 6 * * *"

GitHub ejecuta el script todos los días a las 06:00 UTC, aproximadamente 07:00 en España.

También se puede ejecutar manualmente desde la pestaña Actions del repositorio.

🔐 Variables necesarias

El proyecto utiliza Secrets de GitHub para almacenar credenciales.

Debes configurar los siguientes secretos en:

Repository → Settings → Secrets → Actions

Variables necesarias:

NEWS_API_KEY
OPENAI_API_KEY
EMAIL_USER
EMAIL_PASS
EMAIL_TO
Descripción

NEWS_API_KEY

API Key de NewsAPI.

https://newsapi.org

OPENAI_API_KEY

API Key para utilizar IA para:

filtrado de relevancia

generación de resúmenes

EMAIL_USER

Correo desde el que se envía la newsletter.

EMAIL_PASS

Contraseña de aplicación del correo (por ejemplo Gmail App Password).

EMAIL_TO

Correo destinatario de la newsletter.

📂 Estructura del proyecto
daily-newsletter

script/
   newsletter.py

data/
   sent_urls.txt

.github/workflows/
   newsletter.yml
📜 Dependencias

El proyecto utiliza Python.

Principales librerías:

requests
openai
smtplib

En GitHub Actions se instalan con:

pip install requests openai==0.28
✉️ Ejemplo de email generado
☕ Buenos días

Aquí tienes tu resumen diario de noticias.

📌 Tecnología
- Apple prepara su iPhone plegable
  Actualidad iPhone
  Apple avanza en el desarrollo de su primer dispositivo plegable, que podría llegar en los próximos años con nuevas mejoras en diseño y pantalla.

📌 Bolsa
- Ana Botín compra acciones de Santander
  Europa Press
  La presidenta del banco ha adquirido acciones por valor cercano a tres millones de euros.
🚀 Posibles mejoras futuras

El proyecto puede evolucionar fácilmente hacia:

selección automática de las 15 noticias más importantes del día

ranking por relevancia

eliminación de duplicados por titular

generación de titular editorial

versión web de la newsletter

envío a múltiples suscriptores

dashboard de control

🧠 Objetivo del proyecto

Este proyecto demuestra cómo combinar:

agregación de información

automatización

inteligencia artificial

infraestructura cloud ligera

para construir un sistema de curación automática de contenido.
