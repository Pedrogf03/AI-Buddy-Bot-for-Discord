import os
import discord
from models.groq_model import GroqModel
from models.gemini_model import GeminiModel
from utils.prompt_manager import PromptManager

class DiscordBot:
    def __init__(self, model_provider="groq"):
        self.token = os.getenv("DISCORD_TOKEN")
        self.model_provider = model_provider.lower()
        self.prompt_manager = PromptManager()
        
        # 1. Inicializar Modelo
        print(f"⚙️ Cargando modelo: {self.model_provider}...")
        self.model = self._setup_model()
        
        # 2. Inicializar Cliente de Discord
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        
        # 3. Registrar Eventos
        self._register_events()

    def _setup_model(self):
        if self.model_provider == "groq":
            return GroqModel()
        elif self.model_provider == "gemini":
            return GeminiModel()
        else:
            raise ValueError(f"Proveedor no soportado: {self.model_provider}")

    def _register_events(self):
        """Registra los eventos de Discord manualmente"""
            
        @self.client.event
        async def on_ready():
            print(f'✅ Bot conectado como: {self.client.user}')
            print(f'✅ Modelo activo: {self.model_provider.upper()}')

            activity = discord.Activity(
                type=discord.ActivityType.watching,
                name="pedrogf03.github.io"
            )

            await self.client.change_presence(
                status=discord.Status.online,
                activity=activity
            )

        @self.client.event
        async def on_message(message):
            await self._handle_message(message)

    async def _handle_message(self, message):
        # Ignorar mensajes del propio bot
        if message.author == self.client.user:
            return

        # Lógica de mención
        is_mentioned = self.client.user in message.mentions
        is_reply = (message.reference and message.reference.resolved and 
                    message.reference.resolved.author == self.client.user)

        # Lógica de mensaje privado (DM)
        is_dm = isinstance(message.channel, discord.DMChannel)

        # Si NO es mención, NI respuesta, NI mensaje privado, ignorar.
        if not (is_mentioned or is_reply or is_dm):
            return

        try:
            async with message.channel.typing():
                # 1. Obtener historial
                history_messages = []
                async for msg in message.channel.history(limit=5, before=message):
                    if msg.content:
                        author = "Assistant" if msg.author == self.client.user else "User"
                        history_messages.append(f"{author}: {msg.content}")
                
                history_str = "\n".join(reversed(history_messages))

                # 2. Preparar prompt
                prompt_limpio = self.prompt_manager.clean_message_content(
                    message.content, self.client.user.id
                )
                system_instruction = self.prompt_manager.get_system_prompt()

                # 3. Generar respuesta
                respuesta = await self.model.generate_response(
                    system_instruction=system_instruction,
                    chat_history=history_str,
                    text=prompt_limpio
                )

                # 4. Enviar (con paginación simple)
                if len(respuesta) > 4000:
                    await message.channel.send("😢 No he podido generar una respuesta adecuada.")
                elif len(respuesta) > 2000:
                    for i in range(0, len(respuesta), 1900):
                        await message.channel.send(respuesta[i:i+1900])
                else:
                    await message.channel.send(respuesta)

        except Exception as e:
            await self._handle_error(message, e)

    async def _handle_error(self, message, error):
        print(f"❌ Error: {error}")
        msg = None
        if hasattr(self.model, 'handle_error'):
            msg = self.model.handle_error(error)
        
        if not msg:
            msg = f"🤖 Ocurrió un error interno: {str(error)[:50]}..."
            
        await message.channel.send(msg)

    def run(self):
        if not self.token:
            raise ValueError("❌ Token de Discord no encontrado en .env")
        self.client.run(self.token)