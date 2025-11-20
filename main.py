import os
import discord
from dotenv import load_dotenv

# Importaciones de LangChain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Cargar variables de entorno
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 2. Configuración de la IA (Cerebro)
llm = ChatGroq(
    temperature=0.7,
    model_name="llama-3.1-8b-instant", 
    api_key=GROQ_API_KEY
)

# El Prompt del Sistema define la personalidad
system_prompt = "Eres un asistente experto en programación y Big Data. Respondes de forma concisa y útil en español."

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{text}")
])

#Prompt -> Modelo -> Parser (limpia la salida a texto)
chain = prompt | llm | StrOutputParser()

# 3. Configuración de Discord (Cuerpo)
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot conectado y listo como: {client.user}')

@client.event
async def on_message(message):
    # Evitar que el bot se hable a sí mismo
    if message.author == client.user:
        return

    print(f"Usuario: {message.content}")

    try:
        # Activamos el estado "Escribiendo..." en Discord para dar feedback visual
        async with message.channel.typing():
            
            # Enviamos el mensaje a la IA
            respuesta_ia = chain.invoke({"text": message.content})
            
            # Enviamos la respuesta a Discord
            await message.channel.send(respuesta_ia)

    except Exception as e:
        print(f"❌ Error: {e}")
        await message.channel.send("Ups, mi cerebro de IA ha tenido un fallo temporal.")

# 4. Arrancar el motor
if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)
else:
    print("❌ Error: No se encontró el token de Discord en el archivo .env")