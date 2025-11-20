from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate

class BaseModel(ABC):
    def __init__(self, temperature=0.7):
        self.temperature = temperature
        self.llm = self.get_llm()

    @abstractmethod
    def get_llm(self):
        """Debe devolver una instancia de un LLM de LangChain"""
        pass

    async def generate_response(self, system_instruction, chat_history, text):
        """Genera una respuesta usando una cadena de LangChain"""
        try:
            # Crear el template del prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_instruction),
                ("system", "Historial reciente del chat:\n{chat_history}"),
                ("human", "{text}")
            ])

            # Crear la cadena (Chain)
            chain = prompt | self.llm
            
            # Invocar
            response = await chain.ainvoke({
                "chat_history": chat_history, 
                "text": text
            })
            
            return response.content
        except Exception as e:
            print(f"Error generando respuesta: {e}")
            raise e