import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# Aseguramos que sea entero, ya que os.getenv devuelve string
MY_GUILD_ID = discord.Object(id=int(os.getenv("MY_GUILD_ID")))

class AiBuddy(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):

        extensions = [
            "cogs.games",
            "cogs.general",
            "cogs.help",
            "cogs.moderation",
            "cogs.private"
        ]

        for ext in extensions:
            try:
                await self.load_extension(ext)
                print(f"✅ Cargado: {ext}")
            except commands.ExtensionNotFound:
                print(f"⚠️ No se encontró la extensión: {ext} (Saltando...)")
            except Exception as e:
                print(f"❌ Error al cargar {ext}: {e}")

        try:
            self.tree.copy_global_to(guild=MY_GUILD_ID)
            await self.tree.sync(guild=MY_GUILD_ID)
            print("✅ Comandos sincronizados para el servidor objetivo.")
        except discord.errors.Forbidden:
            print("⚠️ EL bot no está en el servidor objetivo. Sincronizado globalmente.")
            await self.tree.sync()
        except discord.errors.HTTPException as e:
            print(f"⚠️ Error HTTP al sincronizar: {e}")
        except Exception as e:
            print(f"❌ Error inesperado al sincronizar: {e}")

    async def on_ready(self):
        print(f'🤖 Conectado como {self.user} (ID: {self.user.id})')
        
        print(f"\n🌍 Conectado a {len(self.guilds)} servidores:")
        print("="*60)
        
        for guild in self.guilds:
            # Manejo de error por si guild.owner es None (pasa a veces en sharding o cache incompleta)
            dueno = guild.owner.name if guild.owner else "Desconocido"
            
            print(f"  • {guild.name}")
            print(f"    🆔 ID: {guild.id}")
            print(f"    👑 Dueño: {dueno}")
            print(f"    👥 Miembros: {guild.member_count}")
            print("-" * 30)
            
        print("="*60 + "\n")
        
        await self.change_presence(activity=discord.Game(name="/ask"))

bot = AiBuddy()

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))