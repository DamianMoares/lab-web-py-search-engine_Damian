import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb
import tiktoken
from articulos import articulos

load_dotenv()

MODEL = "text-embedding-3-small"
DB_DIR = "chroma_db"
COLLECTION_NAME = "articulos"
COST_PER_1M_TOKENS = 0.02

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
encoding = tiktoken.get_encoding("cl100k_base")

def contar_tokens(texto: str) -> int:
    return len(encoding.encode(texto))

def costo_estimado(total_tokens: int) -> float:
    return (total_tokens / 1_000_000) * COST_PER_1M_TOKENS

def obtener_coleccion():
    chroma_client = chromadb.PersistentClient(path=DB_DIR)
    return chroma_client.get_or_create_collection(name=COLLECTION_NAME)

def obtener_ids_indexados():
    """Obtiene los IDs de documentos ya indexados en ChromaDB."""
    try:
        collection = obtener_coleccion()
        todos = collection.get()
        return set(todos["ids"]) if todos["ids"] else set()
    except:
        return set()

def main(modo="incremental"):
    """
    Indexa artículos en ChromaDB.
    
    Args:
        modo: "incremental" para indexar solo nuevos (default), "full" para reindexar todo
    """
    collection = obtener_coleccion()
    
    # Obtener IDs ya indexados
    ids_indexados = obtener_ids_indexados()
    
    # Filtrar artículos a indexar
    if modo == "incremental":
        articulos_a_indexar = [a for a in articulos if a["id"] not in ids_indexados]
        if not articulos_a_indexar:
            print("✓ Base de datos actualizada. No hay nuevos artículos para indexar.")
            return
        print(f"📌 Indexando {len(articulos_a_indexar)} artículo(s) nuevo(s) de {len(articulos)} total(es)")
    else:
        articulos_a_indexar = articulos
        print(f"📌 Reindexando los {len(articulos)} artículos (modo: full)")

    ids = []
    documentos = []
    metadatas = []
    total_tokens = 0

    for articulo in articulos_a_indexar:
        texto = f"{articulo['titulo']}. {articulo['contenido']}"
        total_tokens += contar_tokens(texto)

        ids.append(articulo["id"])
        documentos.append(texto)
        metadatas.append({
            "id": articulo["id"],
            "titulo": articulo["titulo"]
        })

    respuesta = client.embeddings.create(
        model=MODEL,
        input=documentos
    )

    embeddings = [item.embedding for item in respuesta.data]

    collection.upsert(
        ids=ids,
        documents=documentos,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"✓ Indexación completada")
    print(f"  - Tokens procesados: {total_tokens}")
    print(f"  - Coste estimado: ${costo_estimado(total_tokens):.6f}")
    print(f"  - Total en BD: {len(obtener_ids_indexados())} artículos")

if __name__ == "__main__":
    import sys
    modo = sys.argv[1] if len(sys.argv) > 1 else "incremental"
    main(modo=modo)