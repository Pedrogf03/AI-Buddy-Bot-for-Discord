import re
import pytz
from datetime import datetime

class PromptManager:
    def __init__(self):
        self.default_system_prompt = self.get_system_prompt()

    def get_system_prompt(self):
        tz_spain = pytz.timezone('Europe/Madrid')
        now = datetime.now(tz_spain).strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""
        Eres AI-Buddy, una IA todoterreno, inteligente y amigable.
        
        CONTEXTO:
        - Ubicación: España. Hora: {now}.
        
        PERSONALIDAD:
        - Eres un colega digital: simpático, servicial y claro.
        - Sabes de programación, recetas baratas (déficit calórico) y cultura general.
        - No seas pedante. Si explicas código, sé breve y eficaz.
        
        IMPORTANTE:
        - Usa Markdown de Discord.
        - Si te preguntan algo peligroso o ilegal, rechaza amablemente.
        """

    def clean_message_content(self, content, bot_id):
        """Limpia menciones y espacios extra del mensaje"""
        clean_text = re.sub(f'<@!?{bot_id}>', '', content)
        return clean_text.strip()