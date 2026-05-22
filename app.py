from fastapi import FastAPI, Query, HTTPException
from buscar import buscar

app = FastAPI(
    title="Motor de búsqueda semántica",
    description="API para búsqueda semántica de artículos usando embeddings de OpenAI",
    version="1.0.0"
)

@app.get("/", tags=["info"])
def root():
    """Endpoint raíz con información de la API"""
    return {
        "nombre": "Motor de búsqueda semántica",
        "versión": "1.0.0",
        "endpoints": [
            {"url": "/buscar", "método": "GET", "descripción": "Buscar documentos similares"},
            {"url": "/docs", "método": "GET", "descripción": "Documentación interactiva (Swagger)"}
        ]
    }

@app.get("/buscar", tags=["búsqueda"])
def buscar_endpoint(
    q: str = Query(..., min_length=2, description="Texto de búsqueda"), 
    n: int = Query(3, ge=1, le=10, description="Número de resultados (máximo 10)")
):
    """
    Busca documentos similares en la base de datos.
    
    - **q**: Texto de búsqueda (mínimo 2 caracteres)
    - **n**: Número de resultados a retornar (default: 3, máximo: 10)
    
    Retorna una lista de documentos ordenados por similitud semántica.
    """
    try:
        resultados = buscar(q, n_resultados=n)
        return {
            "query": q,
            "num_resultados": len(resultados),
            "resultados": resultados
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la búsqueda: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)