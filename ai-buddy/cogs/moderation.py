import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="voice_disconnects", description="Cuenta veces que un usuario ha desconectado a otro de la voz")
    @app_commands.describe(moderador="Quien ejecutó la desconexión", usuario="Quien fue desconectado")
    async def voice_disconnects(self, interaction: discord.Interaction, moderador: discord.User, usuario: discord.User):

        if not interaction.guild.me.guild_permissions.view_audit_log:
            await interaction.response.send_message("❌ **Error:** No tengo permiso para ver el 'Registro de Auditoría'.", ephemeral=True)
            return

        await interaction.response.defer()

        contador = 0
        try:
            async for entry in interaction.guild.audit_logs(action=discord.AuditLogAction.member_disconnect, limit=None):
                
                if entry.user.id == moderador.id and entry.target.id == usuario.id:
                    contador += 1
            
            embed = discord.Embed(
                title="🎤 Informe de Voz",
                description="Recuento de desconexiones forzadas de canales de voz.",
                color=0x9b59b6
            )
            embed.add_field(name="Moderador", value=moderador.mention, inline=True)
            embed.add_field(name="Desconectó a", value=usuario.mention, inline=True)
            embed.add_field(name="Total de veces", value=f"**{contador}**", inline=False)
            
            await interaction.followup.send(embed=embed)

        except Exception as e:
            await interaction.followup.send(f"⚠️ Ocurrió un error leyendo los registros: {str(e)}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))