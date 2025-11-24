from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def get_tools():
    """Configura y devuelve las herramientas disponibles para el agente."""
    # max_results=3 es suficiente para obtener contexto sin gastar muchos tokens
    wrapper = DuckDuckGoSearchAPIWrapper(region="es-es", time="y", max_results=3)
    search_tool = DuckDuckGoSearchResults(api_wrapper=wrapper, source="text")
    
    # Es importante darle un nombre y descripción clara para que el LLM sepa cuándo usarla
    search_tool.name = "internet_search"
    search_tool.description = "Útil para buscar información actual, noticias o datos específicos en internet."
    
    return [search_tool]