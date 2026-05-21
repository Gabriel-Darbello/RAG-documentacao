import os
from groq import Groq
from dotenv import load_dotenv
from src.retriever import search

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def send_message(message:str) -> str:
    chunks = search(message)

    context = "\n\n".join([
        f"Fonte: {chunk["fonte"]}\n{chunk["texto"]}"
        for chunk in chunks
    ])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"Você é um assistente especialista em FastAPI,\
                  não use marcações markdown e utilize explicações resumidas pois sua mensagem sera enviada no terminal.\
                    Responda com base na documentação abaixo:\n\n{context}"
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content
