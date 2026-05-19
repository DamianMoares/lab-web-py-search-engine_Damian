# Lab D4 — Motor de búsqueda semántica

## Objetivo

Construir un motor de búsqueda semántica sobre una colección de textos usando embeddings.

## Setup

```bash
# fork & clone the repository
cd lab-web-py-search-engine
python -m venv venv
source venv/bin/activate
pip install openai chromadb python-dotenv tiktoken
pip freeze > requirements.txt
```

```bash
# .env
OPENAI_API_KEY=tu-clave-aqui
```

## Dataset

Usa esta colección de artículos de tecnología (puedes ampliarla):

```python
articulos = [
    {"id": "1", "titulo": "FastAPI vs Flask", "contenido": "FastAPI ofrece validación automática con Pydantic, documentación Swagger integrada y mejor rendimiento asíncrono que Flask."},
    {"id": "2", "titulo": "React vs Vue", "contenido": "React tiene un ecosistema más grande y es mantenido por Meta. Vue tiene una curva de aprendizaje más suave y una sintaxis más intuitiva."},
    {"id": "3", "titulo": "PostgreSQL para principiantes", "contenido": "PostgreSQL es una base de datos relacional open source con soporte para JSON, búsqueda de texto completo y extensiones como pgvector."},
    {"id": "4", "titulo": "Introducción a los LLMs", "contenido": "Los Large Language Models son redes neuronales entrenadas para predecir la siguiente palabra. GPT-4, Claude y Gemini son ejemplos populares."},
    {"id": "5", "titulo": "Despliegue con Docker", "contenido": "Docker permite empaquetar aplicaciones en contenedores que se ejecutan de forma consistente en cualquier entorno."},
    {"id": "6", "titulo": "Autenticación JWT", "contenido": "JSON Web Tokens permiten transmitir información verificada entre partes. Se usan para autenticación stateless en APIs REST."},
    {"id": "7", "titulo": "LangChain para agentes", "contenido": "LangChain simplifica la construcción de aplicaciones con LLMs, proporcionando abstracciones para cadenas, agentes y memoria."},
    {"id": "8", "titulo": "Python vs JavaScript para IA", "contenido": "Python domina el ecosistema de IA gracias a librerías como NumPy, PyTorch y HuggingFace. JavaScript tiene opciones como TensorFlow.js pero es menos maduro."},
]
```

## Parte 1: Indexación

Crea `indexar.py` que:

1. Cargue los artículos
2. Cree embeddings para el campo `contenido` de cada uno
3. Los almacene en ChromaDB con metadatos (titulo, id)
4. Imprima el número de tokens procesados y el coste estimado

## Parte 2: Búsqueda

Crea `buscar.py` con una función `buscar(query, n_resultados=3)` que:

1. Cree el embedding de la query
2. Busque los N documentos más similares en ChromaDB
3. Devuelva los resultados con el score de similitud

Prueba con estas queries:
- "¿cómo hacer una API en Python?"
- "diferencias entre frameworks de frontend"
- "cómo funciona la autenticación en aplicaciones web"
- "herramientas para trabajar con modelos de lenguaje"

## Parte 3: Notebook de análisis

Crea `analisis.ipynb` que visualice:

1. Las queries de prueba y sus resultados
2. Una tabla comparativa: query → mejor resultado → score de similitud
3. (Bonus) Un mapa de calor de similitud entre todos los artículos

## Bonus

- Añade búsqueda por `titulo` además del `contenido`
- Implementa un endpoint FastAPI `GET /buscar?q=` que use este motor
- Haz que la indexación sea incremental (no reindexe si el artículo ya existe)