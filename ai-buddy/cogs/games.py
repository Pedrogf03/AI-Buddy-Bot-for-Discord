import discord
from discord.ext import commands
from discord import app_commands
from services.ai_service import GroqService
from utils.split_text import split_text
import asyncio
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai = GroqService()

    # /rpg
    @app_commands.command(name="rpg", description="Inicia una aventura de rol textual infinita")
    @app_commands.describe(escenario="Dónde ocurre la historia (Ej: Nave espacial, Castillo, Mercadona en apocalipsis)")
    async def rpg(self, interaction: discord.Interaction, escenario: str):
        await interaction.response.defer()

        system = (
            "Eres un Dungeon Master de un juego de rol de texto. "
            "Tu trabajo es narrar una historia inmersiva, corta y emocionante en segunda persona ('Ves', 'Haces'). "
            "Al final de cada mensaje, ofrece 3 opciones numéricas claras para que el jugador elija qué hacer. "
            "Gestiona un inventario simple. Si el jugador muere, di 'FIN DEL JUEGO'. "
            "Usa Español de España y formato Markdown."
        )

        historial = f"ESCENARIO ELEGIDO: {escenario}. Comienza la aventura describiendo dónde estoy y qué llevo puesto."

        narracion = await self.ai.generate_response(system, historial)
        historial += f"\n\nDM: {narracion}"

        fragmentos = split_text(f"🎲 **AVENTURA: {escenario.upper()}**\n\n{narracion}")
        
        ultimo_msg = None
        for i, frag in enumerate(fragmentos):
            if i == len(fragmentos) - 1:
                frag += "\n\n*(Responde a este mensaje con tu acción o el número de opción. Escribe 'fin' para salir)*"
            
            if i == 0:
                ultimo_msg = await interaction.followup.send(frag)
            else:
                ultimo_msg = await interaction.channel.send(frag)

        def check(m):
            if m.author != interaction.user or m.channel != interaction.channel:
                return False
            if m.reference is None:
                return False
            return m.reference.message_id == ultimo_msg.id

        while True:
            try:
                mensaje_usuario = await self.bot.wait_for('message', check=check, timeout=600.0)
                content = mensaje_usuario.content.lower()

                if content in ["fin", "salir", "morir"]:
                    await mensaje_usuario.reply("💀 Has abandonado la partida.")
                    break

                async with interaction.channel.typing():
                    historial += f"\n\nJUGADOR: {mensaje_usuario.content}"
                    
                    prompt_turno = f"{historial}\n\nInstrucción: Continúa la historia. Ofrece nuevas opciones."
                    
                    narracion = await self.ai.generate_response(system, prompt_turno)
                    historial += f"\n\nDM: {narracion}"

                fragmentos = split_text(narracion)
                
                for i, frag in enumerate(fragmentos):
                    if i == 0:
                        ultimo_msg = await mensaje_usuario.reply(frag)
                    else:
                        ultimo_msg = await interaction.channel.send(frag)

                if "FIN DEL JUEGO" in narracion:
                    break

            except asyncio.TimeoutError:
                await interaction.followup.send(f"💤 {interaction.user.mention}, te has quedado dormido en la aventura. Fin.")
                break
            except Exception as e:
                await interaction.followup.send(f"⚠️ Error en el RPG: {e}")
                break

    # /ship
    @app_commands.command(name="ship", description="Calcula la compatibilidad amorosa entre dos usuarios")
    async def ship(self, interaction: discord.Interaction, usuario1: discord.Member, usuario2: discord.Member):
        await interaction.response.defer()

        seed = usuario1.id + usuario2.id
        random.seed(seed)
        porcentaje = random.randint(0, 100)
        
        bloques = int(porcentaje / 10)
        barra = "💖" * bloques + "🖤" * (10 - bloques)

        system = "Eres un cupido sarcástico y gracioso. Explica brevemente la compatibilidad de esta pareja basándote en su porcentaje."
        prompt = f"Pareja: {usuario1.display_name} y {usuario2.display_name}. Compatibilidad: {porcentaje}%. Inventa una razón."
        
        comentario = await self.ai.generate_response(system, prompt)

        embed = discord.Embed(title="💘 Test de Compatibilidad", color=0xe91e63)
        embed.add_field(name="Pareja", value=f"{usuario1.mention} x {usuario2.mention}", inline=False)
        embed.add_field(name="Resultado", value=f"**{porcentaje}%**\n{barra}", inline=False)
        embed.add_field(name="Opinión de Cupido", value=comentario, inline=False)

        await interaction.followup.send(embed=embed)
    
    # /debate
    @app_commands.command(name="debate", description="Inicia un debate interactivo (Debes usar la función Responder)")
    @app_commands.describe(tema="El tema a debatir", postura="Tu postura (la IA defenderá la contraria)")
    async def debate(self, interaction: discord.Interaction, tema: str, postura: str = "A favor"):
        await interaction.response.defer()

        system = (
            "Eres un experto en debates. Tu objetivo es llevar la contraria al usuario "
            "con argumentos lógicos. Sé breve (máximo 50 palabras por turno). "
            "Habla siempre en Español de España."
        )
        
        historial = (
            f"TEMA: '{tema}'.\n"
            f"USUARIO: '{postura}'.\n"
            f"TÚ (IA): Postura opuesta.\n\n"
            "Argumento inicial:"
        )

        respuesta_ia = await self.ai.generate_response(system, historial)
        historial += f"\n\nIA: {respuesta_ia}"

        ultimo_mensaje_bot = await interaction.followup.send(
            f"**⚔️ DEBATE: {tema}**\n\n{respuesta_ia}\n\n"
            "*(⚠️ Para seguir, debes usar la función **Responder** a este mensaje)*"
        )

        def check(m):
            if m.author != interaction.user or m.channel != interaction.channel:
                return False

            if m.reference is None:
                return False

            return m.reference.message_id == ultimo_mensaje_bot.id

        while True:
            try:
                mensaje_usuario = await self.bot.wait_for('message', check=check, timeout=300.0)
                
                content = mensaje_usuario.content.lower()

                if content in ["fin", "stop", "me rindo", "adios"]:
                    await mensaje_usuario.reply("🏳️ Debate finalizado.")
                    break

                async with interaction.channel.typing():
                    historial += f"\n\nUSUARIO: {mensaje_usuario.content}"
                    
                    prompt = f"{historial}\n\nInstrucción: Rebate el argumento. Sé breve."
                    respuesta_ia = await self.ai.generate_response(system, prompt)
                    historial += f"\n\nIA: {respuesta_ia}"

                ultimo_mensaje_bot = await mensaje_usuario.reply(respuesta_ia)

            except asyncio.TimeoutError:
                await interaction.followup.send(f"⏳ {interaction.user.mention}, se acabó el tiempo.")
                break
            except Exception as e:
                print(f"Error debate: {e}")
                break
    
    # /roast
    @app_commands.command(name="roast", description="Haz una burla graciosa (roast) a un usuario")
    async def roast(self, interaction: discord.Interaction, usuario: discord.User):
        await interaction.response.defer()

        nombre = usuario.display_name
        es_bot = "es un bot" if usuario.bot else "es humano"
        
        system = (
            "Eres un comediante de 'Roast Battle' mordaz y sarcástico, pero sin ser excesivamente ofensivo ni racista. "
            "Tu objetivo es burlarte de forma graciosa e inteligente del usuario. Responde en Español de España."
        )
        prompt = f"Haz un roast al usuario llamado '{nombre}'. Info extra: {es_bot}."

        insulto = await self.ai.generate_response(system, prompt)
        
        await interaction.followup.send(f"🔥 **ROAST PARA {usuario.mention}:**\n\n{insulto}")
    
    # /joke
    @app_commands.command(name="joke", description="Cuenta un chiste sobre un tema opcional")
    async def joke(self, interaction: discord.Interaction, tema: str = "general"):
        await interaction.response.defer()
        
        system = "Eres un comediante español gracioso. Cuenta un chiste breve."
        prompt = f"Cuenta un chiste sobre: {tema}"
        
        response = await self.ai.generate_response(system, prompt)
        await interaction.followup.send(response)
        
    # /horoscopo
    @app_commands.command(name="horoscopo", description="Tu predicción diaria (inventada por IA)")
    @app_commands.describe(signo="Tu signo del zodiaco")
    async def horoscopo(self, interaction: discord.Interaction, signo: str):
        await interaction.response.defer()
        
        system = "Eres una adivina mística y un poco dramática. Genera un horóscopo breve, divertido y surrealista para hoy."
        response = await self.ai.generate_response(system, f"Signo: {signo}")
        
        embed = discord.Embed(title=f"🔮 Horóscopo: {signo.capitalize()}", description=response, color=0x9b59b6)
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Games(bot))