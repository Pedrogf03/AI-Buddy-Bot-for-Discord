import os
import discord
import re
from datetime import datetime
import pytz 
from dotenv import load_dotenv

# Importaciones de LangChain
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from groq import RateLimitError, APIError

# Cargar variables de entorno
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- CONFIGURACIÓN DEL MODELO ---
llm = ChatGroq(
    temperature=0.7,
    model_name="llama-3.3-70b-versatile", 
    api_key=GROQ_API_KEY,
    max_retries=2 # Reintentar automáticamente 2 veces si falla la conexión
)

# --- PROMPTS ---
def get_system_prompt():
    tz_spain = pytz.timezone('Europe/Madrid')
    now = datetime.now(tz_spain).strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""
    Eres AI-Buddy, una IA todoterreno, inteligente y amigable.
    
    CONTEXTO:
    - Ubicación: España. Hora: {now}.
    
    PERSONALIDAD:
    - Eres un colega digital: simpático, servicial y claro.
    - Sabes de programación, recetas baratas (déficit calórico) y cultura general.
    - No seas pedante. Si explicas código, sé breve y eficaz.
    
    IMPORTANTE:
    - Usa Markdown de Discord.
    - Si te preguntan algo peligroso o ilegal, rechaza amablemente.
    """

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "{system_instruction}"),
    ("user", "Historial previo:\n{chat_history}\n\nUsuario actual: {text}")
])

chain = prompt_template | llm | StrOutputParser()

# --- DISCORD SETUP ---
intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot conectado como: {client.user}')
    print('✅ Modo: Gratuito (Groq Llama 3.3)')

@client.event
async def on_message(message):
    if message.author == client.user: return

    # Detectar mención o respuesta
    is_mentioned = client.user in message.mentions
    is_reply_to_bot = (message.reference and message.reference.resolved and message.reference.resolved.author == client.user)

    if not (is_mentioned or is_reply_to_bot):
        return

    try:
        async with message.channel.typing():
            # --- 1. GESTIÓN DE MEMORIA ---
            history_messages = []
            async for msg in message.channel.history(limit=10, before=message):
                if not msg.content: continue
                author_name = "AI-Buddy" if msg.author == client.user else msg.author.display_name
                clean_content = re.sub(f'<@!?{client.user.id}>', '', msg.content).strip()
                history_messages.append(f"{author_name}: {clean_content}")
            
            history_str = "\n".join(reversed(history_messages))

            # --- 2. GENERACIÓN DE RESPUESTA ---
            prompt_limpio = re.sub(f'<@!?{client.user.id}>', '', message.content).strip()
            system_instruction = get_system_prompt()
            
            respuesta_completa = await chain.ainvoke({
                "system_instruction": system_instruction,
                "chat_history": history_str,
                "text": prompt_limpio
            })

            # --- 3. ENVÍO ---
            if len(respuesta_completa) > 2000:
                for i in range(0, len(respuesta_completa), 1900):
                    await message.channel.send(respuesta_completa[i:i+1900])
            else:
                await message.channel.send(respuesta_completa)

    # --- 4. CONTROL DE ERRORES (ANTI-SORPRESAS) ---
    except RateLimitError:
        # Error por demasiado uso de la API gratuita
        print("⚠️ Límite de velocidad alcanzado (Rate Limit).")
        await message.channel.send("🥵 Uff, estoy echando humo (mucha gente hablándome a la vez). Dame un minuto para enfriar mis circuitos.")
    
    except APIError as e:
        # Error genérico de la API (servidores caídos, etc.)
        print(f"⚠️ Error de API Groq: {e}")
        await message.channel.send("🔌 Se me ha ido la conexión con el cerebro central. Inténtalo de nuevo en un rato.")

    except Exception as e:
        print(f"❌ Error desconocido: {e}")
        await message.channel.send("Algo ha salido mal internamente. ¿Puedes repetir?")

if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)