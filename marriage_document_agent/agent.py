from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import Optional


class DocumentInput(BaseModel):
    plain_text_document: str = Field(
        description="Texto plano extraído del documento de matrimonio o unión civil en formato PDF")


class CertificateAnalysis(BaseModel):
    document_type: str = Field(
        description="Tipo de documento: 'Matrimonio' o 'Unión Civil'")
    separacion_de_bienes: bool = Field(
        description="True si el texto contiene 'Separación de bienes', False en caso contrario")
    spouse_1_rut: Optional[str] = Field(
        description="RUT del primer cónyuge/conviviente con formato XX.XXX.XXX-X", default=None)
    spouse_2_rut: Optional[str] = Field(
        description="RUT del segundo cónyuge/conviviente con formato XX.XXX.XXX-X", default=None)
    issuance_date: Optional[str] = Field(
        description="Fecha de emisión del certificado en formato YYYY-MM-DD", default=None)
    is_certificate_current: bool = Field(
        description="True si la fecha de emisión está dentro de los últimos 30 días desde hoy (2025-07-28), False en caso contrario")


root_agent = LlmAgent(
    name="marriage_document_agent",
    # https://ai.google.dev/gemini-api/docs/models
    model="gemini-2.0-flash",
    description="Analyzes marriage and civil union certificates in Chile.",
    input_schema=DocumentInput,
    output_schema=CertificateAnalysis,
    output_key="certificate_analysis",
    instruction="""
    Eres un agente especializado en analizar certificados de matrimonio y uniones civiles en Chile. Tu tarea es extraer información específica del texto plano de los documentos.
    
    IMPORTANTE: Tu respuesta DEBE ser un JSON válido que cumpla exactamente con el esquema CertificateAnalysis definido.
    
    Debes extraer exactamente estos campos:
    
    1. document_type: Identifica si es "Matrimonio" o "Unión Civil"
    
    2. separacion_de_bienes: Determina según el tipo de documento:
       - Para Matrimonio: True solo si aparece explícitamente "Separación de bienes" en el texto
       - Para Unión Civil: SIEMPRE True (ya que por ley el régimen por defecto es separación de bienes, sin importar si aparece "comunidad de bienes" o "no pactaron régimen")
    
    3. spouse_1_rut y spouse_2_rut: Extrae los RUTs de ambos cónyuges/convivientes en formato XX.XXX.XXX-X
    
    4. issuance_date: Fecha de emisión del certificado en formato YYYY-MM-DD
    
    5. is_certificate_current: Calcula si la fecha de emisión está dentro de los últimos 30 días desde hoy:
       - True si la diferencia es 30 días o menos
       - False si la diferencia es mayor a 30 días
       - Ejemplo: si issuance_date es 2025-05-05 y hoy es 2025-07-28, son más de 30 días, entonces False
       - Ejemplo: si issuance_date es 2025-07-15 y hoy es 2025-07-28, son 13 días, entonces True
    
    Asegúrate de que la información sea precisa y que todos los campos obligatorios estén completos.
    """,
    tools=[],
)
