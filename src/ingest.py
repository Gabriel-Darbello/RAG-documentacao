from sentence_transformers import SentenceTransformer
import os, re, chromadb

def load_docs(directory:str) -> list[dict]:
    docs = []
    for file in os.listdir(directory):
        if file.endswith(".md"):
            path = os.path.join(directory, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                docs.append({"arquivo": file, "conteudo": content})
    return docs

def chunker(content:str, file:str) -> list[dict]:
    chunks = re.split(r'\n(?=##)', content)
    return[
        {'texto': chunk.strip(), "fonte":file}
        for chunk in chunks
        if len(chunk.strip()) > 100
    ]


embedding_model = SentenceTransformer("all-MiniLm-L6-v2")
docs = load_docs("data/docs")
file_chunks = []
for doc in docs:
    chunks = chunker(doc["conteudo"], doc["arquivo"])
    file_chunks.extend(chunks)

chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection("fastapi_docs")
print("Gerando embeddings e salvando no ChromaDB...")

for i, chunk in enumerate(file_chunks):
    embedding = embedding_model.encode(chunk["texto"]).tolist()
    collection.add(
        documents=[chunk["texto"]],
        embeddings=[embedding],
        metadatas=[{"fonte": chunk["fonte"]}],
        ids=[f"chunk_{i}"]
    )
    print(f"  [{i+1}/{len(file_chunks)}] {chunk['fonte']}")

print("\nIngestão concluída!")
print(f"Total salvo: {collection.count()} chunks")
