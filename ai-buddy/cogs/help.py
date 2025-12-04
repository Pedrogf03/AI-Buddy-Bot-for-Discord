import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Muestra todos los comandos disponibles")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Centro de Ayuda de AI-Buddy",
            description="Aquí tienes la lista de todo lo que puedo hacer por ti:",
            color=0x9b59b6
        )
        
        for command in self.bot.tree.walk_commands():
            
            if command.extras.get('hidden'):
                continue

            if isinstance(command, app_commands.Command):
                nombre = f"/{command.name}"
                descripcion = command.description or "Sin descripción disponible."
                
                if command.parameters:
                    nombre += " `[opciones]`"

                embed.add_field(name=nombre, value=descripcion, inline=False)

        embed.set_footer(text="Usa los comandos escribiendo '/' en el chat.")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))