import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="voice_kicks", description="Muestra un ranking de usuarios que más han desconectado a otros de canales de voz")
    async def voice_kicks(self, interaction: discord.Interaction):

        if not interaction.guild.me.guild_permissions.view_audit_log:
            await interaction.response.send_message("❌ Error: No tengo permiso para ver el 'Registro de Auditoría'.", ephemeral=True)
            return

        await interaction.response.defer()

        # Diccionario para guardar {ID_Usuario: {objeto_usuario, contador}}
        stats = {}
        fecha_mas_antigua = None  # Variable para rastrear la fecha

        try:
            async for entry in interaction.guild.audit_logs(action=discord.AuditLogAction.member_disconnect, limit=None):
                
                if entry.user is None:
                    continue
                
                fecha_mas_antigua = entry.created_at

                if entry.user in stats:
                    stats[entry.user]['cantidad'] += entry.extra.count
                else:
                    stats[entry.user] = {
                        'user': entry.user.name,
                        'cantidad': entry.extra.count
                    }

            ranking_ordenado = sorted(stats.values(), key=lambda x: x['cantidad'], reverse=True)

            if not ranking_ordenado:
                await interaction.followup.send("No he encontrado desconexiones en el registro.")
                return

            descripcion = ""
            for i, data in enumerate(ranking_ordenado[:10], 1):
                usuario = data['user']
                total = data['cantidad']
                
                medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
                
                descripcion += f"**{medalla}** {usuario} — **{total}** veces\n"

            texto_fecha = fecha_mas_antigua.strftime("%d/%m/%Y") if fecha_mas_antigua else "Desconocida"

            embed = discord.Embed(
                title="✂️ Ranking de Desconexiones de Voz",
                description=f"Estos son los usuarios que más gente han echado del chat de voz:\n\n{descripcion}",
                color=0xe74c3c
            )
            embed.set_footer(text=f"Datos extraídos desde: {texto_fecha}")

            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"Error al generar ranking: {e}")
            await interaction.followup.send(f"⚠️ Ocurrió un error procesando el ranking: {str(e)}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))