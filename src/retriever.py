import chromadb
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection("fastapi_docs")

def search(message:str, n_results:int = 3) -> list[dict]:
    embedding = embedding_model.encode(message).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "texto": results["documents"][0][i],
            "fonte": results["metadatas"][0][i]['fonte']
        })
    return chunks
