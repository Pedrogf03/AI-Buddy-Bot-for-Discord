import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class AiBuddy(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        await self.load_extension("cogs.games")
        await self.load_extension("cogs.general")
        await self.load_extension("cogs.help")
        await self.load_extension("cogs.moderation")
        await self.load_extension("cogs.private")
        
        await self.tree.sync()
        print("✅ Comandos sincronizados correctamente.")

    async def on_ready(self):
        print(f'🤖 Conectado como {self.user} (ID: {self.user.id})')
        
        print(f"\n🌍 Conectado a {len(self.guilds)} servidores:")
        print("="*60)
        
        for guild in self.guilds:
            dueno = guild.owner.name if guild.owner else "Desconocido (Falta Intent o Caché)"
            
            print(f"  • {guild.name}")
            print(f"    🆔 ID: {guild.id}")
            print(f"    👑 Dueño: {dueno}")
            print(f"    👥 Miembros: {guild.member_count}")
            print("-" * 30)
            
        print("="*60 + "\n")
        
        await self.change_presence(activity=discord.Game(name="/ask o /help"))

bot = AiBuddy()

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))