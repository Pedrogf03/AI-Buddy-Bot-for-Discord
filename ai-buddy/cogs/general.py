import discord
from discord.ext import commands
from discord import app_commands
from services.ai_service import GroqService
import asyncio

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai = GroqService()

    @app_commands.command(name="joke", description="Cuenta un chiste sobre un tema opcional")
    async def joke(self, interaction: discord.Interaction, tema: str = "general"):
        await interaction.response.defer()
        
        system = "Eres un comediante español gracioso. Cuenta un chiste breve."
        prompt = f"Cuenta un chiste sobre: {tema}"
        
        response = await self.ai.generate_response(system, prompt)
        await interaction.followup.send(response)

    @app_commands.command(name="eli5", description="Explícamelo como si tuviera 5 años")
    async def eli5(self, interaction: discord.Interaction, concepto: str):
        await interaction.response.defer()
        
        system = "Eres un profesor amable. Explica conceptos complejos de forma extremadamente sencilla para un niño de 5 años. Usa emojis."
        
        response = await self.ai.generate_response(system, concepto)
        await interaction.followup.send(response)
        
    @app_commands.command(name="omewa", description="Genera un poema de amor para omewita", extras={'hidden': True})
    async def omewa(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        system = "Eres un poeta amable. Genera un poema de amor dedicado a omewita."
        
        response = await self.ai.generate_response(system, "Hazlo.")
        await interaction.followup.send(response)
        
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

async def setup(bot):
    await bot.add_cog(General(bot))