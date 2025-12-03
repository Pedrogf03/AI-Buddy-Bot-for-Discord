"""
AI Discord Bot - Un bot de Discord con IA
"""

__version__ = "2.0.0"
__author__ = "Pedrogf03"

from .services.ai_service import GroqService
from .utils.web_search import search_internet

__all__ = [
    'GroqService',
    'search_internet'
]

package_info = {
    "name": "AI Discord Bot",
    "version": __version__,
    "models_available": ["groq"],
    "description": "Bot de Discord modular con Slash Commands y soporte para Groq"
}

def get_info():
    return package_info