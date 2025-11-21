import os
from dotenv import load_dotenv
from discord_bot import DiscordBot

def main():
    load_dotenv()
    
    try:
        model = "groq"
        # model = "gemini"
        
        bot = DiscordBot(model_provider=model)

        print("🚀 Iniciando sistema...")
        bot.run()
        
    except Exception as e:
        print(f"❌ Error fatal al iniciar: {e}")

if __name__ == "__main__":
    main()