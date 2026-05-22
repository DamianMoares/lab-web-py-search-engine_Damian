![logo_ironhack_blue 7](https://user-images.githubusercontent.com/23629340/40541063-a07a0a8a-601a-11e8-91b5-2f13e4e6b441.png)

# Lab | Motor de búsqueda semántica

## Objetivo

Construir un motor de búsqueda semántica sobre una colección de textos usando embeddings de OpenAI y ChromaDB para almacenar y recuperar documentos basados en similitud semántica.

## 🚀 Inicio rápido

### 1. Configuración del entorno

```bash
# Clonar el repositorio
cd lab-web-py-search-engine

# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (macOS/Linux)
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tu clave de OpenAI
# OPENAI_API_KEY=sk-proj-xxxxx
```

Obtén tu API key en: https://platform.openai.com/api-keys

## Dataset

Colección de 8 artículos sobre tecnología:

| ID | Título | Tema |
|---|---|---|
| 1 | FastAPI vs Flask | Frameworks web Python |
| 2 | React vs Vue | Frameworks frontend |
| 3 | PostgreSQL para principiantes | Bases de datos |
| 4 | Introducción a los LLMs | Modelos de lenguaje |
| 5 | Despliegue con Docker | Containerización |
| 6 | Autenticación JWT | Seguridad |
| 7 | LangChain para agentes | Herramientas LLM |
| 8 | Python vs JavaScript para IA | Lenguajes de programación |

## 📚 Estructura del Proyecto

```
lab-web-py-search-engine/
├── articulos.py          # Datos de los artículos
├── indexar.py            # Script para crear embeddings e indexar
├── buscar.py             # Función de búsqueda semántica
├── app.py                # API FastAPI (bonus)
├── analisis.ipynb        # Notebook de análisis y visualización
├── requirements.txt      # Dependencias Python
├── .env                  # Variables de entorno (no commitear)
├── .env.example          # Ejemplo de .env
├── chroma_db/            # Base de datos ChromaDB (generada)
└── README.md             # Este archivo
```

## 📋 Parte 1: Indexación

### Crear embeddings e indexar artículos

```bash
# Indexación incremental (solo nuevos artículos)
python indexar.py

# Reindexar todos los artículos
python indexar.py full
```

**Salida esperada:**
```
📌 Indexando 8 artículo(s) nuevo(s) de 8 total(es)
✓ Indexación completada
  - Tokens procesados: 1234
  - Coste estimado: $0.000045
  - Total en BD: 8 artículos
```

**Características:**
- ✅ Indexación incremental (no reindexea si existe)
- ✅ Calcula tokens procesados
- ✅ Estima coste de API
- ✅ Almacena en ChromaDB con metadatos

## 🔍 Parte 2: Búsqueda Semántica

### Buscar documentos similares

```bash
python buscar.py
```

O en Python:

```python
from buscar import buscar

# Búsqueda básica
resultados = buscar("¿cómo hacer una API en Python?", n_resultados=3)

# Mostrar resultados
for r in resultados:
    print(f"[{r['score']:.4f}] {r['titulo']}")
```

**Queries de prueba:**
- "¿cómo hacer una API en Python?"
- "diferencias entre frameworks de frontend"
- "cómo funciona la autenticación en aplicaciones web"
- "herramientas para trabajar con modelos de lenguaje"

**Salida esperada:**
```
[0.8234] FastAPI vs Flask
[0.6123] LangChain para agentes
[0.5891] Python vs JavaScript para IA
```

## 📊 Parte 3: Notebook de Análisis

### Visualizaciones y análisis

```bash
jupyter notebook analisis.ipynb
```

**Contenidos del notebook:**
1. 📈 Tabla comparativa: query → mejor resultado → score
2. 📊 Gráfico de barras con scores de similitud
3. 🔥 Mapa de calor de similitud entre artículos
4. 📋 Tabla detallada con todos los resultados

## 🎁 Funcionalidades Bonus

### 1. API FastAPI

```bash
# Iniciar servidor
uvicorn app:app --reload

# Probar endpoint
curl "http://localhost:8000/buscar?q=API%20Python&n=3"
```

**Response:**
```json
{
  "query": "API Python",
  "resultados": [
    {
      "id": "1",
      "titulo": "FastAPI vs Flask",
      "documento": "...",
      "score": 0.8234
    }
  ]
}
```

### 2. Búsqueda por múltiples campos

```python
from buscar import buscar

# Buscar en contenido
resultados = buscar("Docker", buscar_en="contenido")

# Búsqueda futura en títulos
resultados = buscar("vs", buscar_en="titulo")
```

### 3. Indexación incremental

```python
from indexar import main

# Solo indexa nuevos artículos
main(modo="incremental")

# Reindexar todo
main(modo="full")
```

## 🔧 Tecnologías

| Herramienta | Propósito |
|---|---|
| **OpenAI** | Embeddings con text-embedding-3-small |
| **ChromaDB** | Base de datos vectorial persistente |
| **Python-dotenv** | Gestión de variables de entorno |
| **Tiktoken** | Contador de tokens |
| **FastAPI** | API REST (bonus) |
| **Pandas & Matplotlib** | Análisis y visualización |

## 📈 Ejemplo de Uso Completo

```bash
# 1. Activar entorno
source venv/bin/activate

# 2. Indexar artículos (primera vez)
python indexar.py

# 3. Hacer búsquedas
python buscar.py

# 4. Análisis en Jupyter
jupyter notebook analisis.ipynb

# 5. (Opcional) Iniciar API
uvicorn app:app --reload
```

## 📝 Notas

- **ChromaDB**: Se almacena en el directorio `chroma_db/`
- **Costes**: El modelo `text-embedding-3-small` cuesta $0.02 por 1M tokens
- **Límites**: API de OpenAI tiene límites de rate
- **Privacidad**: Nunca commitees tu `.env` con la API key