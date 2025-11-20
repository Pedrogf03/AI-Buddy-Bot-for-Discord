"""
AI Discord Bot - Un bot de Discord con múltiples modelos de IA
"""

__version__ = "1.0.0"
__author__ = "Pedrogf03"

# Importaciones principales para facilitar el acceso
from .discord_bot import DiscordBot
from .models import GroqModel, GeminiModel
from .utils import PromptManager

# Lista de lo que se exporta por defecto
__all__ = [
    'DiscordBot',
    'GroqModel', 
    'GeminiModel',
    'PromptManager'
]

# Información del paquete
package_info = {
    "name": "AI Discord Bot",
    "version": __version__,
    "models_available": ["groq", "gemini"],
    "description": "Bot de Discord con soporte para múltiples modelos de IA"
}

def get_info():
    """Retorna información del paquete"""
    return package_info