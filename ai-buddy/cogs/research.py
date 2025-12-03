import discord
from discord.ext import commands
from discord import app_commands
from services.ai_service import GroqService
from utils.web_search import search_internet

class Research(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai = GroqService()

    @app_commands.command(name="search", description="Busca en internet y resume la información")
    async def search(self, interaction: discord.Interaction, consulta: str):
        await interaction.response.defer()
        
        search_results = search_internet(consulta)
        
        if not search_results:
            await interaction.followup.send("No encontré nada relevante en internet.")
            return

        system = (
            "Eres un asistente de investigación útil y preciso. "
            "Responde a la consulta del usuario BASÁNDOTE SOLO en la información provista. "
            "Si la información no es suficiente, dilo. Responde en Español de España.\n\n"
            "IMPORTANTE: Al final de tu respuesta, debes incluir una sección titulada 'Fuentes' "
            "donde listes las URLs exactas de donde has extraído la información. "
            "Usa el formato: - [Nombre de la web](URL)"
        )
        
        prompt = f"Consulta del usuario: {consulta}\n\nInformación de internet (incluye enlaces):\n{search_results}"
        
        try:
            response = await self.ai.generate_response(system, prompt)
            
            # Control de seguridad por si la respuesta es muy larga para un Embed
            if len(response) > 4096:
                response = response[:4090] + "..."

            embed = discord.Embed(title=f"🔎 Resultados: {consulta}", description=response, color=0x00ff00)
            embed.set_footer(text="Información obtenida vía DuckDuckGo & Groq")
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"❌ Ocurrió un error al procesar la búsqueda: {str(e)}")

async def setup(bot):
    await bot.add_cog(Research(bot))