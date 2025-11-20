# 🤖 AI-Buddy: Intelligent Discord Assistant

[![Discord](https://img.shields.io/badge/Discord-Invite_Bot-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/oauth2/authorize?client_id=1441091789959336058&permissions=67584&integration_type=0&scope=bot)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/Powered_by-Groq-orange?style=for-the-badge)](https://groq.com/)

**AI-Buddy** es un asistente conversacional de alto rendimiento para servidores de Discord. A diferencia de los bots tradicionales, utiliza la potencia de **Llama 3.3 70B** a través de la infraestructura LPU (Language Processing Unit) de **Groq** para ofrecer respuestas casi instantáneas con razonamiento complejo.

## 🔗 Añadir al Servidor

¿Quieres probar a AI-Buddy en tu propio servidor? Haz clic en el botón de abajo para invitarlo. Necesitarás permisos de administración en el servidor destino.

> [**➕ Invitar AI-Buddy a mi Servidor**](https://discord.com/oauth2/authorize?client_id=1441091789959336058&permissions=67584&integration_type=0&scope=bot)

---

## ⚙️ ¿Cómo funciona?

Este proyecto integra varias tecnologías punteras de IA y orquestación de datos:

1.  **Inferencia de Baja Latencia:** Utiliza la API de **Groq**, que acelera la inferencia de LLMs (Large Language Models) eliminando el cuello de botella de las GPUs tradicionales.
2.  **Gestión de Memoria con LangChain:** El bot no solo responde, sino que "recuerda". Implementa un sistema de historial que lee los últimos 10 mensajes del contexto para mantener el hilo de la conversación (simulando una memoria a corto plazo).

## 🚀 Características

- **⚡ Velocidad Extrema:** Respuestas generadas en milisegundos gracias a la arquitectura Llama-3 en Groq.
- **🧠 Contexto Conversacional:** Puedes hablar con él como con una persona; recuerda lo que dijiste en el mensaje anterior.
- **🛡️ Anti-Spam:** Solo se activa mediante mención (`@AI-Buddy`) o respondiendo (reply) a sus mensajes, manteniendo limpio el chat general.
- **🔧 Stack Técnico:** Python, Discord.py, LangChain Core & Groq API.

## 📖 Guía de Uso

Una vez el bot esté en tu servidor, la interacción es sencilla:

### 1. Iniciar conversación

Menciona al bot para hacerle una pregunta.

> **Usuario:** `@AI-Buddy Explícame la diferencia entre un decorador y un generador en Python.`

### 2. Continuar el hilo

No necesitas volver a mencionarlo. Simplemente usa la función de **"Responder"** (Reply) de Discord sobre el mensaje del bot. Él leerá el hilo y mantendrá el contexto.

---

_Este proyecto demuestra la implementación de agentes conversacionales modernos utilizando orquestadores de LLMs (LangChain) y hardware de inferencia de nueva generación._
