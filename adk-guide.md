# Guía Completa: Google Agent Development Kit (ADK) - Versión Actualizada

Esta guía proporciona un análisis técnico completo de Google Agent Development Kit (ADK), combinando ejemplos prácticos del repositorio ADK Crash Course con la documentación oficial completa. Diseñada para servir como referencia técnica integral para el desarrollo de nuevos proyectos con Google ADK.

## Índice

1. [Introducción General](#introducción-general)
2. [Configuración Base](#configuración-base)
3. [Análisis de Ejemplos](#análisis-de-ejemplos)
4. [Patrones de Arquitectura](#patrones-de-arquitectura)
5. [Herramientas (Tools)](#herramientas-tools)
6. [Sesiones y Memoria](#sesiones-y-memoria)
7. [Callbacks](#callbacks)
8. [Artifacts](#artifacts)
9. [Streaming y Comunicación en Tiempo Real](#streaming-y-comunicación-en-tiempo-real)
10. [Seguridad y Safety](#seguridad-y-safety)
11. [Evaluación de Agentes](#evaluación-de-agentes)
12. [Deployment](#deployment)
13. [Grounding](#grounding)
14. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
15. [Limitaciones y Consideraciones](#limitaciones-y-consideraciones)
16. [Buenas Prácticas](#buenas-prácticas)
17. [Casos de Uso por Tipo de Agente](#casos-de-uso-por-tipo-de-agente)
18. [Consideraciones de Producción](#consideraciones-de-producción)
19. [Recursos Adicionales](#recursos-adicionales)

## Introducción General

Google Agent Development Kit (ADK) es un framework flexible y modular para desarrollar y desplegar agentes de IA. Aunque está optimizado para Gemini y el ecosistema de Google, ADK es agnóstico al modelo y al deployment, construido para compatibilidad con otros frameworks. ADK fue diseñado para hacer que el desarrollo de agentes se sienta más como desarrollo de software tradicional.

### Características Principales

- **Orquestación Flexible**: Define flujos de trabajo usando agentes de workflow (Sequential, Parallel, Loop) para pipelines predecibles, o aprovecha el enrutamiento dinámico impulsado por LLM.
- **Arquitectura Multi-Agente**: Construye aplicaciones modulares y escalables componiendo múltiples agentes especializados en una jerarquía.
- **Ecosistema Rico de Herramientas**: Equipa a los agentes con diversas capacidades usando herramientas pre-construidas, funciones personalizadas, bibliotecas de terceros, o incluso otros agentes como herramientas.
- **Listo para Deployment**: Conteneriza y despliega tus agentes en cualquier lugar - ejecuta localmente, escala con Vertex AI Agent Engine, o integra en infraestructura personalizada.
- **Evaluación Integrada**: Evalúa sistemáticamente el rendimiento del agente evaluando tanto la calidad de la respuesta final como la trayectoria de ejecución paso a paso.
- **Construcción de Agentes Seguros**: Aprende a construir agentes poderosos y confiables implementando patrones de seguridad y mejores prácticas.

### Conceptos Fundamentales

- **Root Agent (Agente Raíz)**: Todo setup ADK debe tener al menos un agente raíz que sirve como punto de entrada para todas las solicitudes
- **LlmAgent**: El componente central que actúa como la "mente" del sistema, usando LLMs para razonamiento y toma de decisiones
- **Herramientas (Tools)**: Extensiones que permiten a los agentes interactuar con sistemas externos (Function Calling, Built-in, Third-party)
- **Estado y Sesiones**: Mecanismos para mantener contexto entre interacciones mediante diccionarios key-value persistentes
- **Multi-Agent Systems**: Arquitecturas donde múltiples agentes especializados colaboran mediante **delegación completa**
- **Workflow Agents**: Agentes que ejecutan sub-agentes en patrones específicos (secuencial, paralelo, loop)
- **Runner**: Componente que orquesta agentes y sesiones para procesar solicitudes y generar respuestas
- **Callbacks**: Puntos de control en el ciclo de vida del agente para insertar lógica personalizada
- **Artifacts**: Mecanismo para manejar datos binarios nombrados y versionados
- **Streaming**: Capacidad de comunicación bidireccional en tiempo real con voz y video

## Configuración Base

### Estructura de Proyecto Requerida

**⚠️ CRÍTICO**: El nombre del agente (`name`) debe coincidir **exactamente** con el nombre de la carpeta que lo contiene.

```
proyecto/
├── agent_folder/           # Directorio del agente (nombre debe coincidir)
│   ├── __init__.py        # OBLIGATORIO: from . import agent
│   ├── agent.py           # OBLIGATORIO: root_agent = Agent(...)
│   └── .env               # Variables de entorno (solo en raíz)
├── requirements.txt        # Dependencias del proyecto
└── tests/                  # Tests del agente
    ├── unit/
    └── integration/
```

**Reglas Fundamentales**:
- `__init__.py` debe importar el módulo agent: `from . import agent`
- `agent.py` debe definir una variable llamada `root_agent`
- Solo se necesita un `.env` en la carpeta del agente raíz (multi-agente)
- Ejecutar `adk` siempre desde el directorio padre, nunca desde dentro del agente

### Instalación

#### Crear y activar entorno virtual (recomendado):
```bash
# Crear
python -m venv .venv

# Activar (cada nuevo terminal)
# macOS/Linux
source .venv/bin/activate
# Windows CMD
.venv\Scripts\activate.bat
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

#### Instalar ADK:
```bash
pip install google-adk

# Verificar instalación (opcional)
adk --version
```

### Dependencias Core

```txt
google-adk[database]==0.3.0    # Framework principal + soporte DB
google-generativeai==0.8.5     # Modelos Gemini
python-dotenv==1.1.0           # Variables de entorno
litellm==1.66.3                # Integración multi-modelo (opcional)
yfinance==0.2.56               # Para ejemplos financieros
psutil==5.9.5                  # Para monitoreo de sistema
```

### Modelos Disponibles

#### Modelos Gemini (Google AI Studio / Vertex AI)
- **Gemini 2.5 Pro**: El más inteligente, mejor para tareas complejas
- **Gemini 2.5 Flash**: Balance entre velocidad e inteligencia
- **Gemini 2.0 Flash**: Rápido pero menos inteligente, ideal para producción
- **Gemini 2.0 Flash Live**: Para streaming de voz/video
- **Gemini 2.0 No Flash**: Características multimodales, 1M tokens de contexto

#### Modelos compatibles con streaming (voz/video)
Para usar streaming en ADK, necesitas modelos que soporten la API Live de Gemini. Verifica la compatibilidad en la [documentación de modelos](https://ai.google.dev/api/models#method:-models.list).

### Configuración API

#### Google AI Studio (más simple para desarrollo)
```python
# En .env
GOOGLE_API_KEY=your_api_key_here
```

#### Vertex AI (recomendado para producción)
```python
# En .env
VERTEX_PROJECT_ID=your-project-id
VERTEX_LOCATION=us-central1

# Autenticación desde terminal
gcloud auth login
```

#### Para LiteLLM (modelos no-Google)
```python
# En .env
OPENROUTER_API_KEY=your_openrouter_key_here
```

## Análisis de Ejemplos

### 1. Basic Agent (Agente Básico)

**Ubicación**: `1-basic-agent/greeting_agent/`

**Propósito**: Demostrar la implementación más simple de un agente ADK.

**Componentes Clave**:
```python
from google.adk.agents import Agent

root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash",
    description="Greeting agent",
    instruction="""
    You are a helpful assistant that greets the user. 
    Ask for the user's name and greet them by name.
    """,
)
```

**Lecciones Técnicas**:
- La variable `root_agent` es **obligatoria** para que ADK descubra el agente
- El parámetro `instruction` es crítico para definir el comportamiento
- Estructura mínima requerida: `__init__.py` que importa `agent.py`

**Caso de Uso**: Agentes conversacionales simples, prototipos, validación de concepto.

### 2. Tool Agent (Agente con Herramientas)

**Ubicación**: `2-tool-agent/tool_agent/`

**Propósito**: Demostrar integración de herramientas built-in y custom functions.

**Componentes Clave**:
```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Tool agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - google_search
    """,
    tools=[google_search],
)
```

**Limitaciones Importantes**:
- Solo **una herramienta built-in por agente** (google_search, code_execution, vertex_ai_search)
- **No se pueden mezclar** herramientas built-in con custom functions
- Para usar múltiples herramientas built-in, se requiere arquitectura multi-agente

**Buenas Prácticas para Custom Functions**:
```python
def custom_tool(param: str, tool_context: ToolContext) -> dict:
    """
    Descripción clara para el LLM.
    
    Args:
        param: Descripción del parámetro
        tool_context: Contexto para acceder al estado
    
    Returns:
        dict: Formato preferido {"status": "success", "result": "..."}
    """
    # No usar valores por defecto en parámetros
    # Retornar siempre diccionario
    return {"status": "success", "result": resultado}
```

**Caso de Uso**: Agentes que necesitan interactuar con APIs externas, buscar información en tiempo real, ejecutar código.

### 3. LiteLLM Agent (Integración Multi-Modelo)

**Ubicación**: `3-litellm-agent/dad_joke_agent/`

**Propósito**: Demostrar uso de modelos no-Google a través de LiteLLM.

**Componentes Clave**:
```python
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="openrouter/openai/gpt-4.1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

root_agent = Agent(
    name="dad_joke_agent",
    model=model,  # Usar modelo LiteLLM
    tools=[get_dad_joke],
)
```

**Limitaciones Críticas**:
- Modelos no-Google **NO pueden usar herramientas built-in** de ADK
- Solo funciones custom disponibles
- Útil para diversificación de modelos y optimización de costos

**Caso de Uso**: Proyectos que requieren múltiples modelos, optimización de costos, comparación de rendimiento entre proveedores.

### 4. Structured Outputs (Salidas Estructuradas)

**Ubicación**: `4-structured-outputs/email_agent/`

**Propósito**: Garantizar formato consistente usando Pydantic schemas.

**Componentes Clave**:
```python
from pydantic import BaseModel, Field

class EmailContent(BaseModel):
    subject: str = Field(description="Subject line description")
    body: str = Field(description="Email body description")

root_agent = LlmAgent(
    name="email_agent",
    model="gemini-2.0-flash",
    instruction="IMPORTANT: Your response MUST be valid JSON...",
    output_schema=EmailContent,
    output_key="email",  # Almacena en estado de sesión
)
```

**Limitaciones**:
- Agentes con `output_schema` **NO pueden usar herramientas**
- Debe producir JSON válido como respuesta final
- Requiere instrucciones explícitas sobre el formato JSON

**Caso de Uso**: Integración con sistemas externos, APIs que requieren formato específico, pipelines de datos estructurados.

### 5. Sessions and State (Sesiones y Estado)

**Ubicación**: `5-sessions-and-state/question_answering_agent/`

**Propósito**: Mantener contexto y estado entre interacciones.

**Componentes Clave**:
```python
# Definición del agente con variables de template
instruction="""
You are a helpful assistant.

User Information:
Name: {user_name}
Preferences: {user_preferences}
"""

# Configuración de sesión
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
initial_state = {
    "user_name": "Brandon Hancock",
    "user_preferences": "Preferences text...",
}

stateful_session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
```

**Funcionalidades**:
- Variables de template en instrucciones (`{variable_name}`)
- Estado mutable entre interacciones
- Historial automático de conversación

**Caso de Uso**: Chatbots personalizados, asistentes con memoria, aplicaciones que requieren continuidad de contexto.

### 6. Persistent Storage (Almacenamiento Persistente)

**Ubicación**: `6-persistent-storage/memory_agent/`

**Propósito**: Persiste estado en base de datos, sobrevive reinicio de aplicación.

**Componentes Clave**:
```python
from google.adk.sessions import DatabaseSessionService

# Configuración de base de datos
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# Herramientas que modifican estado
def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    reminders = tool_context.state.get("reminders", [])
    reminders.append(reminder)
    tool_context.state["reminders"] = reminders  # Auto-guardado
    return {"message": f"Added reminder: {reminder}"}
```

**Bases de Datos Soportadas**:
- SQLite: `sqlite:///./database.db`
- PostgreSQL: `postgresql://user:password@localhost/db`
- MySQL: `mysql://user:password@localhost/db`

**Gestión de Sesiones**:
```python
# Verificar sesiones existentes
existing_sessions = session_service.list_sessions(app_name, user_id)

# Usar sesión existente o crear nueva
if existing_sessions.sessions:
    SESSION_ID = existing_sessions.sessions[0].id
else:
    new_session = session_service.create_session(...)
```

**Caso de Uso**: Aplicaciones de producción, sistemas de CRM, asistentes personales de largo plazo.

### 7. Multi-Agent (Sistemas Multi-Agente)

**Ubicación**: `7-multi-agent/manager/`

**Propósito**: Orquestación de agentes especializados para tareas complejas.

**Dos Patrones Principales**:

#### Patrón 1: Sub-Agent Delegation
```python
# Delegación completa - sub-agente toma control total
root_agent = Agent(
    name="manager",
    instruction="Always delegate to appropriate agent...",
    sub_agents=[stock_analyst, funny_nerd],  # Delegación completa
)
```

#### Patrón 2: Agent-as-Tool
```python
from google.adk.tools.agent_tool import AgentTool

# Agente como herramienta - manager mantiene control
root_agent = Agent(
    name="manager",
    instruction="Use specialized agents as tools...",
    tools=[
        AgentTool(news_analyst),  # Resultado regresa al manager
        get_current_time,
    ],
)
```

**Limitaciones Críticas**:
- **Sub-agentes NO pueden usar herramientas built-in**
- Para múltiples herramientas built-in, usar patrón Agent-as-Tool

**Estructura de Directorios**:
```
manager/
├── __init__.py              # Importa agent.py
├── agent.py                 # Define root_agent
└── sub_agents/
    ├── __init__.py
    ├── agent1_folder/
    │   ├── __init__.py
    │   └── agent.py
    └── agent2_folder/
        ├── __init__.py
        └── agent.py
```

**Caso de Uso**: Sistemas complejos con múltiples dominios de expertise, customer service, plataformas de análisis.

### 8. Stateful Multi-Agent (Multi-Agente con Estado)

**Ubicación**: `8-stateful-multi-agent/customer_service_agent/`

**Propósito**: Combinar orquestación multi-agente con estado persistente compartido.

**Componentes Clave**:
```python
# Estado compartido entre todos los agentes
def initialize_state():
    return {
        "user_name": "Brandon Hancock",
        "purchased_courses": [""],
        "interaction_history": [],
    }

# Agentes especializados con acceso al mismo estado
customer_service_agent = Agent(
    name="customer_service",
    instruction="""
    User Information:
    Name: {user_name}
    Purchased Courses: {purchased_courses}
    Interaction History: {interaction_history}
    """,
    sub_agents=[policy_agent, sales_agent, course_support_agent, order_agent],
)
```

**Flujo de Trabajo**:
1. **Creación de sesión** con estado inicial
2. **Enrutamiento inteligente** basado en contenido de consulta
3. **Actualización de estado** por agentes especializados
4. **Personalización** basada en historial e información de usuario

**Caso de Uso**: Plataformas de servicio al cliente, sistemas de soporte técnico, aplicaciones empresariales complejas.

### 9. Callbacks (Ganchos de Eventos)

**Ubicación**: `9-callbacks/`

**Propósito**: Interceptar y modificar comportamiento en diferentes etapas de ejecución.

#### Tipos de Callbacks:

**Agent Callbacks**:
```python
def before_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    # Logging, validación, métricas
    state = callback_context.state
    state["request_counter"] = state.get("request_counter", 0) + 1
    return None  # Continuar con procesamiento normal

def after_agent_callback(callback_context: CallbackContext) -> Optional[types.Content]:
    # Post-procesamiento, cleanup
    return None
```

**Model Callbacks**:
```python
def before_model_callback(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Filtrado de contenido, modificación de prompts
    if contains_inappropriate_content(llm_request):
        return LlmResponse(content=create_rejection_response())
    return None  # Proceder normalmente

def after_model_callback(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    # Transformación de respuestas
    response_text = llm_response.content.parts[0].text
    modified_text = apply_filters(response_text)
    llm_response.content.parts[0].text = modified_text
    return llm_response
```

**Tool Callbacks**:
```python
def before_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    # Modificación de argumentos, validación
    if args.get("country") == "USA":
        args["country"] = "United States"
    return None

def after_tool_callback(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict) -> Optional[Dict]:
    # Enriquecimiento de respuestas
    enhanced_response = copy.deepcopy(tool_response)
    enhanced_response["metadata"] = add_metadata(tool_response)
    return enhanced_response
```

**Caso de Uso**: Logging y monitoreo, filtrado de contenido, cumplimiento normativo, transformación de datos.

### 10. Sequential Agent (Agente Secuencial)

**Ubicación**: `10-sequential-agent/lead_qualification_agent/`

**Propósito**: Ejecutar sub-agentes en orden fijo, cada uno alimentando al siguiente.

**Componentes Clave**:
```python
from google.adk.agents import SequentialAgent

# Pipeline de calificación de leads
root_agent = SequentialAgent(
    name="lead_qualification_agent",
    model="gemini-2.0-flash",
    description="Lead qualification pipeline",
    instruction="Execute the following agents in sequence...",
    sub_agents=[
        validator_agent,    # Valida información completa
        scorer_agent,       # Asigna puntuación 1-10
        recommender_agent,  # Sugiere acciones basadas en score
    ],
)
```

**Sub-Agente con Output Key**:
```python
validator_agent = LlmAgent(
    name="validator",
    output_schema=ValidationResult,
    output_key="validation_status",  # Disponible para siguientes agentes
)
```

**Flujo de Datos**:
1. Validator evalúa → guarda resultado en `validation_status`
2. Scorer accede a `validation_status` → guarda en `lead_score`  
3. Recommender accede a ambos → genera `action_recommendation`

**Caso de Uso**: Pipelines de procesamiento, workflows de aprobación, análisis multi-etapa.

### 11. Parallel Agent (Agente Paralelo)

**Ubicación**: `11-parallel-agent/system_monitor_agent/`

**Propósito**: Ejecutar sub-agentes concurrentemente para mejorar rendimiento.

**Componentes Clave**:
```python
from google.adk.agents import ParallelAgent, SequentialAgent

# Recolección paralela de información
system_info_gatherer = ParallelAgent(
    name="system_info_gatherer",
    model="gemini-2.0-flash",
    description="Gather system information in parallel",
    sub_agents=[
        cpu_info_agent,     # Ejecuta concurrentemente
        memory_info_agent,  # Ejecuta concurrentemente  
        disk_info_agent,    # Ejecuta concurrentemente
    ],
)

# Pipeline híbrido: paralelo + secuencial
root_agent = SequentialAgent(
    name="system_monitor_agent",
    sub_agents=[
        system_info_gatherer,    # Recolección paralela
        synthesizer_agent,       # Síntesis secuencial
    ],
)
```

**Herramientas de Sistema**:
```python
def get_cpu_info() -> dict:
    import psutil
    return {
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "load_average": psutil.getloadavg(),
    }
```

**Características**:
- **Ejecución independiente**: Sub-agentes no comparten estado durante ejecución
- **Mejor rendimiento**: Ideal para tareas independientes
- **Recolección de resultados**: Resultados combinados después de ejecución paralela

**Caso de Uso**: Monitoreo de sistemas, análisis de datos paralelo, investigación web distribuida.

### 12. Loop Agent (Agente con Bucle)

**Ubicación**: `12-loop-agent/linkedin_post_agent/`

**Propósito**: Refinamiento iterativo hasta cumplir criterios de calidad.

**Componentes Clave**:
```python
from google.adk.agents import LoopAgent, SequentialAgent

# Pipeline con refinamiento iterativo
root_agent = SequentialAgent(
    name="linkedin_post_pipeline",
    sub_agents=[
        initial_generator,     # Genera post inicial
        refinement_loop,       # Refina iterativamente
    ],
)

# Bucle de refinamiento
refinement_loop = LoopAgent(
    name="post_refinement_loop",
    max_iterations=10,
    sub_agents=[
        post_reviewer,    # Evalúa calidad + posible exit
        post_refiner,     # Mejora basada en feedback
    ],
)
```

**Control de Bucle con Exit Tool**:
```python
def exit_loop(final_post: str, tool_context: ToolContext) -> dict:
    """Exit the loop when quality criteria are met."""
    tool_context.actions.escalate = True  # Señal para terminar bucle
    return {"status": "loop_exited", "final_post": final_post}

post_reviewer = Agent(
    name="post_reviewer",
    instruction="""
    Evaluate post quality. If all criteria are met, 
    call exit_loop tool. Otherwise, provide feedback.
    """,
    tools=[character_counter, exit_loop],
)
```

**Flujo de Refinamiento**:
1. **Generación inicial** de contenido
2. **Evaluación de calidad** con criterios específicos
3. **Exit o refinamiento** basado en evaluación
4. **Mejora iterativa** hasta alcanzar calidad deseada

**Caso de Uso**: Generación de contenido de alta calidad, procesos de revisión automática, optimización iterativa.

## Herramientas (Tools)

### ¿Qué es una Tool?

En ADK, una Tool representa una capacidad específica proporcionada a un agente IA, permitiéndole realizar acciones e interactuar con el mundo más allá de sus capacidades básicas de generación de texto y razonamiento.

### Características Clave

- **Orientadas a la acción**: Las herramientas realizan tareas específicas como consultar bases de datos, hacer requests API, buscar en la web, ejecutar código
- **Extienden capacidades del agente**: Permiten acceso a información en tiempo real y superar limitaciones del training data
- **Ejecutan lógica predefinida**: Las herramientas ejecutan lógica específica definida por el desarrollador, no poseen capacidades de razonamiento independientes

### Cómo los Agentes Usan Herramientas

1. **Razonamiento**: El LLM del agente analiza instrucciones, historial y request del usuario
2. **Selección**: Basado en el análisis, decide qué herramienta usar
3. **Invocación**: Genera los argumentos requeridos y ejecuta la herramienta
4. **Observación**: Recibe el output de la herramienta
5. **Finalización**: Incorpora el resultado en su proceso de razonamiento

### Tipos de Herramientas en ADK

#### 1. Function Tools (Herramientas de Función)

**Funciones Síncronas**:
```python
def get_weather(city: str) -> dict:
    """
    Obtiene el clima actual para una ciudad.
    
    Args:
        city: Nombre de la ciudad
        
    Returns:
        dict: {"status": "success", "report": "..."}
    """
    # Implementación
    return {"status": "success", "report": f"El clima en {city}..."}
```

**Agentes como Herramientas**:
```python
from google.adk.tools import AgentTool

specialized_agent = Agent(name="specialist", ...)
root_agent = Agent(
    tools=[AgentTool(specialized_agent)]
)
```

**Long Running Tools**:
```python
from google.adk.tools import LongRunningTool

def process_data(data: str) -> dict:
    # Operación que toma tiempo
    pass

long_tool = LongRunningTool(
    func=process_data,
    timeout=60  # segundos
)
```

#### 2. Built-in Tools (Herramientas Integradas)

**Google Search**:
```python
from google.adk.tools import google_search

root_agent = Agent(
    tools=[google_search],
    instruction="Usa Google Search para respuestas actualizadas"
)
```

**Ejecución de Código**:
```python
from google.adk.tools import built_in_code_execution

code_agent = Agent(
    tools=[built_in_code_execution],
    instruction="Ejecuta código Python para cálculos"
)
```

**Vertex AI Search**:
```python
from google.adk.tools import VertexAiSearchTool

vertex_search = VertexAiSearchTool(
    data_store_id="projects/123/locations/us/collections/default/dataStores/my-store"
)

agent = Agent(tools=[vertex_search])
```

#### 3. Third-Party Tools

ADK permite integración con herramientas de bibliotecas populares como LangChain y CrewAI.

### Tool Context

El Tool Context proporciona acceso a información contextual dentro de las funciones de herramienta:

```python
from google.adk.tools import ToolContext

def advanced_tool(param: str, tool_context: ToolContext) -> dict:
    # Acceso al estado
    current_value = tool_context.state.get("counter", 0)
    tool_context.state["counter"] = current_value + 1
    
    # Control de flujo
    if need_specialist:
        tool_context.actions.transfer_to_agent = "specialist_agent"
    
    # Acceso a artifacts
    doc = tool_context.load_artifact("document.pdf")
    
    # Búsqueda en memoria
    memories = tool_context.search_memory("query")
    
    return {"status": "success", "result": "..."}
```

### Mejores Prácticas para Definir Herramientas

1. **Nombres Descriptivos**:
```python
# ✅ Bueno
def get_user_profile(user_id: int) -> dict:

# ❌ Malo
def process(id: int) -> dict:
```

2. **Parámetros Claros**:
```python
# ✅ Bueno - con type hints y sin defaults
def search_documents(query: str, limit: int) -> dict:

# ❌ Malo - sin types y con defaults
def search(q, limit=10):
```

3. **Docstrings Completas**:
```python
def create_ticket(title: str, description: str, priority: str) -> dict:
    """
    Crea un ticket de soporte en el sistema.
    
    Usar cuando el usuario reporta un problema o solicita ayuda.
    
    Args:
        title: Título breve del ticket
        description: Descripción detallada del problema
        priority: Nivel de prioridad (low, medium, high, critical)
        
    Returns:
        dict: {"status": "success", "ticket_id": "...", "url": "..."}
              o {"status": "error", "error_message": "..."}
    """
```

## Sesiones y Memoria

### Conceptos Core

ADK proporciona formas estructuradas de manejar contexto a través de Session, State y Memory:

- **Session**: Thread de conversación actual
- **State**: Datos dentro de la conversación actual
- **Memory**: Información buscable entre sesiones

### Prefijos de Estado

```python
# Específico de sesión (default)
tool_context.state["counter"] = 1

# Compartido entre usuarios de la app
tool_context.state["app:shared_config"] = {...}

# Específico del usuario (todas sus sesiones)
tool_context.state["user:preferences"] = {...}

# Temporal (no persistente)
tool_context.state["temp:calculation"] = result
```

### SessionService

**InMemory (desarrollo)**:
```python
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
```

**Database (producción)**:
```python
from google.adk.sessions import DatabaseSessionService

session_service = DatabaseSessionService(
    db_url="postgresql://user:pass@host/db"
)
```

### MemoryService

ADK ofrece servicios para gestionar memoria a largo plazo:

```python
from google.adk.memory import InMemoryMemoryService

memory_service = InMemoryMemoryService()

# En herramientas
memories = tool_context.search_memory("búsqueda relevante")
```

### Express Mode

Para desarrollo más rápido con estado automático:

```python
from google.adk.sessions import ExpressSession

session = ExpressSession()
# Manejo automático de estado sin configuración manual
```

## Callbacks

### Mecanismo de Callbacks

Los callbacks proporcionan un mecanismo poderoso para interceptar la ejecución del agente en puntos específicos:

```python
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest

def my_before_model_callback(
    callback_context: CallbackContext, 
    llm_request: LlmRequest
) -> Optional[LlmResponse]:
    # return None = continuar normalmente
    # return LlmResponse = skip LLM call
    return None

agent = LlmAgent(
    name="agent_with_callbacks",
    model="gemini-2.0-flash",
    before_model_callback=my_before_model_callback
)
```

### Tipos de Callbacks y Control de Flujo

1. **before_agent** → `Optional[types.Content]`
2. **after_agent** → `Optional[types.Content]`
3. **before_model** → `Optional[LlmResponse]`
4. **after_model** → `Optional[LlmResponse]`
5. **before_tool** → `Optional[Dict]`
6. **after_tool** → `Optional[Dict]`

### Ejemplo: Guardrail de Seguridad

```python
def safety_guardrail_callback(
    callback_context: CallbackContext,
    llm_request: LlmRequest
) -> Optional[LlmResponse]:
    # Extraer último mensaje del usuario
    user_message = llm_request.contents[-1].parts[0].text
    
    # Verificar contenido inseguro
    if is_unsafe_content(user_message):
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text="No puedo ayudar con eso.")]
            )
        )
    
    # Modificar instrucciones del sistema
    llm_request.config.system_instruction.parts[0].text = (
        "[Safety Filter Active] " + 
        llm_request.config.system_instruction.parts[0].text
    )
    
    return None  # Continuar con request modificado
```

## Artifacts

### ¿Qué son los Artifacts?

Los Artifacts representan un mecanismo para manejar datos binarios nombrados y versionados asociados con sesiones de usuario o usuarios específicos.

### Conceptos Clave

- **Definición**: Pieza de datos binarios identificada por un filename único
- **Representación**: Usando `google.genai.types.Part` con inline_data
- **Versionado**: Automático, cada save crea nueva versión
- **Persistencia**: Manejada por ArtifactService

### Configuración

```python
from google.adk.artifacts import InMemoryArtifactService
# o
from google.adk.artifacts import GcsArtifactService

# Para desarrollo
artifact_service = InMemoryArtifactService()

# Para producción
artifact_service = GcsArtifactService(
    bucket_name="my-artifacts-bucket"
)

runner = Runner(
    agent=agent,
    artifact_service=artifact_service
)
```

### Uso en Herramientas

```python
def process_document(filename: str, tool_context: ToolContext) -> dict:
    # Cargar artifact
    document = tool_context.load_artifact(filename)
    if not document:
        return {"error": "Documento no encontrado"}
    
    # Procesar
    result = analyze_document(document.inline_data.data)
    
    # Guardar resultado
    result_part = types.Part.from_data(
        data=result.encode(),
        mime_type="text/plain"
    )
    version = tool_context.save_artifact(
        "analysis_result.txt", 
        result_part
    )
    
    # Listar artifacts disponibles
    all_files = tool_context.list_artifacts()
    
    return {
        "status": "success",
        "version": version,
        "available_files": all_files
    }
```

### Namespacing

```python
# Específico de sesión
tool_context.save_artifact("report.pdf", data)

# Específico de usuario (persiste entre sesiones)
tool_context.save_artifact("user:profile.jpg", data)
```

## Streaming y Comunicación en Tiempo Real

### Características de Streaming

ADK soporta comunicación bidireccional de baja latencia con voz y video usando la API Live de Gemini:

- Conversaciones de voz naturales con interrupciones
- Procesamiento de texto, audio y video
- Respuestas en texto y audio

### Configuración Básica

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="streaming_agent",
    model="gemini-2.0-flash-exp",  # Modelo compatible con streaming
    # o model="gemini-2.0-flash-live-001"
    instruction="Asistente con capacidades de voz",
    tools=[google_search]
)
```

### Ejecutar con Streaming

```bash
# Configurar SSL (requerido para voz/video)
export SSL_CERT_FILE=$(python -m certifi)

# Lanzar UI con streaming
adk web
```

### Herramientas de Streaming

Las herramientas pueden transmitir resultados intermedios:

```python
async def monitor_stock_price(symbol: str) -> AsyncGenerator[dict, None]:
    while True:
        price = get_current_price(symbol)
        yield {"price": price, "timestamp": datetime.now()}
        await asyncio.sleep(1)
```

### Aplicación Custom con Streaming

```python
from fastapi import FastAPI
from google.adk.runners import Runner

app = FastAPI()

@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Configurar runner con streaming
    async for event in runner.run_live(...):
        await websocket.send_json(event.to_dict())
```

## Seguridad y Safety

### Riesgos de Seguridad

1. **Desalineación y corrupción de objetivos**
2. **Generación de contenido dañino**
3. **Acciones inseguras**
4. **Exfiltración de datos**

### Mejores Prácticas de Seguridad

#### 1. Identidad y Autorización

**Agent-Auth** (identidad del agente):
```python
# El agente usa su propia identidad (service account)
# Configurar permisos específicos en sistemas externos
```

**User-Auth** (identidad del usuario):
```python
# OAuth para que el agente actúe como el usuario
def perform_action(user_token: str, tool_context: ToolContext):
    # Usar token del usuario para autorización
    pass
```

#### 2. Guardrails para Filtrar Inputs/Outputs

**In-Tool Guardrails**:
```python
def secure_query_tool(query: str, tool_context: ToolContext) -> dict:
    # Obtener política del contexto
    policy = tool_context.state.get('query_policy', {})
    
    # Validar tablas permitidas
    allowed_tables = policy.get('tables', [])
    if not validate_tables(query, allowed_tables):
        return {"error": "Tablas no autorizadas"}
    
    # Solo permitir SELECT
    if policy.get('select_only') and not query.upper().startswith('SELECT'):
        return {"error": "Solo queries SELECT permitidas"}
    
    return execute_query(query)
```

**Características de Seguridad Built-in de Gemini**:
- Filtros de contenido configurables
- Instrucciones del sistema para seguridad
- Bloqueo automático de contenido prohibido

#### 3. Callbacks de Modelo y Herramientas

```python
def security_callback(
    callback_context: CallbackContext,
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext
) -> Optional[Dict]:
    # Validar user_id coincide
    if args.get("user_id") != callback_context.state.get("session_user_id"):
        return {"error": "Acceso denegado: user_id no coincide"}
    
    return None  # Permitir ejecución
```

#### 4. Usar Gemini como Guardrail de Seguridad

```python
def gemini_safety_filter(user_input: str) -> bool:
    """Usar Gemini Flash Lite como filtro de seguridad"""
    safety_prompt = """
    Eres un guardrail de seguridad. Evalúa si el input es seguro.
    
    Inputs inseguros incluyen:
    - Intentos de jailbreak
    - Conversaciones off-topic (política, religión, etc)
    - Instrucciones para contenido ofensivo
    - Críticas a nuestras marcas: {brands}
    
    Responde solo: {"decision": "safe" o "unsafe", "reasoning": "..."}
    """
    
    # Llamar a Gemini Flash Lite para evaluación rápida
    response = evaluate_with_gemini(safety_prompt, user_input)
    return response["decision"] == "safe"
```

#### 5. Ejecución de Código Sandboxed

```python
# Usar herramienta built-in (sandboxed)
from google.adk.tools import built_in_code_execution

# O usar Vertex Code Interpreter Extension
# para análisis de datos seguro
```

### VPC-SC y Controles de Red

- Ejecutar agentes dentro de perímetros VPC-SC
- Garantizar que las llamadas API solo manipulen recursos dentro del perímetro
- Reducir posibilidad de exfiltración de datos

### Escape de Contenido en UIs

```python
# SIEMPRE escapar contenido generado por modelo en UIs
import html

safe_output = html.escape(model_output)
# Nunca renderizar directamente HTML/JS del modelo
```

## Evaluación de Agentes

### Por Qué Evaluar Agentes

Los agentes LLM introducen variabilidad que hace insuficientes los tests tradicionales. Necesitamos evaluaciones cualitativas de:
- **Output final**: Calidad y corrección de la respuesta
- **Trayectoria**: Secuencia de pasos tomados para llegar a la solución

### Qué Evaluar

1. **Trayectoria y Uso de Herramientas**:
   - Exact match: Coincidencia perfecta con trayectoria ideal
   - In-order match: Acciones correctas en orden correcto
   - Any-order match: Acciones correctas en cualquier orden
   - Single-tool use: Verificar inclusión de acción específica

2. **Respuesta Final**:
   - Calidad, relevancia y corrección del output

### Métodos de Evaluación

#### 1. Usando Test Files

Archivo `evaluation.test.json`:
```json
[
  {
    "query": "¿cuál es el clima en París?",
    "expected_tool_use": [
      {
        "tool_name": "get_weather",
        "tool_input": {"city": "Paris"}
      }
    ],
    "expected_intermediate_agent_responses": [],
    "reference": "El clima en París está soleado con 25°C."
  }
]
```

#### 2. Usando Evalset Files

Para sesiones más complejas y multi-turno:
```json
[
  {
    "name": "weather_conversation",
    "data": [
      {
        "query": "¿Qué puedes hacer?",
        "expected_tool_use": [],
        "reference": "Puedo proporcionar información del clima..."
      },
      {
        "query": "¿Cuál es el clima en NYC?",
        "expected_tool_use": [
          {
            "tool_name": "get_weather",
            "tool_input": {"city": "New York"}
          }
        ],
        "reference": "El clima en Nueva York..."
      }
    ],
    "initial_session": {
      "state": {},
      "app_name": "weather_app",
      "user_id": "test_user"
    }
  }
]
```

### Ejecutar Evaluaciones

#### Web UI (`adk web`):
1. Iniciar servidor: `adk web`
2. Interactuar con agente
3. Click en "Eval tab"
4. Crear o seleccionar evalset
5. Agregar sesión actual como eval

#### Programáticamente (`pytest`):
```python
from google.adk.evaluation.agent_evaluator import AgentEvaluator

def test_agent():
    AgentEvaluator.evaluate(
        agent_module="my_agent",
        eval_dataset_file_path_or_dir="tests/agent.test.json"
    )
```

#### CLI (`adk eval`):
```bash
adk eval \
  my_agent \
  evalset.json \
  --config_file_path=test_config.json \
  --print_detailed_results
```

### Criterios de Evaluación

```json
{
  "tool_trajectory_avg_score": 1.0,
  "response_match_score": 0.8
}
```

## Deployment

### Opciones de Deployment

#### 1. Vertex AI Agent Engine (Recomendado)

Servicio completamente administrado en Google Cloud:

- Auto-scaling automático
- Gestión simplificada
- Optimizado para agentes ADK

#### 2. Cloud Run

Para control completo sobre escalamiento:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8080"]
```

```bash
# Build y deploy
gcloud run deploy my-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

#### 3. Google Kubernetes Engine (GKE)

Para arquitecturas más complejas y requisitos específicos de infraestructura.

### Testing Pre-Deployment

```bash
# Servidor local
adk api_server

# Crear sesión
curl -X POST http://localhost:8000/apps/my_agent/users/u123/sessions/s123 \
  -H "Content-Type: application/json" \
  -d '{"state": {"key": "value"}}'

# Enviar query
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "my_agent",
    "user_id": "u123",
    "session_id": "s123",
    "new_message": {
      "role": "user",
      "parts": [{"text": "Hola"}]
    }
  }'
```

## Grounding

### Google Search Grounding

Permite a los agentes acceder a información en tiempo real de la web:

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

agent = Agent(
    name="search_agent",
    model="gemini-2.5-flash",
    instruction="Responde usando Google Search. Siempre cita fuentes.",
    tools=[google_search]
)
```

### Estructura de Respuesta Grounded

```python
# Respuesta incluye:
{
    "content": "Respuesta del agente...",
    "groundingMetadata": {
        "groundingChunks": [
            {"web": {"title": "Fuente", "uri": "https://..."}}
        ],
        "groundingSupports": [
            {
                "groundingChunkIndices": [0],
                "segment": {
                    "text": "Texto citado",
                    "startIndex": 0,
                    "endIndex": 50
                }
            }
        ],
        "searchEntryPoint": {...}  # HTML para sugerencias
    }
}
```

### Vertex AI Search Grounding

Para búsqueda en datos privados configurados:

```python
from google.adk.tools import VertexAiSearchTool

vertex_search = VertexAiSearchTool(
    data_store_id="projects/123/locations/us/dataStores/my-store"
)
```

## Model Context Protocol (MCP)

### ¿Qué es MCP?

El Model Context Protocol es un estándar abierto para estandarizar cómo los LLMs se comunican con aplicaciones externas, fuentes de datos y herramientas.

### MCP en ADK

ADK permite tanto usar como exponer herramientas MCP:

#### Usar Servidores MCP Existentes:
```python
# ADK actúa como cliente MCP
# Usa herramientas proporcionadas por servidores MCP externos
```

#### Exponer Herramientas ADK vía MCP:
```python
# Construir servidor MCP que envuelve herramientas ADK
# Haciéndolas accesibles a cualquier cliente MCP
```

### MCP Toolbox para Bases de Datos

Servidor MCP open source para acceso a bases de datos:

```python
# Integración con BigQuery, PostgreSQL, etc.
# Soporte nativo en ADK
```

### FastMCP

Framework de alto nivel para construir servidores MCP:

```python
from fastmcp import FastMCP

# Decorador simple para exponer funciones
@fastmcp.tool
def mi_herramienta(param: str) -> str:
    return f"Resultado: {param}"
```

## Patrones de Arquitectura

### 1. Agente Simple
- **Propósito**: Tareas conversacionales básicas
- **Componentes**: Agent + instruction
- **Ejemplo**: Chatbot de saludo

### 2. Agente con Herramientas
- **Propósito**: Interacción con sistemas externos
- **Componentes**: Agent + tools (built-in o custom)
- **Limitación**: Una herramienta built-in por agente

### 3. Agente con Estado
- **Propósito**: Continuidad entre sesiones
- **Componentes**: Agent + SessionService + state management
- **Variantes**: InMemory (temporal) vs Database (persistente)

### 4. Sistema Multi-Agente
- **Propósito**: Especialización y orquestación
- **Patrones**: Delegation vs Agent-as-Tool
- **Casos**: Customer service, análisis complejo

### 5. Workflow Agents
- **Sequential**: Procesamiento en pipeline
- **Parallel**: Ejecución concurrente
- **Loop**: Refinamiento iterativo

### 6. Híbridos
- **Multi-Agent + State**: Especialización con memoria compartida
- **Sequential + Parallel**: Optimización de rendimiento
- **Loop + Multi-Agent**: Refinamiento colaborativo

## Limitaciones y Consideraciones

### Limitaciones de Herramientas

1. **Una herramienta built-in por agente raíz**
   ```python
   # ❌ NO FUNCIONA
   Agent(tools=[google_search, code_execution])
   
   # ✅ SOLUCIÓN: Multi-Agent
   Agent(tools=[AgentTool(search_agent), AgentTool(code_agent)])
   ```

2. **No mezclar built-in con custom**
   ```python
   # ❌ NO FUNCIONA  
   Agent(tools=[google_search, custom_function])
   
   # ✅ SOLUCIÓN: Separar en agentes especializados
   ```

3. **Sub-agentes no pueden usar built-in tools**
   ```python
   # ❌ NO FUNCIONA
   sub_agent = Agent(tools=[google_search])
   root_agent = Agent(sub_agents=[sub_agent])
   
   # ✅ SOLUCIÓN: Agent-as-Tool pattern
   ```

### Limitaciones de Modelos

1. **LiteLLM + Built-in Tools incompatible**
   ```python
   # ❌ NO FUNCIONA
   Agent(model=LiteLlm(...), tools=[google_search])
   
   # ✅ SOLO custom functions con LiteLLM
   ```

2. **Output Schema sin herramientas**
   ```python
   # ❌ NO FUNCIONA
   Agent(output_schema=Schema, tools=[...])
   
   # ✅ Output schema O herramientas, no ambos
   ```

### Consideraciones de Rendimiento

1. **Parallel vs Sequential**
   - Parallel: Tareas independientes, mejor rendimiento
   - Sequential: Dependencias entre etapas, procesamiento ordenado

2. **Estado en memoria vs persistente**
   - InMemory: Más rápido, no sobrevive reinicio
   - Database: Persistente, overhead de I/O

3. **Número de iteraciones en Loop**
   - Balance entre calidad y tiempo/costo
   - Implementar exit conditions claras

### Limitaciones de Streaming

- Actualmente no soporta: Callbacks, LongRunningTool, ExampleTool, Shell agents (SequentialAgent)
- Requiere modelos específicos con soporte Live API

## Buenas Prácticas

### Estructura de Proyecto

```
proyecto/
├── requirements.txt         # Dependencias específicas
├── .env.example            # Template de configuración
├── main_agent/             # Agente principal
│   ├── __init__.py        # from . import agent
│   ├── agent.py           # root_agent = ...
│   ├── .env               # API keys
│   └── sub_agents/        # Si es multi-agente
│       ├── __init__.py
│       ├── specialist1/
│       └── specialist2/
├── utils/                  # Funciones compartidas
│   ├── __init__.py
│   ├── tools.py           # Custom functions
│   └── state_management.py
└── tests/                  # Tests
    ├── unit/
    ├── integration/
    └── evalsets/
```

### Instrucciones Efectivas

```python
instruction = """
ROLE: Define el rol claramente
TASK: Especifica la tarea principal
CONSTRAINTS: Límites y restricciones
TOOLS: Lista herramientas disponibles
OUTPUT: Formato de respuesta esperado

EXAMPLES:
- Ejemplo de entrada y salida esperada
- Casos edge a considerar

IMPORTANT: Instrucciones críticas al final
"""
```

### Manejo de Estado

```python
# ✅ Inicialización consistente
def initialize_state():
    return {
        "user_id": None,
        "preferences": {},
        "history": [],
        "metadata": {"created_at": datetime.now().isoformat()}
    }

# ✅ Actualización segura en tools
def update_state_tool(value: str, tool_context: ToolContext) -> dict:
    current_list = tool_context.state.get("items", [])
    current_list.append(value)
    tool_context.state["items"] = current_list  # Trigger auto-save
    return {"status": "updated", "count": len(current_list)}
```

### Manejo de Errores

```python
def robust_tool(param: str, tool_context: ToolContext) -> dict:
    try:
        result = risky_operation(param)
        return {
            "status": "success",
            "result": result,
            "error": None
        }
    except Exception as e:
        logger.error(f"Error in tool: {e}")
        return {
            "status": "error", 
            "result": None,
            "error": str(e)
        }
```

### Callbacks Productivos

```python
def production_before_agent_callback(callback_context: CallbackContext):
    # Logging estructurado
    logger.info("Agent execution started", extra={
        "agent_name": callback_context.agent_name,
        "user_id": callback_context.user_id,
        "session_id": callback_context.session_id,
        "invocation_id": callback_context.invocation_id
    })
    
    # Métricas
    callback_context.state["request_start_time"] = time.time()
    
    # Rate limiting
    request_count = callback_context.state.get("requests_today", 0)
    if request_count > MAX_REQUESTS_PER_DAY:
        return types.Content(
            role="model",
            parts=[types.Part(text="Daily limit exceeded. Please try tomorrow.")]
        )
    
    return None
```

## Casos de Uso por Tipo de Agente

### Agente Básico
- **Chatbots simples**: Atención al cliente nivel 1
- **Interfaces conversacionales**: FAQ automatizado
- **Prototipos**: Validación de conceptos

### Tool Agent  
- **Investigación automatizada**: Búsqueda y síntesis de información
- **Integración de APIs**: Conectar servicios externos
- **Automatización de tareas**: Scripts inteligentes

### LiteLLM Agent
- **Optimización de costos**: Usar modelos más económicos
- **Diversificación**: Reducir dependencia de un proveedor
- **Evaluación comparativa**: Testear diferentes modelos

### Structured Outputs
- **Integración de sistemas**: APIs que requieren formato específico
- **Pipelines de datos**: ETL automatizado con LLM
- **Reportes automatizados**: Generación estructurada de contenido

### Sessions & State
- **Asistentes personales**: Memoria de preferencias de usuario
- **Educación adaptativa**: Progreso personalizado
- **Recomendaciones**: Basadas en historial de interacción

### Persistent Storage
- **Aplicaciones de producción**: Estado que sobrevive reinicio
- **CRM automatizado**: Gestión de relaciones con clientes
- **Sistemas de soporte**: Historial técnico detallado

### Multi-Agent
- **Plataformas complejas**: Múltiples dominios de expertise
- **Customer service**: Enrutamiento inteligente especializado
- **Análisis empresarial**: Diferentes perspectivas de análisis

### Stateful Multi-Agent
- **Experiencias personalizadas**: Estado compartido entre especialistas
- **Plataformas educativas**: Progreso entre diferentes tutores
- **Salud digital**: Historial compartido entre especialistas

### Sequential Agent
- **Procesos de aprobación**: Workflow de negocio estructurado
- **Análisis de datos**: Pipeline de procesamiento
- **Content creation**: Generación + revisión + optimización

### Parallel Agent
- **Monitoreo de sistemas**: Recolección concurrente de métricas
- **Investigación distribuida**: Búsqueda paralela en múltiples fuentes
- **Análisis de mercado**: Evaluación simultánea de competidores

### Loop Agent
- **Generación de contenido premium**: Refinamiento hasta calidad óptima
- **Optimización iterativa**: Mejora continua de resultados
- **Control de calidad**: Revisión automática hasta aprobación

### Streaming Agent
- **Asistentes de voz**: Conversaciones naturales en tiempo real
- **Análisis de video**: Procesamiento de streams en vivo
- **Experiencias interactivas**: UI/UX con feedback inmediato

## Consideraciones de Producción

### Seguridad
- Nunca exponer API keys en código
- Implementar rate limiting
- Validar inputs de usuario
- Filtrar contenido sensible con callbacks
- Usar VPC-SC para aislamiento de red
- Escapar contenido en UIs

### Monitoreo
- Logging estructurado de todas las interacciones
- Métricas de rendimiento y uso
- Alertas para fallos y anomalías
- Seguimiento de costos de API
- Integración con herramientas de observabilidad

### Escalabilidad
- Usar DatabaseSessionService para estado persistente
- Considerar connection pooling para bases de datos
- Implementar caching donde sea apropiado
- Arquitectura distribuida para alto volumen
- Usar Vertex AI Agent Engine para auto-scaling

### Mantenimiento
- Versionado de agentes y esquemas
- Testing automatizado de workflows
- Rollback strategies para deployments
- Documentación actualizada de comportamiento esperado
- Evaluación continua con evalsets

### Optimización
- Selección de modelo según caso de uso
- Parallel agents para tareas independientes
- Caching de respuestas frecuentes
- Lazy loading de recursos
- Batch processing donde sea posible

## Recursos Adicionales

### Documentación Oficial
- [Documentación ADK](https://google.github.io/adk-docs/)
- [API Reference](https://google.github.io/adk-docs/api-reference/)
- [Ejemplos de Agentes](https://github.com/google/adk-samples)

### Comunidad
- [GitHub Issues](https://github.com/google/adk/issues)
- [Discord/Slack Community](#) (si existe)
- [Stack Overflow Tag](#) (si existe)

### Herramientas de Desarrollo
- `adk web`: UI de desarrollo interactiva
- `adk api_server`: Servidor local para testing
- `adk eval`: Evaluación desde CLI

### Integraciones de Observabilidad
- [Comet Opik](https://www.comet.com/docs/opik/tracing/integrations/adk)
- AgentOps
- Arize Phoenix
- Weights & Biases

Esta guía proporciona una base sólida para el desarrollo de proyectos ADK, cubriendo desde implementaciones básicas hasta arquitecturas complejas de producción. La combinación de ejemplos prácticos del curso con la documentación oficial completa ofrece una referencia integral para desarrolladores trabajando con Google Agent Development Kit.

# URL's documentación oficial ADK

## Página Principal
1. https://google.github.io/adk-docs/

## Get Started
2. https://google.github.io/adk-docs/get-started/
3. https://google.github.io/adk-docs/get-started/installation/
4. https://google.github.io/adk-docs/get-started/quickstart/
5. https://google.github.io/adk-docs/get-started/streaming/
6. https://google.github.io/adk-docs/get-started/streaming/quickstart-streaming/
7. https://google.github.io/adk-docs/get-started/streaming/quickstart-streaming-java/
8. https://google.github.io/adk-docs/get-started/testing/
9. https://github.com/google/adk-samples
10. https://google.github.io/adk-docs/get-started/about/

## Tutorials
11. https://google.github.io/adk-docs/tutorials/
12. https://google.github.io/adk-docs/tutorials/agent-team/

## Agents
13. https://google.github.io/adk-docs/agents/
14. https://google.github.io/adk-docs/agents/llm-agents/
15. https://google.github.io/adk-docs/agents/workflow-agents/
16. https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/
17. https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/
18. https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/
19. https://google.github.io/adk-docs/agents/custom-agents/
20. https://google.github.io/adk-docs/agents/multi-agents/
21. https://google.github.io/adk-docs/agents/models/

## Tools
22. https://google.github.io/adk-docs/tools/
23. https://google.github.io/adk-docs/tools/function-tools/
24. https://google.github.io/adk-docs/tools/built-in-tools/
25. https://google.github.io/adk-docs/tools/third-party-tools/
26. https://google.github.io/adk-docs/tools/google-cloud-tools/
27. https://google.github.io/adk-docs/tools/mcp-tools/
28. https://google.github.io/adk-docs/tools/openapi-tools/
29. https://google.github.io/adk-docs/tools/authentication/

## Running Agents
30. https://google.github.io/adk-docs/runtime/
31. https://google.github.io/adk-docs/runtime/runconfig/

## Deploy
32. https://google.github.io/adk-docs/deploy/
33. https://google.github.io/adk-docs/deploy/agent-engine/
34. https://google.github.io/adk-docs/deploy/cloud-run/
35. https://google.github.io/adk-docs/deploy/gke/

## Sessions & Memory
36. https://google.github.io/adk-docs/sessions/
37. https://google.github.io/adk-docs/sessions/session/
38. https://google.github.io/adk-docs/sessions/state/
39. https://google.github.io/adk-docs/sessions/memory/
40. https://google.github.io/adk-docs/sessions/express-mode/

## Callbacks
41. https://google.github.io/adk-docs/callbacks/
42. https://google.github.io/adk-docs/callbacks/types-of-callbacks/
43. https://google.github.io/adk-docs/callbacks/design-patterns-and-best-practices/

## Artifacts
44. https://google.github.io/adk-docs/artifacts/

## Events
45. https://google.github.io/adk-docs/events/

## Context
46. https://google.github.io/adk-docs/context/

## Observability
47. https://google.github.io/adk-docs/observability/agentops/
48. https://google.github.io/adk-docs/observability/arize-ax/
49. https://google.github.io/adk-docs/observability/phoenix/
50. https://google.github.io/adk-docs/observability/weave/
51. https://google.github.io/adk-docs/observability/logging/

## Evaluate
52. https://google.github.io/adk-docs/evaluate/

## MCP
53. https://google.github.io/adk-docs/mcp/

## Bidi-streaming (live)
54. https://google.github.io/adk-docs/streaming/

## Grounding
55. https://google.github.io/adk-docs/grounding/google_search_grounding/
56. https://google.github.io/adk-docs/grounding/vertex_ai_search_grounding/

## Safety and Security
57. https://google.github.io/adk-docs/safety/

## Agent2Agent (A2A) Protocol
58. https://github.com/google/A2A/

## Community Resources
59. https://google.github.io/adk-docs/community/

## Contributing Guide
60. https://google.github.io/adk-docs/contributing-guide/

## API Reference
61. https://google.github.io/adk-docs/api-reference/