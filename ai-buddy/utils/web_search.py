from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def search_internet(query: str) -> str:
    wrapper = DuckDuckGoSearchAPIWrapper(region="es-es", time="y", max_results=3)
    try:
        return wrapper.run(query)
    except Exception as e:
        return f"Error en la búsqueda: {str(e)}"