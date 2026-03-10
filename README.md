# 📰 AI Daily Newsletter

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Automation](https://img.shields.io/badge/Automation-GitHub%20Actions-black)
![AI](https://img.shields.io/badge/AI-OpenAI-green)
![NewsAPI](https://img.shields.io/badge/Data-NewsAPI-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

Sistema automatizado que **recopila, filtra y envía una newsletter diaria personalizada** utilizando **inteligencia artificial y automatización en la nube**.

Cada mañana recibirás un email con **las noticias más relevantes del día**, resumidas por IA y seleccionadas según tus intereses.

---

# 🚀 Qué hace este proyecto

El sistema:

1. Busca noticias recientes en internet
2. Filtra las noticias realmente relevantes con IA
3. Elimina duplicados de días anteriores
4. Genera un resumen corto de cada noticia
5. Construye una newsletter clara y rápida de leer
6. Envía automáticamente el email
7. Guarda las noticias enviadas para evitar repetirlas

Todo esto se ejecuta **automáticamente cada día** mediante **GitHub Actions**.

---

# 🧠 Temas de noticias

La IA prioriza noticias relacionadas con:

- 🏢 Real Estate en España  
- 📈 Bolsa y mercados financieros  
- 🧠 Inteligencia Artificial  
- 💻 Tecnología  
- 🚀 Innovación empresarial  
- ⚽ Fútbol  
- 🎾 Pádel  
- 🏛️ Política española  
- 🚨 Sucesos en España  
- 📍 Sucesos en Valencia  

La IA selecciona **las 15 noticias más relevantes del día**.

---

# ⚙️ Arquitectura del sistema

El flujo del sistema es el siguiente:

```
NewsAPI
   │
   ▼
Recopilación de noticias
   │
   ▼
Filtro IA (relevancia)
   │
   ▼
Eliminación de duplicados
   │
   ▼
Generación de resumen con IA
   │
   ▼
Construcción del email
   │
   ▼
Envío por SMTP
   │
   ▼
Guardado de URLs enviadas
```

---

# 🔎 Cómo funciona paso a paso

## 1️⃣ Recopilación de noticias

El script consulta **NewsAPI** para obtener artículos recientes sobre los temas definidos.

---

## 2️⃣ Eliminación de duplicados

El sistema guarda las URLs enviadas en:

```
data/sent_urls.txt
```

Antes de enviar una noticia, comprueba si ya fue enviada anteriormente.

Si la URL ya existe en el archivo:

```
la noticia se descarta automáticamente
```

---

## 3️⃣ Selección inteligente con IA

Cada noticia se analiza con IA para decidir si es **realmente relevante**.

La IA responde únicamente:

```
SI
NO
```

Solo las noticias con **SI** pasan al siguiente paso.

---

## 4️⃣ Generación del resumen

La IA genera un resumen breve de **2-3 líneas**, optimizado para lectura rápida.

---

## 5️⃣ Construcción de la newsletter

El sistema genera un email con este formato:

```
☕ Buenos días

Aquí tienes tu resumen diario de noticias.

📌 Tecnología
- Apple prepara su iPhone plegable
  Actualidad iPhone
  Apple avanza en el desarrollo de su primer dispositivo plegable con mejoras en diseño y pantalla.

📌 Bolsa
- Ana Botín compra acciones de Santander
  Europa Press
  La presidenta del banco ha adquirido acciones por valor cercano a tres millones de euros.
```

---

## 6️⃣ Envío automático por email

El email se envía mediante **SMTP utilizando Gmail**.

---

## 7️⃣ Guardado de noticias enviadas

Después de enviar la newsletter:

1. se actualiza `sent_urls.txt`
2. se hace commit automático
3. se sube el archivo al repositorio

Esto permite **recordar qué noticias ya se enviaron**.

---

# 🕒 Automatización diaria

La ejecución automática se realiza con **GitHub Actions**.

Ejemplo del cron job:

```yaml
schedule:
  - cron: "0 6 * * *"
```

GitHub ejecuta el script todos los días a las:

```
06:00 UTC
≈ 07:00 en España
```

También se puede ejecutar manualmente desde:

```
GitHub → Actions → Run workflow
```

---

# 🔐 Variables necesarias

Debes configurar estos **Secrets en GitHub**:

```
Repository → Settings → Secrets → Actions
```

Variables necesarias:

```
NEWS_API_KEY
OPENAI_API_KEY
EMAIL_USER
EMAIL_PASS
EMAIL_TO
```

---

# 📄 Descripción de variables

### NEWS_API_KEY

API de noticias utilizada para recopilar artículos.

https://newsapi.org

---

### OPENAI_API_KEY

Se utiliza para:

- filtrar noticias relevantes
- generar resúmenes automáticos

---

### EMAIL_USER

Correo desde el que se envía la newsletter.

---

### EMAIL_PASS

Contraseña de aplicación del correo (por ejemplo **Gmail App Password**).

---

### EMAIL_TO

Correo destinatario de la newsletter.

---

# 📂 Estructura del proyecto

```
daily-newsletter

script/
   newsletter.py

data/
   sent_urls.txt

.github/workflows/
   newsletter.yml
```

---

# 📜 Dependencias

El proyecto utiliza **Python**.

Librerías principales:

```
requests
openai
smtplib
```

En GitHub Actions se instalan con:

```
pip install requests openai==0.28
```

---

# 📬 Ejemplo de newsletter

```
☕ Buenos días

Aquí tienes tu resumen diario de noticias.

📌 Inteligencia Artificial
- OpenAI lanza nuevas herramientas para empresas
  TechCrunch
  La compañía presenta nuevas capacidades orientadas a empresas para integrar modelos de IA en procesos corporativos.

📌 Real Estate
- El mercado inmobiliario en España sigue creciendo
  El Economista
  La demanda de vivienda continúa aumentando impulsada por la inversión extranjera y la escasez de oferta.
```

---

# 🔮 Posibles mejoras futuras

Este proyecto puede evolucionar hacia:

- 📊 ranking automático de noticias por importancia  
- 🌐 versión web de la newsletter  
- 👥 envío a múltiples suscriptores  
- 📱 app móvil  
- 📈 dashboard de métricas  
- 🧠 análisis de tendencias  

---

# 🧠 Objetivo del proyecto

Este proyecto demuestra cómo combinar:

- agregación de información
- inteligencia artificial
- automatización
- infraestructura cloud ligera

para construir un **sistema automático de curación de noticias** que entrega **información relevante cada mañana** sin intervención manual.

---

⭐ Si te gusta el proyecto, puedes mejorarlo añadiendo más fuentes, más categorías o creando una versión pública de la newsletter.
