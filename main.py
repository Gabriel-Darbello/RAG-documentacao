from src.chat import send_message

print("FastAPI Docs Assistant")
print("Digite 'sair' para encerrar\n")

while True:
    message = input("Você: ")

    if message.lower() == "sair":
        break

    if not message.strip():
        continue

    response = send_message(message)
    print(f"\nAssistente: {response}\n")
