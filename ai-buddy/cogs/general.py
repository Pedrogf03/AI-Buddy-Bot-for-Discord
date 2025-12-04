import discord
from discord.ext import commands
from discord import app_commands
from services.ai_service import GroqService

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
        
        response = await self.ai.generate_response(system, "")
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

    @app_commands.command(name="debate", description="Inicia un debate con la IA")
    async def debate(self, interaction: discord.Interaction, tema: str, postura: str = "A favor"):
        await interaction.response.defer()

        system = (
            "Eres un experto en debates y abogado del diablo. Tu objetivo es llevar la contraria al usuario "
            "con argumentos lógicos, sólidos y a veces provocadores. Sé breve pero contundente. "
            "Habla siempre en Español de España."
        )
        
        prompt = (
            f"El tema del debate es: '{tema}'.\n"
            f"El usuario defiende la postura: '{postura}'.\n"
            "Tú debes defender la postura OPUESTA. Empieza el debate dando tu primer argumento."
        )

        respuesta = await self.ai.generate_response(system, prompt)
        
        embed = discord.Embed(title=f"🗣️ Debate: {tema}", description=respuesta, color=0xe67e22)
        embed.set_footer(text=f"Tú defiendes: {postura} | La IA defiende lo contrario")
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))