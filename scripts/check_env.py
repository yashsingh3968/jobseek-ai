import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

assert key, "GEMINI_API_KEY is not set"

print("Key loaded, length:", len(key))