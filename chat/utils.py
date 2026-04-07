from groq import Groq
import os 
from dotenv import load_dotenv

# This loads the variables from .env into your system environment
load_dotenv()

# os.getenv looks for the variable "GROQ_API_KEY" 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# def llm_call(messages):
#     response = client.chat.completions.create(
#         # model="llama-3.1-8b-instant",
#         model="meta-llama/llama-4-scout-17b-16e-instruct",
#         messages=messages
#     )
#     return response.choices[0].message.content


def llm_call(messages):
    try:
        # SYSTEM PROMPT (MEMORY + IMAGE AWARENESS)
        system_prompt = {
    "role": "system",
    "content": (
        "You are a helpful AI assistant.\n\n"

        "RESPONSE RULES:\n"
        "1. Keep responses clear and concise.\n"
        "2. Avoid unnecessary explanations.\n"
        "3. Use bullet points when listing information.\n"
        "4. Use headings when needed.\n"
        "5. Do NOT repeat the question.\n"
        "6. If the answer is simple, keep it short.\n"
        "7. For image descriptions, structure output clearly.\n\n"

        "MEMORY RULES:\n"
        "If previous messages contain image descriptions, treat them as real images.\n"
    )}
        # PREPEND SYSTEM PROMPT
        final_messages = [system_prompt] + messages

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=final_messages,
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM Error: {str(e)}"
