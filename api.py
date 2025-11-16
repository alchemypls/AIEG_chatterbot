import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("api_key")

genai = genai.Client(api_key=api_key)

def super_chatter_bot(prompt: str) -> str:
    response = genai.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    bot_response = super_chatter_bot(user_prompt)
    print("Chatterbot Response:", bot_response)