import discord
from discord.ext import commands
from discord import app_commands
from services.ai_service import GroqService
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

class Media(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai = GroqService()

    @app_commands.command(name="imagine", description="Genera una imagen usando IA (Pollinations)")
    async def imagine(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

        embed = discord.Embed(title=f"🎨 {prompt}", color=0xFF00FF)
        embed.set_image(url=image_url)
        embed.set_footer(text="Generado por Pollinations.ai")
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Media(bot))