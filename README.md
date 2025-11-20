# 🤖 AI-Buddy: Bot de Discord Potenciado por Llama 3.1 & LangChain

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-Orchestration-green)
![Groq](https://img.shields.io/badge/Groq-Llama%203.1-orange)
![Discord](https://img.shields.io/badge/Discord.py-Interface-purple)

Un asistente conversacional inteligente de baja latencia integrado en Discord. Este proyecto conecta la interfaz de usuario de Discord con el modelo **Llama 3.1** a través de la **LPU (Language Processing Unit) de Groq**, utilizando **LangChain** para la orquestación del flujo de datos.

El objetivo es demostrar una arquitectura de chat eficiente, modular y de coste cero para despliegue de LLMs.

## 🚀 Características

* **Inferencia de Alta Velocidad:** Uso de la API de Groq para respuestas casi instantáneas (Llama 3.1-8b-instant).
* **Arquitectura Modular:** Construido sobre LangChain, facilitando la futura integración de memoria (Chat History) o RAG.
* **Interactividad:** Feedback visual en Discord (estado "escribiendo...") para mejor UX.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python
* **Orquestación:** [LangChain](https://www.langchain.com/) (LCEL)
* **Modelo (LLM):** Llama 3.1 (vía [Groq Cloud](https://console.groq.com/))
* **Interfaz:** [Discord.py](https://discordpy.readthedocs.io/)
* **Gestión de Entorno:** Python-dotenv

## 🚀 Pruébalo Ahora

No necesitas instalar código para ver funcionar a **AI-Buddy**. Puedes invitar al bot directamente a tu servidor de Discord y empezar a chatear.

[![Invitar a Discord](https://img.shields.io/badge/Discord-Invitar%20AI--Buddy-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1441091789959336058)

### ¿Cómo usarlo?
1. Haz clic en el botón de arriba y autoriza al bot en tu servidor.
2. Ve a cualquier canal de texto al que el bot tenga acceso.
3. Escribe tu pregunta o comando.
   > **Ejemplo:** "Explícame qué es MapReduce en Big Data"
