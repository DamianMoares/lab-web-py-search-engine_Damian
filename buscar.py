import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

load_dotenv()

MODEL = "text-embedding-3-small"
DB_DIR = "chroma_db"
COLLECTION_NAME = "articulos"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def obtener_coleccion():
    chroma_client = chromadb.PersistentClient(path=DB_DIR)
    return chroma_client.get_or_create_collection(name=COLLECTION_NAME)

def buscar(query, n_resultados=3, buscar_en="contenido"):
    """
    Busca documentos similares a la query en ChromaDB.
    
    Args:
        query: Texto de búsqueda
        n_resultados: Número de resultados a retornar (default: 3)
        buscar_en: Campo de búsqueda - "contenido", "titulo" o "ambos" (default: "contenido")
    
    Returns:
        Lista de resultados con id, titulo, documento y score de similitud
    """
    collection = obtener_coleccion()

    emb = client.embeddings.create(
        model=MODEL,
        input=query
    ).data[0].embedding

    resultados = collection.query(
        query_embeddings=[emb],
        n_results=n_resultados,
        include=["documents", "metadatas", "distances"]
    )

    salida = []
    for i in range(len(resultados["ids"][0])):
        distancia = resultados["distances"][0][i]
        salida.append({
            "id": resultados["ids"][0][i],
            "titulo": resultados["metadatas"][0][i]["titulo"],
            "documento": resultados["documents"][0][i],
            "score": 1 - distancia
        })
    return salida

if __name__ == "__main__":
    queries = [
        "¿cómo hacer una API en Python?",
        "diferencias entre frameworks de frontend",
        "cómo funciona la autenticación en aplicaciones web",
        "herramientas para trabajar con modelos de lenguaje"
    ]

    for q in queries:
        print(f"\nQUERY: {q}")
        for r in buscar(q):
            print(r)