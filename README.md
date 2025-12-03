# 🤖 AI-Buddy v2.0

![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/AI-Groq_Llama3-orange?logo=meta&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

> Un bot de Discord modular "Todo en Uno": Investiga, analiza videos, genera imágenes y entretiene.

[![Invitar al Bot](https://img.shields.io/badge/Discord-Invitar_al_Servidor-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1441091789959336058&permissions=67712&integration_type=0&scope=bot+applications.commands)

---

## 📖 Descripción

**AI-Buddy v2.0** es la evolución completa del asistente. Abandonando los chats pasivos, ahora funciona mediante **Slash Commands (`/`)** para ofrecer herramientas precisas de productividad y entretenimiento.

Utiliza la potencia de **Llama 3 (vía Groq)** para el razonamiento, **DuckDuckGo** para la investigación y varias APIs especializadas para el manejo de multimedia, todo sin requerir claves API costosas para las funciones extra.

## ✨ Características Principales

- **⚡ Velocidad Extrema:** Respuestas casi instantáneas gracias a la infraestructura de Groq.
- **📺 Analista de YouTube:** Resume videos enteros, extrae puntos clave y conclusiones sin que tengas que verlos (`/resumen_yt`).
- **🌍 Lector Web:** Entra en páginas web, lee el contenido y te genera resúmenes ejecutivos (`/analizar_web`).
- **🎨 Generación de Imágenes:** Crea arte visual al instante usando IA generativa (`/imagine`).
- **🧠 Entretenimiento Inteligente:** Desde debates filosóficos contra la IA hasta "Roasts" personalizados para tus amigos.
- **🛡️ Privacidad:** Sin bases de datos. Todo es efímero y se procesa en RAM.

## 🎮 Comandos Disponibles

Escribe `/` en el chat para ver el menú.

### 🛠️ Utilidad e Investigación

| Comando              | Descripción                                                           |
| :------------------- | :-------------------------------------------------------------------- |
| `/search [consulta]` | Busca en internet en tiempo real y resume la información con fuentes. |
| `/codigo [leng]`     | Genera snippets de programación explicados.                           |
| `/traducir`          | Traduce textos complejos a cualquier idioma.                          |

### 🎭 Diversión y Multimedia

| Comando             | Descripción                                                              |
| :------------------ | :----------------------------------------------------------------------- |
| `/imagine [prompt]` | Genera una imagen basada en tu descripción (vía Pollinations).           |
| `/debate [tema]`    | Inicia un debate donde la IA adopta la postura contraria a la tuya.      |
| `/roast [@usuario]` | Genera una burla graciosa e ingeniosa hacia un miembro del servidor.     |
| `/joke [tema]`      | Cuenta un chiste sobre el tema que elijas.                               |
| `/eli5 [tema]`      | _"Explain Like I'm 5"_. Explica conceptos difíciles de forma muy simple. |

## 📂 Estructura del Proyecto

El bot utiliza una arquitectura de **Cogs** (extensiones) para mantener el código limpio:

```text
ai-buddy/
├── cogs/
│   ├── general.py      # Diversión: roast, debate, joke, eli5
│   ├── media.py        # Multimedia: YouTube, Web Scraping, Imágenes
│   ├── research.py     # Búsqueda: DuckDuckGo
│   ├── utility.py      # Herramientas: Traductor, Código
│   └── help.py         # Sistema de ayuda automático
├── services/           # Lógica de conexión con Groq (LLM)
├── utils/              # Herramientas de búsqueda web
├── main.py             # Arranque y carga de módulos
└── Dockerfile          # Configuración de despliegue
```

## 🚀 Instalación y Despliegue

### Requisitos

Necesitas las siguientes claves en un archivo `.env`:

```env
DISCORD_TOKEN=tu_token_aqui
GROQ_API_KEY=tu_api_key_de_groq
# No se necesitan claves para YouTube ni Imágenes
```

### Opción A: Docker (Recomendado)

1.  **Clonar el repo:**
    ```bash
    git clone [https://github.com/Pedrogf03/AI-Buddy-Bot-for-Discord](https://github.com/Pedrogf03/AI-Buddy-Bot-for-Discord)
    cd AI-Buddy-Bot-for-Discord
    ```
2.  **Construir y Correr:**
    ```bash
    docker build -t ai-buddy .
    docker run -d --env-file .env --name ai-buddy ai-buddy
    ```

### Opción B: Local (Python)

1.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

    _(Asegúrate de que tu `requirements.txt` incluye: `discord.py`, `langchain-groq`, `duckduckgo-search`, `youtube-transcript-api`, `beautifulsoup4`, `requests`)_.

2.  **Ejecutar:**

    ```bash
    python main.py
    ```

## 🛠️ Stack Tecnológico

- **Core:** Python 3.10+, Discord.py
- **IA:** Groq Cloud (Llama-3.3-70b)
- **Web/Media:** DuckDuckGo Search, YouTube Transcript API, BeautifulSoup4.
- **Imágenes:** Pollinations.ai API.

## ⚖️ Legal y Privacidad

El uso de este bot implica la aceptación de nuestras políticas.

- **Privacidad:** No guardamos logs, mensajes ni datos de usuarios. El análisis de webs y videos se realiza en tiempo real y no se almacena.
- **Responsabilidad:** El desarrollador no se hace responsable del contenido generado por la IA o de las imágenes creadas.

---

Desarrollado por [Pedrogf03](https://www.google.com/search?q=https://github.com/Pedrogf03) 🖤
