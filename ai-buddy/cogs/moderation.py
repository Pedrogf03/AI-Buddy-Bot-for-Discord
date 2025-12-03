import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kicks", description="Cuenta cuántas veces un usuario ha expulsado a otro")
    @app_commands.describe(moderador="El usuario que ejecutó la expulsión", usuario="El usuario que fue expulsado")
    async def kicks(self, interaction: discord.Interaction, moderador: discord.User, usuario: discord.User):
        if not interaction.guild.me.guild_permissions.view_audit_log:
            await interaction.response.send_message("❌ **Error:** No tengo permiso para ver el 'Registro de Auditoría' en este servidor.", ephemeral=True)
            return

        await interaction.response.defer()

        contador = 0
        try:
            async for entry in interaction.guild.audit_logs(action=discord.AuditLogAction.member_disconnect, limit=None):
                

                if entry.user.id == moderador.id and entry.target.id == usuario.id:
                    contador += 1
            
            embed = discord.Embed(
                title="👮‍♂️ Informe de Auditoría",
                description=f"Recuento de expulsiones entre los usuarios seleccionados.",
                color=0xe74c3c
            )
            embed.add_field(name="Moderador", value=moderador.mention, inline=True)
            embed.add_field(name="Expulsó a", value=usuario.mention, inline=True)
            embed.add_field(name="Total de veces", value=f"**{contador}**", inline=False)
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"⚠️ Ocurrió un error leyendo los registros: {str(e)}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))