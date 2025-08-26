# Optimización del Sistema RAG - Session Management

## Problema Inicial

El código original en `ask.py` era ineficiente porque en cada pregunta se estaba:

1. **Cargando las embeddings** desde cero
2. **Cargando el vectorstore** desde disco (índice FAISS)
3. **Inicializando el modelo LLM** 
4. **Construyendo la cadena RAG**

Esto significaba que cada pregunta tenía una latencia alta y uso innecesario de recursos.

## Solución Implementada

### 1. Sistema de Sesión con Caché Inteligente

Se ha creado una nueva clase `RAGSession` en `atlasqaxai/rag/session.py` que:

- **Mantiene en memoria** todos los componentes RAG cargados
- **Detecta automáticamente** cuando necesita recargar los componentes
- **Invalida la caché** cuando es necesario

### 2. Detección Automática de Cambios

La sesión detecta cambios en:

- **Archivos del índice**: Monitorea `index.faiss` y `index.pkl` por tiempo de modificación
- **Configuración**: Detecta cambios en variables de entorno (modelos, parámetros)
- **Estado de componentes**: Verifica si algún componente está faltante

### 3. Invalidación Manual

Los comandos que modifican el índice ahora invalidan la sesión:

- **`ingest.py`**: Invalida después de añadir nuevos documentos
- **`wipe.py`**: Invalida después de borrar el índice
- **`rebuild.py`**: Ya usa `wipe` + `ingest`, por lo que se invalida automáticamente

## Beneficios

### **Rendimiento Mejorado**
- **Primera pregunta**: Carga inicial (tiempo normal)
- **Preguntas subsecuentes**: Uso inmediato de componentes cacheados
- **Reducción significativa** en latencia para preguntas consecutivas

### **Detección Automática de Cambios**
- No requiere reiniciar la aplicación después de indexar
- Recarga automática cuando detecta cambios en el índice
- Mantiene consistencia de datos

### **Flexibilidad**
- Funciona con interfaz CLI y Streamlit
- Invalidación manual disponible si es necesaria
- Logging detallado para debugging

### **Compatibilidad Total**
- No requiere cambios en el código existente de la UI
- Los comandos existentes funcionan igual que antes
- API backward-compatible

## Uso

### Automático (Recomendado)
```python
# En ask.py - ahora optimizado
from ..rag import session

def run(question: str):
    rag_session = session.get_session()
    chain = rag_session.get_chain()  # Caché automático
    response = chain.invoke(question)
    return response
```

### Manual (Para casos especiales)
```python
from atlasqaxai.rag import session

# Forzar recarga si es necesario
session.get_session().force_reload()

# Verificar estado
status = session.get_session().get_status()
print(status)
```

## Flujo de Trabajo Optimizado

1. **Primera pregunta**: Carga todos los componentes
2. **Preguntas subsecuentes**: Uso directo del caché
3. **Nuevo indexado**: Detección automática + recarga
4. **Cambio de configuración**: Detección automática + recarga

## Archivos Modificados

- **`atlasqaxai/rag/session.py`** *(nuevo)*: Sistema de sesión
- **`atlasqaxai/commands/ask.py`**: Usa la sesión
- **`atlasqaxai/commands/ingest.py`**: Invalida después de indexar
- **`atlasqaxai/commands/wipe.py`**: Invalida después de borrar
- **`atlasqaxai/rag/__init__.py`**: Expone la sesión
- **`test_session.py`** *(nuevo)*: Script de prueba

## Testing

Ejecutar el script de prueba:

```bash
cd /home/pagusti/git-repos/atlasqaxai
python test_session.py
```

Este script verifica:
- Carga inicial de componentes
- Funcionamiento del caché
- Invalidación manual
- Estado de la sesión

## Consideraciones Técnicas

- **Thread-safe**: La implementación actual asume uso single-thread
- **Memoria**: Los componentes permanecen en memoria (diseño intencional para performance)
- **Detección de cambios**: Basada en timestamps de archivos y hash de configuración
- **Logging**: Mensajes informativos para tracking de cargas/recargas
