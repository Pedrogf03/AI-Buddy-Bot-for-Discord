import discord
from discord.ext import commands
from discord import app_commands
import re
import urllib.parse
import requests
from services.ai_service import GroqService
from utils.web_search import search_internet
from utils.split_text import split_text

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai = GroqService()

    # /eli5
    @app_commands.command(name="eli5", description="Explícamelo como si tuviera 5 años")
    async def eli5(self, interaction: discord.Interaction, concepto: str):
        await interaction.response.defer()
        
        system = "Eres un profesor amable. Explica conceptos complejos de forma extremadamente sencilla para un niño de 5 años. Usa emojis."
        
        response = await self.ai.generate_response(system, concepto)
        
        # Aplicamos split_text
        fragmentos = split_text(response)
        for i, frag in enumerate(fragmentos):
            if i == 0:
                await interaction.followup.send(frag)
            else:
                await interaction.channel.send(frag)
        
    # /ask
    @app_commands.command(name="ask", description="Haz cualquier pregunta a la IA")
    @app_commands.describe(pregunta="Lo que quieras saber o conversar")
    async def ask(self, interaction: discord.Interaction, pregunta: str):

        await interaction.response.defer()

        system = (
            "Eres AI-Buddy, un asistente virtual útil, inteligente y amable. "
            "Responde a las preguntas del usuario de forma clara, precisa y en Español de España. "
            "Usa formato Markdown (negritas, listas, bloques de código) para estructurar bien tu respuesta."
        )

        try:
            respuesta = await self.ai.generate_response(system, pregunta)

            # Lógica híbrida:
            # Si la respuesta cabe en un Embed (aprox 4000 chars), usamos Embed porque es más bonito.
            # Si es más larga, usamos split_text y enviamos mensajes normales para no cortar nada.
            
            if len(respuesta) <= 4000:
                embed = discord.Embed(description=respuesta, color=0x2ecc71)
                embed.set_author(name=f"Pregunta de {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
                embed.title = pregunta[:250]
                await interaction.followup.send(embed=embed)
            else:
                # Caso respuesta masiva: Enviamos encabezado y luego el texto dividido
                await interaction.followup.send(f"**❓ Pregunta:** {pregunta}\n*(La respuesta es larga, se enviará en varios mensajes)*")
                
                fragmentos = split_text(respuesta)
                for frag in fragmentos:
                    await interaction.channel.send(frag)

        except Exception as e:
            await interaction.followup.send(f"❌ Ocurrió un error al generar la respuesta: {str(e)}")
            
    # /search
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
            
            # Igual que en /ask, si es gigante (muchas fuentes), usamos texto plano dividido
            if len(response) <= 4000:
                embed = discord.Embed(title=f"🔎 Resultados: {consulta}", description=response, color=0x00ff00)
                embed.set_footer(text="Información obtenida vía DuckDuckGo & Groq")
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(f"🔎 **Resultados para: {consulta}**")
                
                fragmentos = split_text(response)
                for frag in fragmentos:
                    await interaction.channel.send(frag)

        except Exception as e:
            await interaction.followup.send(f"❌ Ocurrió un error al procesar la búsqueda: {str(e)}")
            
    # /imagine
    @app_commands.command(name="imagine", description="Genera una imagen usando IA (Pollinations)")
    async def imagine(self, interaction: discord.Interaction, prompt: str):
        # Las imágenes no necesitan split_text
        await interaction.response.defer()
        
        encoded_prompt = urllib.parse.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"

        embed = discord.Embed(title=f"🎨 {prompt}", color=0xFF00FF)
        embed.set_image(url=image_url)
        embed.set_footer(text="Generado por Pollinations.ai")
        
        await interaction.followup.send(embed=embed)
        
    # /traductor
    @app_commands.command(name="traductor", description="Traduce un texto a cualquier idioma")
    @app_commands.describe(texto="El texto a traducir", idioma="Idioma destino (ej: Inglés, Francés, Japonés)")
    async def traducir(self, interaction: discord.Interaction, texto: str, idioma: str):
        await interaction.response.defer()
        
        system = f"Eres un traductor profesional experto. Traduce el texto del usuario al idioma: {idioma}. Devuelve SOLO la traducción, sin explicaciones extra."
        response = await self.ai.generate_response(system, texto)
        
        # Los campos de Embed (add_field) tienen límite de 1024 caracteres.
        if len(response) < 1000 and len(texto) < 1000:
            embed = discord.Embed(title=f"Traducción al {idioma}", color=0x3498db)
            embed.add_field(name="Original", value=texto, inline=False)
            embed.add_field(name="Traducción", value=response, inline=False)
            await interaction.followup.send(embed=embed)
        else:
            # Si es un texto largo, lo enviamos dividido
            header = f"🌐 **Traducción al {idioma}**\n\n**Original:**\n{texto[:500]}..." if len(texto) > 500 else f"**Original:**\n{texto}"
            await interaction.followup.send(header)
            
            fragmentos = split_text(f"**Traducción:**\n{response}")
            for frag in fragmentos:
                await interaction.channel.send(frag)

    # /code
    @app_commands.command(name="code", description="Genera un snippet de código en el lenguaje especificado")
    @app_commands.describe(lenguaje="Python, JS, C++...", instruccion="Qué debe hacer el código")
    async def codigo(self, interaction: discord.Interaction, lenguaje: str, instruccion: str):
        await interaction.response.defer()
        
        system = (
            f"Eres un experto programador senior. Genera código en {lenguaje}. "
            "Proporciona solo el código dentro de bloques markdown, con comentarios breves explicativos en el código. "
            "No des cháchara antes ni después."
        )
        prompt = f"Instrucción: {instruccion}"
        
        response = await self.ai.generate_response(system, prompt)
        
        texto_completo = f"Aquí tienes tu código en **{lenguaje}**:\n{response}"
        fragmentos = split_text(texto_completo)
        
        for i, frag in enumerate(fragmentos):
            if i == 0:
                await interaction.followup.send(frag)
            else:
                await interaction.channel.send(frag)

    # /resumen
    @app_commands.command(name="resumen", description="Resume un texto largo en 3 puntos clave")
    async def resumir(self, interaction: discord.Interaction, texto: str):
        await interaction.response.defer()
        
        system = "Eres un asistente eficiente. Resume el siguiente texto proporcionado por el usuario en 3 puntos clave (bullet points). Sé conciso."
        
        response = await self.ai.generate_response(system, texto)
        
        if len(response) <= 4000:
            embed = discord.Embed(title="📝 Resumen", description=response, color=0xe67e22)
            await interaction.followup.send(embed=embed)
        else:
            fragmentos = split_text(f"📝 **Resumen:**\n\n{response}")
            for i, frag in enumerate(fragmentos):
                if i == 0:
                    await interaction.followup.send(frag)
                else:
                    await interaction.channel.send(frag)
    
    # /code_review
    @app_commands.command(name="code_review", description="La IA analiza tu código, busca errores y lo mejora")
    @app_commands.describe(lenguaje="Python, JS, etc.", codigo="Pega aquí tu código")
    async def revisar_codigo(self, interaction: discord.Interaction, lenguaje: str, codigo: str):
        await interaction.response.defer()

        system = (
            f"Eres un ingeniero de software senior experto en {lenguaje}. "
            "Analiza el código del usuario. "
            "1. Busca bugs potenciales o malas prácticas. "
            "2. Muestra la versión corregida y optimizada. "
            "3. Explica los cambios brevemente."
        )

        response = await self.ai.generate_response(system, codigo)
        
        # Code reviews suelen ser largas, verificamos longitud
        if len(response) <= 4000:
            embed = discord.Embed(title=f"🛠️ Revisión de código ({lenguaje})", description=response, color=0x34495e)
            await interaction.followup.send(embed=embed)
        else:
            header = f"🛠️ **Revisión de código ({lenguaje})**"
            await interaction.followup.send(header)
            
            fragmentos = split_text(response)
            for frag in fragmentos:
                await interaction.channel.send(frag)

async def setup(bot):
    await bot.add_cog(General(bot))