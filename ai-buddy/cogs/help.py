import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Muestra todos los comandos disponibles")
    async def help_command(self, interaction: discord.Interaction):
        # Creamos el embed base
        embed = discord.Embed(
            title="🤖 Centro de Ayuda de AI-Buddy",
            description="Aquí tienes la lista de todo lo que puedo hacer por ti:",
            color=0x9b59b6
        )
        
        # Iteramos sobre todos los comandos de barra (slash commands) registrados
        # self.bot.tree.walk_commands() recorre todos los comandos y subcomandos
        for command in self.bot.tree.walk_commands():
            # Filtramos para no mostrar comandos que no tengan descripción (opcional)
            if isinstance(command, app_commands.Command):
                nombre = f"/{command.name}"
                descripcion = command.description or "Sin descripción disponible."
                
                # Si el comando tiene parámetros, podemos indicarlo visualmente (opcional)
                if command.parameters:
                    nombre += " `[opciones]`"

                embed.add_field(name=nombre, value=descripcion, inline=False)

        embed.set_footer(text="Usa los comandos escribiendo '/' en el chat.")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))