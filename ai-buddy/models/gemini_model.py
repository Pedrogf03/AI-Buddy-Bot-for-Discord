import os
from langchain_google_genai import ChatGoogleGenerativeAI
from .base_model import BaseModel

class GeminiModel(BaseModel):
    def __init__(self, temperature=0.7, model_name="gemini-2.5-flash-lite"):
        self.model_name = model_name
        self.api_key = os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError("❌ Falta la GOOGLE_API_KEY en el archivo .env")

        super().__init__(temperature)
    
    def get_llm(self):
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=self.temperature,
            google_api_key=self.api_key,
        )
    
    @staticmethod
    def handle_error(error):
        error_msg = str(error).lower()
        if "quota" in error_msg or "resource exhausted" in error_msg:
            return "📊 He alcanzado mi cuota de Google API por hoy."
        return None