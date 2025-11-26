# 🤖 AI-Buddy

![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Privacy](https://img.shields.io/badge/Privacy-Ephemeral-orange)
![License](https://img.shields.io/badge/License-MIT-green)

> Un bot de Discord potenciado por IA, diseñado para ser desplegado fácilmente con Docker y respetando la privacidad del usuario.

[![Invitar al Bot](https://img.shields.io/badge/Discord-Invitar_al_Servidor-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1441091789959336058&permissions=67584&integration_type=0&scope=bot)

---

## 📖 Descripción

**AI-Buddy** es una integración inteligente para Discord que utiliza un modelo de IA de Groq o Gemini para conversar con los usuarios de forma natural. Solo añádelo a tu servidor y comienza a conversar. Puedes mencionar al bot en cualquier canal para que responda o hablarle en privado sin necesidad de mencionarlo.

El proyecto está diseñado bajo la filosofía **"Privacy First"** y la simplicidad de despliegue. Todo el entorno está contenerizado con Docker, lo que permite ponerlo en marcha en cualquier servidor en cuestión de segundos.

## ✨ Características

- **🐳 Dockerizado:** Listo para desplegar sin preocuparse por dependencias de Python o versiones del sistema operativo.
- **🧠 Contexto Efímero:** Mantiene una "memoria corta" de los últimos 10 mensajes para mantener el hilo de la conversación.
- **🔒 Privacidad Total:** No utiliza bases de datos. La información se procesa en memoria volátil y se descarta inmediatamente después de responder.
- **⚡ Respuesta a Eventos:** Sistema robusto de escucha de mensajes optimizado para evitar latencia.
- **👀 Buscar en Internet:** Si le pides al bot que busque información en internet, podrá hacerlo utilizando la herramienta de DuckDuckGo Search.

## 🚀 Despliegue Rápido (Docker)

Para ejecutar este bot, solo necesitas tener [Docker](https://www.docker.com/) instalado.

### 1. Clonar y Configurar

Descarga el repositorio y configura las variables de entorno.

```bash
git clone https://github.com/Pedrogf03/AI-Buddy-Bot-for-Discord
cd AI-Buddy-Bot-for-Discord
```

Crea un archivo `.env` en la raíz (puedes copiar el ejemplo):

```# Archivo .env
DISCORD_TOKEN=pega_aqui_tu_token_de_discord
GROQ_API_KEY=pega_aqui_tu_api_key
GOOGLE_API_KEY=pega_aqui_tu_api_key
```

### 2. Construir y Lanzar

Una vez configurado el `.env`, simplemente lanza el contenedor:

```
docker-compose up -d --build
```

¡Listo! El bot debería estar online. Puedes ver los logs con `docker logs -f ai-buddy`.

## 🛠️ Tecnologías

- **Lenguaje**: Python

- **Contenerización**: Docker

- **Librerías**:

  - discord.py
  - python-dotenv
  - pytz
  - langchain-groq
  - langchain-google-genai
  - google-generativeai>=0.8.3
  - duckduckgo-search
  - langchain
  - langchain-community
  - ddgs

- **Modelos IA**:
  - gemini-2.5-flash-lite
  - llama-3.3-70b-versatile

## ⚖️ Legal

El uso de este bot implica la aceptación de nuestras políticas, diseñadas para proteger tu privacidad al no almacenar datos persistentemente.

- [Términos de Servicio](TERMS.md)
- [Política de Privacidad](PRIVACY.md)

---

![Views](https://visitor-badge.laobi.icu/badge?page_id=Pedrogf03.Ai-Buddy-Bot-for-Discord&left_text=Views)

Desarrollado por Pedrogf03 🖤
