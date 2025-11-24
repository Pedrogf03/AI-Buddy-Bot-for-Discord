from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from utils.tools_manager import get_tools
from langchain_core.output_parsers import StrOutputParser

class BaseModel(ABC):
    def __init__(self, temperature=0.7):
        self.temperature = temperature
        self.llm = self.get_llm()
        self.tools = get_tools()
        
        self.search_triggers = [
            "busca", "buscar", "investiga", "google", 
            "internet", "precio de", "encuentra informacion",
            "busca en la web", "¿quién es", "¿qué pasó"
        ]

    @abstractmethod
    def get_llm(self):
        """Debe devolver una instancia de un LLM de LangChain"""
        pass
    
    def _should_search(self, text: str) -> bool:
        """Determina si el mensaje del usuario pide explícitamente buscar."""
        text_lower = text.lower()
        return any(trigger in text_lower for trigger in self.search_triggers)

    async def generate_response(self, system_instruction, chat_history, text):
        try:
            # Búsqueda activada
            if self._should_search(text):
                print(f"🔎 Detectado intento de búsqueda para: '{text}'")
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_instruction),
                    ("system", "Has sido activado en MODO BÚSQUEDA. Usa la herramienta 'internet_search'. "
                                "Sintetiza la respuesta y SIEMPRE cita la URL de la fuente al final."),
                    ("system", "Historial:\n{chat_history}"),
                    ("human", "{text}"),
                    ("placeholder", "{agent_scratchpad}"),
                ])

                agent = create_tool_calling_agent(self.llm, self.tools, prompt)
                agent_executor = AgentExecutor(
                    agent=agent, 
                    tools=self.tools, 
                    verbose=True,
                    handle_parsing_errors=True
                )

                response = await agent_executor.ainvoke({
                    "chat_history": chat_history, 
                    "text": text
                })
                return response["output"]

            # Charla activada
            else:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_instruction),
                    ("system", "Historial reciente:\n{chat_history}"),
                    ("human", "{text}")
                ])

                chain = prompt | self.llm | StrOutputParser()
                
                response = await chain.ainvoke({
                    "chat_history": chat_history, 
                    "text": text
                })
                
                return response

        except Exception as e:
            print(f"Error generando respuesta: {e}")
            return "Tuve un problema procesando tu solicitud de búsqueda."