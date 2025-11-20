# 🤖 AI-Buddy: Hybrid AI Discord Assistant

[![Discord](https://img.shields.io/badge/Discord-Invite_Bot-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1441091789959336058&permissions=67584&integration_type=0&scope=bot)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Core-green?style=for-the-badge)](https://www.langchain.com/)
[![Groq](https://img.shields.io/badge/Powered_by-Groq-orange?style=for-the-badge)](https://groq.com/)
[![Gemini](https://img.shields.io/badge/Powered_by-Gemini-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white)](https://deepmind.google/technologies/gemini/)

**AI-Buddy** es un asistente conversacional avanzado y modular para Discord. A diferencia de los bots básicos, AI-Buddy utiliza una arquitectura híbrida basada en **LangChain** que permite alternar entre la velocidad extrema de **Llama 3.3 (vía Groq)** y la capacidad multimodal de **Gemini 2.5 Flash Preview (vía Google)**.

El proyecto implementa buenas prácticas de ingeniería de software (OOP), gestión de memoria conversacional y manejo robusto de errores de API.

## 🚀 Características Principales

- **⚡ Arquitectura Híbrida:**
  - **Modo Groq (LPU):** Inferencia casi instantánea para conversaciones fluidas usando Llama 3.
  - **Modo Gemini:** Capacidad de procesamiento robusta con gran ventana de contexto.
- **🧠 Memoria Contextual:** El bot "recuerda" el hilo de la conversación leyendo los últimos mensajes del canal, permitiendo interacciones naturales.
- **🛡️ Smart Activation:** Solo responde a menciones (`@AI-Buddy`) o respuestas directas (Replies), evitando el spam en el chat general.
- **🔧 Sistema Modular:** Código estructurado en clases (`BaseModel`, `GroqModel`, `GeminiModel`) para facilitar la escalabilidad.
- **📄 Paginación Automática:** Maneja respuestas largas dividiéndolas inteligentemente para respetar el límite de 2000 caracteres de Discord.

---

## 🛠️ Instalación y Despliegue

Sigue estos pasos para ejecutar tu propia instancia del bot en local.

### 1. Prerrequisitos
- Python 3.10 o superior.
- Una cuenta y token de Bot en [Discord Developer Portal](https://discord.com/developers/applications).
- API Keys de [GroqConsole](https://console.groq.com/) y/o [Google AI Studio](https://aistudio.google.com/).

### 2. Clonar el repositorio
```bash
git clone https://github.com/Pedrogf03/AI-Buddy-Bot-for-Discord
cd AI-Buddy-Bot-for-Discord
```

### 3. Configurar el Entorno Virtual
Es altamente recomendable usar un entorno virtual para aislar las dependencias.

```Bash
# En Windows
python -m venv venv
.\venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependencias
```Bash
pip install -r requirements.txt
```
### 5. Configuración de Variables (.env)
Crea un archivo llamado .env en la raíz del proyecto y pega tus credenciales:

```bash
DISCORD_TOKEN=tu_token_de_discord_aqui
GROQ_API_KEY=tu_api_key_de_groq_aqui
GOOGLE_API_KEY=tu_api_key_de_google_aqui
```
### 6. Ejecutar el Bot
Por defecto, el bot iniciará usando Groq. Puedes cambiar el proveedor en main.py.

```Bash
python main.py
```

## ⚙️ Estructura del Proyecto
```Plaintext
AI-Buddy-Bot/
├── models/               # Lógica de los LLMs (Patrón Strategy)
│   ├── base_model.py     # Clase abstracta para estandarizar modelos
│   ├── groq_model.py     # Implementación de Llama 3.3
│   └── gemini_model.py   # Implementación de Google Gemini
├── utils/
│   ├── prompt_manager.py # Gestor de System Prompts y limpieza de texto
├── discord_bot.py        # Lógica del cliente de Discord y eventos
├── main.py               # Punto de entrada y carga de entorno
└── requirements.txt      # Dependencias del proyecto
```

## 📖 Guía de Uso
Una vez el bot esté en línea:

- Iniciar una charla: Menciona al bot para hacer una pregunta.

    ```Usuario: @AI-Buddy ¿Cuál es la diferencia entre async y sync en Python?```

- Continuar la charla: Usa la función "Responder" (Reply) de Discord sobre el mensaje del bot. No hace falta volver a mencionarlo; él leerá el contexto.

- Personalidad: Puedes modificar el archivo utils/prompt_manager.py para cambiar cómo se comporta el bot.

_Desarrollado con ❤️, Python y LangChain._