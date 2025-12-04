import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class AiBuddy(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        await self.load_extension("cogs.general")
        await self.load_extension("cogs.research")
        await self.load_extension("cogs.media")
        await self.load_extension("cogs.utility")
        await self.load_extension("cogs.help")
        await self.load_extension("cogs.moderation")
        
        await self.tree.sync()
        print("✅ Comandos sincronizados correctamente.")

    async def on_ready(self):
        print(f'🤖 Conectado como {self.user} (ID: {self.user.id})')
        
        print(f"\n🌍 Conectado a {len(self.guilds)} servidores:")
        for guild in self.guilds:
            print(f"  • {guild.name} (ID: {guild.id})")
        print("---------------------------------------")
        
        await self.change_presence(activity=discord.Game(name="/ask o /help"))

bot = AiBuddy()

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))