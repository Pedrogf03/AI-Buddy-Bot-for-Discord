import os
from langchain_groq import ChatGroq
from groq import RateLimitError, APIError
from .base_model import BaseModel

class GroqModel(BaseModel):
    def __init__(self, temperature=0.7, model_name="llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("❌ Falta la GROQ_API_KEY en el archivo .env")
            
        super().__init__(temperature)
    
    def get_llm(self):
        return ChatGroq(
            temperature=self.temperature,
            model_name=self.model_name,
            api_key=self.api_key,
            max_retries=2
        )
    
    @staticmethod
    def handle_error(error):
        if isinstance(error, RateLimitError):
            return "🥵 Estoy echando humo (Rate Limit). Dame un minuto."
        elif isinstance(error, APIError):
            return "🔌 Error de conexión con Groq. Intenta de nuevo."
        return None