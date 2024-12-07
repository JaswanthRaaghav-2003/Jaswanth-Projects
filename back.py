from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio
import os

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')  # Adjust model name if needed

# Define a class to store conversation context
class Reference:
    def __init__(self) -> None:
        self.response = ""

# Create an instance of Reference
reference = Reference()

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Query Gemini API function
def query_gemini(input_text):
    try:
        prompt = f"You are a helpful assistant. Please answer the following question clearly and accurately:\n{input_text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error during Gemini inference: {e}")
        return "An error occurred while generating a response."

# Clear the previous conversation
def clear_past():
    reference.response = ""

# Handlers for bot commands
@dp.message(Command(commands=["start"]))
async def start_handler(message: Message):
    await message.answer("Hi! I am Tele Bot! Created by Jaswanth Raaghav. Powered by Google Gemini API. How can I assist you?")

@dp.message(Command(commands=["help"]))
async def help_handler(message: Message):
    help_text = (
        "Hi! I'm your AI-powered Telegram bot. Here are my commands:\n"
        "/start - Start a conversation\n"
        "/clear - Clear the past conversation and context\n"
        "/help - Show this help message\n"
        "You can also send me any message, and I'll try to help!"
    )
    await message.answer(help_text)

@dp.message(Command(commands=["clear"]))
async def clear_handler(message: Message):
    clear_past()
    await message.answer("I've cleared the past conversation and context.")

@dp.message()
async def chat_handler(message: Message):
    user_input = message.text
    print(f"USER: {user_input}")
    
    full_input = f"{reference.response}\nUser: {user_input}" if reference.response else user_input
    response = query_gemini(full_input)
    
    reference.response = f"{reference.response}\nUser: {user_input}\nBot: {response}" if reference.response else f"User: {user_input}\nBot: {response}"
    
    print(f"GEMINI: {response}")
    await message.answer(response)

# Bot startup
async def on_startup():
    print("Bot is up and running!")

async def main():
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
