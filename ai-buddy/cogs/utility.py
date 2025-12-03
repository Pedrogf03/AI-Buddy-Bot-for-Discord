import discord
from discord.ext import commands
from discord import app_commands
from services.ai_service import GroqService

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai = GroqService()

    @app_commands.command(name="traducir", description="Traduce un texto a cualquier idioma")
    @app_commands.describe(texto="El texto a traducir", idioma="Idioma destino (ej: Inglés, Francés, Japonés)")
    async def traducir(self, interaction: discord.Interaction, texto: str, idioma: str):
        await interaction.response.defer()
        
        system = f"Eres un traductor profesional experto. Traduce el texto del usuario al idioma: {idioma}. Devuelve SOLO la traducción, sin explicaciones extra."
        response = await self.ai.generate_response(system, texto)
        
        embed = discord.Embed(title=f"Traducción al {idioma}", color=0x3498db)
        embed.add_field(name="Original", value=texto, inline=False)
        embed.add_field(name="Traducción", value=response, inline=False)
        
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="codigo", description="Genera un snippet de código en el lenguaje especificado")
    @app_commands.describe(lenguaje="Python, JS, C++...", instruccion="Qué debe hacer el código")
    async def codigo(self, interaction: discord.Interaction, lenguaje: str, instruccion: str):
        await interaction.response.defer()
        
        system = (
            f"Eres un experto programador senior. Genera código en {lenguaje}. "
            "Proporciona solo el código dentro de bloques markdown, con comentarios breves explicativos en el código. "
            "No des cháchara antes ni después."
        )
        prompt = f"Instrucción: {instruccion}"
        
        response = await self.ai.generate_response(system, prompt)
        await interaction.followup.send(f"Aquí tienes tu código en **{lenguaje}**:\n{response}")

    @app_commands.command(name="resumir", description="Resume un texto largo en 3 puntos clave")
    async def resumir(self, interaction: discord.Interaction, texto: str):
        await interaction.response.defer()
        
        system = "Eres un asistente eficiente. Resume el siguiente texto proporcionado por el usuario en 3 puntos clave (bullet points). Sé conciso."
        
        response = await self.ai.generate_response(system, texto)
        
        embed = discord.Embed(title="📝 Resumen", description=response, color=0xe67e22)
        await interaction.followup.send(embed=embed)
        
    @app_commands.command(name="ask", description="Haz cualquier pregunta a la IA")
    @app_commands.describe(pregunta="Lo que quieras saber o conversar")
    async def ask(self, interaction: discord.Interaction, pregunta: str):

        await interaction.response.defer()

        system = (
            "Eres AI-Buddy, un asistente virtual útil, inteligente y amable. "
            "Responde a las preguntas del usuario de forma clara, precisa y en Español de España. "
            "Usa formato Markdown (negritas, listas, bloques de código) para estructurar bien tu respuesta."
        )

        try:
            respuesta = await self.ai.generate_response(system, pregunta)

            if len(respuesta) > 4090:
                respuesta = respuesta[:4090] + "... (respuesta truncada por límite de Discord)"

            embed = discord.Embed(description=respuesta, color=0x2ecc71)

            embed.set_author(name=f"Pregunta de {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
            embed.title = pregunta[:250]
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"❌ Ocurrió un error al generar la respuesta: {str(e)}")

async def setup(bot):
    await bot.add_cog(Utility(bot))