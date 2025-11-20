import os
import discord
import re
from dotenv import load_dotenv

# Importaciones de LangChain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Cargar variables de entorno
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configuración de la IA
llm = ChatGroq(
    temperature=0.7,
    model_name="llama-3.1-8b-instant", # <-- Modelo de Groq
    api_key=GROQ_API_KEY
)

# Prompt del Sistema
system_prompt = """
Eres AI-Buddy, un asistente de inteligencia artificial avanzado, útil y amable.
Tu objetivo es proporcionar información precisa, clara y concisa a los usuarios en un servidor de Discord.

DIRECTRICES DE COMPORTAMIENTO:
1.  **Tono:** Mantén un tono profesional pero cercano y conversacional.
2.  **Idioma:** Responde siempre en el mismo idioma en el que te habla el usuario (principalmente Español, pero adáptate).
3.  **Formato:** Aprovecha al máximo el formato Markdown de Discord:
    * Usa **negrita** para conceptos clave.
    * Usa `código en línea` para términos técnicos o comandos.
    * Usa bloques de código (```) para scripts o programación, especificando el lenguaje.
    * Usa listas (viñetas) para organizar la información.
4.  **Concisión:** Recuerda que estás en un chat. Evita muros de texto enormes a menos que te pidan una explicación detallada. Ve al grano.
5.  **Conocimiento:** Si no sabes algo, admítelo honestamente. No inventes información.
6.  **Código:** Si te piden código, explícalo brevemente antes o después del bloque.
7.  **Longitud:** Discord tiene un límite estricto de 2000 caracteres por mensaje.
    * Intenta que tus respuestas sean breves.
    * Si vas a generar un código muy largo, divídelo o resume la explicación.
    * Nunca rellenes con texto innecesario.
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{text}")
])

# Prompt -> Modelo -> Parser
chain = prompt | llm | StrOutputParser()

# Configuración de Discord
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Eventos del Bot
@client.event
async def on_ready():
    print(f'✅ Bot conectado y listo como: {client.user}')

# Evento de Mensaje
@client.event
async def on_message(message):
    # Evitar que el bot se hable a sí mismo
    if message.author == client.user:
        return

    # Ignorar mensajes que no mencionan al bot
    if client.user not in message.mentions:
        return

    # Limpiar el prompt
    prompt_limpio = re.sub(f'<@!?{client.user.id}>', '', message.content).strip()

    try:
        async with message.channel.typing():
            # 1. Obtenee la respuesta completa de la IA
            respuesta_completa = chain.invoke({"text": prompt_limpio})
            
            # 2. Lógica de fragmentación (Chunking) para Discord (Límite 2000)
            if len(respuesta_completa) > 2000:
                for i in range(0, len(respuesta_completa), 1900):
                    chunk = respuesta_completa[i:i+1900]
                    await message.channel.send(chunk)
            else:
                # Si es corto, se envía normal
                await message.channel.send(respuesta_completa)

    except Exception as e:
        print(f"❌ Error: {e}")
        await message.channel.send("Ocurrió un error procesando tu solicitud.")

# Arrancar el motor
if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)
else:
    print("❌ Error: No se encontró el token de Discord en el archivo .env")