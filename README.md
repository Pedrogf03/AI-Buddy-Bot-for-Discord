# 🤖 AI-Buddy v2.0

![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Groq](https://img.shields.io/badge/AI-Groq_Llama3-orange?logo=meta&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

[![Invitar al Bot](https://img.shields.io/badge/Discord-Invitar_al_Servidor-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1441091789959336058&permissions=67712&integration_type=0&scope=bot+applications.commands)

---

## 📖 Descripción

**AI-Buddy v2.0** es la evolución completa del asistente. Abandonando los chats pasivos, ahora funciona mediante **Slash Commands (`/`)** para ofrecer herramientas precisas de productividad, moderación y entretenimiento.

Utiliza la potencia de **Llama 3 (vía Groq)** para el razonamiento, **DuckDuckGo** para la investigación y varias APIs especializadas.

## ✨ Características Principales

- **⚡ Velocidad Extrema:** Respuestas casi instantáneas gracias a la infraestructura de Groq.
- **🎲 Juegos de Rol Infinitos:** Un Dungeon Master IA (`/rpg`) que narra aventuras interactivas donde tú tomas las decisiones.
- **🎨 Arte y Diversión:** Generación de imágenes, tests de compatibilidad y debates contra la IA.

## 🎮 Comandos Disponibles

Escribe `/` en el chat para ver el menú interactivo.

### 🧠 IA y Utilidad General
| Comando | Descripción |
| :--- | :--- |
| `/ask [pregunta]` | Conversa directamente con la IA sobre cualquier tema. |
| `/eli5 [tema]` | *"Explain Like I'm 5"*. Explica conceptos difíciles de forma muy simple. |
| `/search [consulta]` | Busca en internet en tiempo real y resume la información con fuentes. |

### 🎭 Juegos y Entretenimiento
| Comando | Descripción |
| :--- | :--- |
| `/rpg [escenario]` | Inicia una aventura de rol textual infinita. ¡Tú eliges el mundo! |
| `/ship [u1] [u2]` | Calcula la compatibilidad amorosa entre dos usuarios (con opinión de la IA). |
| `/imagine [prompt]` | Genera una imagen basada en tu descripción (vía Pollinations). |
| `/debate [tema]` | Inicia un debate interactivo donde la IA adopta la postura contraria a la tuya. |
| `/roast [@usuario]` | Genera una burla graciosa e ingeniosa hacia un miembro del servidor. |
| `/joke [tema]` | Cuenta un chiste sobre el tema que elijas. |

### 🛠️ Herramientas y Moderación
| Comando | Descripción |
| :--- | :--- |
| `/voice_kicks` | Muestra un ranking (Top 10) de usuarios que más han desconectado a otros de la voz. |
| `/code [leng]` | Genera snippets de programación explicados. |
| `/code_review [leng] [código]` | Analiza el código y da una versión mejorada. |

## 📂 Estructura del Proyecto

El bot utiliza una arquitectura modular basada en **Cogs**:

```text
ai-buddy/
├── cogs/               # Lógica de comandos
├── services/           # Lógica de conexión con Groq (LLM)
├── utils/              # Funciones auxiliares (split_text, search)
├── main.py             # Arranque y carga de módulos
└── Dockerfile          # Configuración de despliegue
````

## 🚀 Instalación y Despliegue

### Requisitos

Necesitas las siguientes claves en un archivo `.env`:

```env
DISCORD_TOKEN=tu_token_aqui
GROQ_API_KEY=tu_api_key_de_groq
```

### Opción A: Docker (Recomendado)

1.  **Clonar el repo:**
    ```bash
    git clone https://github.com/Pedrogf03/AI-Buddy-Bot-for-Discord
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

2.  **Ejecutar:**

    ```bash
    python main.py
    ```

## 🛠️ Stack Tecnológico

  - **Core:** Python 3.10+, Discord.py
  - **IA:** Groq Cloud (Llama-3.3-70b)
  - **Web:** DuckDuckGo Search.
  - **Imágenes:** Pollinations.ai API.

## ⚖️ Legal y Privacidad

El uso de este bot implica la aceptación de nuestras políticas.

  - [Política de Privacidad](PRIVACY.md)
  - [Términos y Condiciones](https://www.google.com/search?q=TERMS.md)

-----

Desarrollado por [Pedrogf03](https://github.com/Pedrogf03) 🖤