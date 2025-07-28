from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import List, Optional


class DocumentInput(BaseModel):
    plain_text_document: str = Field(
        description="Texto plano extraído del documento de matrimonio o unión civil en formato PDF")


class SpouseInfo(BaseModel):
    name: str = Field(
        description="Nombre completo del contrayente/conviviente civil")
    rut: Optional[str] = Field(
        description="RUT del contrayente con formato XX.XXX.XXX-X", default=None)
    birth_date: Optional[str] = Field(
        description="Fecha de nacimiento en formato YYYY-MM-DD", default=None)
    nationality: Optional[str] = Field(
        description="Nacionalidad del contrayente", default=None)
    civil_status: Optional[str] = Field(
        description="Estado civil anterior", default=None)


class CertificateAnalysis(BaseModel):
    document_type: str = Field(
        description="Tipo de documento: 'Matrimonio' o 'Unión Civil'")
    is_valid_certificate: bool = Field(
        description="Si el documento es un certificado válido de matrimonio o unión civil")
    folio: Optional[str] = Field(
        description="Número de folio del certificado (ej: 500627557741)", default=None)
    codigo_verificacion: Optional[str] = Field(
        description="Código de verificación del certificado", default=None)
    patrimonial_regime: Optional[str] = Field(
        description="Régimen patrimonial: 'Sociedad Conyugal', 'Separación de Bienes', o 'Participación en los Gananciales'", default=None)
    spouses: List[SpouseInfo] = Field(
        description="Información de los contrayentes/convivientes civiles", default=[])
    ceremony_date: Optional[str] = Field(
        description="Fecha de la ceremonia/celebración en formato YYYY-MM-DD", default=None)
    ceremony_location: Optional[str] = Field(
        description="Circunscripción o lugar donde se realizó la ceremonia", default=None)
    registro_number: Optional[str] = Field(
        description="Número de inscripción del registro", default=None)
    registro_year: Optional[str] = Field(
        description="Año del registro", default=None)
    civil_registry_office: Optional[str] = Field(
        description="Oficina de registro civil (siempre 'SERVICIO DE REGISTRO CIVIL E IDENTIFICACIÓN')", default=None)
    issuance_date: Optional[str] = Field(
        description="Fecha de emisión del certificado en formato YYYY-MM-DD", default=None)
    issuance_time: Optional[str] = Field(
        description="Hora de emisión del certificado", default=None)
    additional_info: Optional[str] = Field(
        description="Información adicional sobre régimen patrimonial u otros detalles", default=None)
    error_message: Optional[str] = Field(
        description="Mensaje de error si no se puede procesar el documento", default=None)


root_agent = LlmAgent(
    name="marriage_document_agent",
    # https://ai.google.dev/gemini-api/docs/models
    model="gemini-2.0-flash",
    description="Analyzes marriage and civil union certificates in Chile.",
    input_schema=DocumentInput,
    output_schema=CertificateAnalysis,
    output_key="certificate_analysis",
    instruction="""
    Eres un agente especializado en analizar certificados de matrimonio y uniones civiles en Chile. Tu tarea es identificar y extraer información clave del texto plano de los documentos, como nombres, fechas, lugares y otros detalles relevantes. Utiliza tu conocimiento sobre la legislación chilena para interpretar correctamente los datos.
    
    IMPORTANTE: Tu respuesta DEBE ser un JSON válido que cumpla exactamente con el esquema CertificateAnalysis definido.
    
    Si encuentras información que no puedes procesar, indícalo claramente en el campo error_message. Tu objetivo es proporcionar una comprensión clara y precisa del contenido del documento, asegurándote de que todos los detalles sean correctos y relevantes para el contexto legal chileno.
    
    Si el documento no es un certificado de matrimonio o unión civil, marca is_valid_certificate como false e informa en error_message por qué no es relevante para tu tarea.
    
    Si el documento es un certificado de matrimonio o unión civil válido:
    - Identifica si es "Matrimonio" o "Unión Civil" 
    - Extrae información de los contrayentes/convivientes civiles
    - Determina el régimen patrimonial:
      * Para Matrimonio: puede ser "Sociedad Conyugal" (por defecto), "Separación de Bienes", o "Participación en los Gananciales"
      * Para Unión Civil: por defecto es "Separación de Bienes" a menos que se especifique "comunidad de bienes"
    - Extrae fechas, lugares, números de registro y demás información estructurada
    
    Asegúrate de que la información sea precisa y completa, y que cumpla con los estándares legales chilenos.
    """,
    tools=[],
)
