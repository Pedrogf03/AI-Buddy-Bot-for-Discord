import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from groq import RateLimitError, APIError

class GroqService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Falta la GROQ_API_KEY en el env")
        
        self.llm = ChatGroq(
            temperature=0.5,
            model_name="llama-3.3-70b-versatile",
            api_key=self.api_key,
            max_retries=2
        )

    async def generate_response(self, system_prompt: str, user_input: str) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        
        chain = prompt | self.llm

        try:
            response = await chain.ainvoke({"input": user_input})
            return response.content
        except RateLimitError:
            return "🥵 Estoy echando humo (Límite de velocidad). Dame un minuto."
        except APIError:
            return "🔌 Error de conexión con Groq."
        except Exception as e:
            return f"Error inesperado: {str(e)}"