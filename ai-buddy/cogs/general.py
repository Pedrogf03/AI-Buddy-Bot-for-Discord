import discord
from discord.ext import commands
from discord import app_commands
import re
import urllib.parse
import requests
import io
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

            if len(respuesta) <= 4000:
                embed = discord.Embed(description=respuesta, color=0x2ecc71)
                embed.set_author(name=f"Pregunta de {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
                embed.title = pregunta[:250]
                await interaction.followup.send(embed=embed)
            else:
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
        
        if len(response) < 1000 and len(texto) < 1000:
            embed = discord.Embed(title=f"Traducción al {idioma}", color=0x3498db)
            embed.add_field(name="Original", value=texto, inline=False)
            embed.add_field(name="Traducción", value=response, inline=False)
            await interaction.followup.send(embed=embed)
        else:
            header = f"🌐 **Traducción al {idioma}**\n\n**Original:**\n{texto[:500]}..." if len(texto) > 500 else f"**Original:**\n{texto}"
            await interaction.followup.send(header)
            
            fragmentos = split_text(f"**Traducción:**\n{response}")
            for frag in fragmentos:
                await interaction.channel.send(frag)

    # /code
    @app_commands.command(name="code", description="Genera un archivo de código en el lenguaje especificado")
    @app_commands.describe(lenguaje="Python, JS, C++...", instruccion="Qué debe hacer el código")
    async def codigo(self, interaction: discord.Interaction, lenguaje: str, instruccion: str):
        await interaction.response.defer()
        
        extensiones = {
            'python': 'py', 'py': 'py', 'javascript': 'js', 'js': 'js', 'node': 'js',
            'typescript': 'ts', 'ts': 'ts', 'html': 'html', 'css': 'css',
            'c++': 'cpp', 'cpp': 'cpp', 'c': 'c', 'java': 'java', 'c#': 'cs', 
            'go': 'go', 'rust': 'rs', 'php': 'php', 'sql': 'sql', 'json': 'json', 'bash': 'sh'
        }
        ext = extensiones.get(lenguaje.lower(), 'txt')
        
        system = (
            f"Eres un experto programador senior. Genera código en {lenguaje}. "
            "IMPORTANTE: Devuelve ÚNICAMENTE el código en texto plano. "
            "NO uses bloques de markdown, ni títulos, ni explicaciones. "
        )
        prompt = f"Instrucción: {instruccion}"
        
        response = await self.ai.generate_response(system, prompt)
        
        # Limpieza por si la IA pone markdown
        codigo_limpio = response.replace(f"```{lenguaje.lower()}", "").replace("```", "").strip()
        
        archivo_en_memoria = io.BytesIO(codigo_limpio.encode('utf-8'))
        archivo_discord = discord.File(archivo_en_memoria, filename=f"code.{ext}")
        
        await interaction.followup.send(f"Aquí tienes tu código en **{lenguaje}**:", file=archivo_discord)

    # /resumen
    @app_commands.command(name="resumen", description="Resume un texto, un archivo o una web en 3 puntos clave")
    @app_commands.describe(texto="Texto directo", archivo="Archivo de texto (.txt, .md, .py...)", url="Enlace a una web")
    async def resumir(self, interaction: discord.Interaction, texto: str = None, archivo: discord.Attachment = None, url: str = None):
        await interaction.response.defer()
        
        contenido_a_resumir = ""

        # 1. Procesamiento de Archivo
        if archivo:
            # Verificamos que sea un archivo de texto o código manejable
            if not archivo.filename.endswith(('.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.c', '.cpp')):
                await interaction.followup.send("❌ Por favor, sube un archivo de texto válido (.txt, .md, código, etc).")
                return
            try:
                # Leemos los bytes y decodificamos a string
                archivo_bytes = await archivo.read()
                contenido_a_resumir = archivo_bytes.decode('utf-8')
            except UnicodeDecodeError:
                await interaction.followup.send("❌ No pude leer el archivo. Asegúrate de que esté codificado en UTF-8.")
                return

        # 2. Procesamiento de URL
        elif url:
            try:
                # Hacemos la petición a la web
                page = requests.get(url, timeout=10)
                if page.status_code == 200:
                    raw_html = page.text
                    # Limpieza básica de HTML usando regex para no gastar tokens en etiquetas
                    clean_text = re.sub(r'<[^>]+>', '', raw_html) # Elimina etiquetas <...>
                    contenido_a_resumir = clean_text[:10000] # Limitamos caracteres para no saturar
                else:
                    await interaction.followup.send(f"❌ No pude acceder a la web. Código de estado: {page.status_code}")
                    return
            except Exception as e:
                await interaction.followup.send(f"❌ Error al intentar acceder a la URL: {str(e)}")
                return

        # 3. Procesamiento de Texto directo
        elif texto:
            contenido_a_resumir = texto

        # Validación final
        if not contenido_a_resumir:
            await interaction.followup.send("⚠️ Debes proporcionar un **texto**, adjuntar un **archivo** o poner una **URL**.")
            return

        # Enviamos a la IA
        system = "Eres un asistente eficiente. Resume el siguiente contenido proporcionado por el usuario en 3 puntos clave (bullet points). Sé conciso."
        
        # Recortamos por seguridad si es gigante (aunque Groq suele aguantar bastante contexto)
        response = await self.ai.generate_response(system, contenido_a_resumir[:15000])
        
        if len(response) <= 4000:
            embed = discord.Embed(title="📝 Resumen", description=response, color=0xe67e22)
            if url:
                embed.set_footer(text=f"Fuente: {url}")
            elif archivo:
                embed.set_footer(text=f"Archivo: {archivo.filename}")
            await interaction.followup.send(embed=embed)
        else:
            fragmentos = split_text(f"📝 **Resumen:**\n\n{response}")
            for i, frag in enumerate(fragmentos):
                if i == 0:
                    await interaction.followup.send(frag)
                else:
                    await interaction.channel.send(frag)
    
    # /code_review
    @app_commands.command(name="code_review", description="Analiza tu código, explica errores y envía la corrección en un archivo")
    @app_commands.describe(lenguaje="Python, JS, etc.", codigo="Pega aquí tu código")
    async def revisar_codigo(self, interaction: discord.Interaction, lenguaje: str, codigo: str):
        await interaction.response.defer()

        # Determinamos extensión igual que en /code
        extensiones = {
            'python': 'py', 'py': 'py', 'javascript': 'js', 'js': 'js', 'node': 'js',
            'typescript': 'ts', 'ts': 'ts', 'html': 'html', 'css': 'css',
            'c++': 'cpp', 'cpp': 'cpp', 'c': 'c', 'java': 'java', 'c#': 'cs', 
            'go': 'go', 'rust': 'rs', 'php': 'php', 'sql': 'sql', 'json': 'json', 'bash': 'sh'
        }
        ext = extensiones.get(lenguaje.lower(), 'txt')

        # Prompt con separador especial para dividir explicación y código raw
        separator = "---CODE_SEPARATOR---"
        
        system = (
            f"Eres un ingeniero de software senior experto en {lenguaje}. "
            "Analiza el código del usuario. "
            "1. Proporciona una explicación clara de los errores y las mejoras realizadas. "
            f"2. Luego, inserta exactamente este separador: {separator}\n"
            "3. Después del separador, proporciona ÚNICAMENTE el código corregido completo en texto plano (sin markdown, sin ```). "
            "Tu respuesta debe tener esas dos partes diferenciadas."
        )

        response = await self.ai.generate_response(system, codigo)
        
        # Lógica de separación
        if separator in response:
            partes = response.split(separator)
            explicacion = partes[0].strip()
            codigo_final = partes[1].strip()
            
            # Limpieza extra del código por si acaso
            codigo_final = codigo_final.replace(f"```{lenguaje.lower()}", "").replace("```", "").strip()
        else:
            # Fallback por si la IA ignora el separador
            explicacion = response
            codigo_final = ""

        # 1. Enviamos la explicación (Embed o texto plano si es muy larga)
        if len(explicacion) <= 4000:
            embed = discord.Embed(title=f"🛠️ Revisión de código ({lenguaje})", description=explicacion, color=0x34495e)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"🛠️ **Revisión de código ({lenguaje})**")
            fragmentos = split_text(explicacion)
            for frag in fragmentos:
                await interaction.channel.send(frag)
        
        # 2. Enviamos el archivo con el código corregido si existe
        if codigo_final:
            archivo_memoria = io.BytesIO(codigo_final.encode('utf-8'))
            archivo_discord = discord.File(archivo_memoria, filename=f"revisado.{ext}")
            
            # Lo enviamos como un mensaje nuevo en el mismo hilo/canal
            await interaction.channel.send("Aquí tienes el archivo con el código corregido y optimizado:", file=archivo_discord)

async def setup(bot):
    await bot.add_cog(General(bot))