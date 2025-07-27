# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based proof-of-concept that uses Google's Agent Development Kit (ADK) with the Gemini 2.0 Flash model to analyze Chilean marriage and civil union certificates. The system can determine the type of union (Matrimonio or Unión Civil) and identify the patrimonial regime based on certificate content.

## Development Commands

### Setup and Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Create and activate virtual environment (if needed)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Running the Application
```bash
# Run in simple mode (single agent)
python main.py

# Run in team mode (multi-agent system)
python main.py --mode team

# Alternative: Use ADK web interface
adk web
```

### Environment Configuration
The application requires a `.env` file in the `multi_tool_agent/` directory:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Architecture

### Agent Modes
The system supports two operational modes:

1. **Simple Mode**: Single agent (`civil_union_analyzer`) with three tools:
   - `read_pdf_certificate`: Extracts text from PDF files
   - `get_civil_union_info`: Retrieves reference information about Chilean civil unions
   - `analyze_certificate`: Analyzes certificate content

2. **Team Mode**: Six specialized agents working collaboratively:
   - `document-reader`: PDF text extraction
   - `info-extractor`: Structured information extraction
   - `union-analyzer`: Union type determination
   - `regime-analyzer`: Patrimonial regime analysis
   - `final-analysis`: Comprehensive summary creation
   - `civil-union-analyzer-root`: Main orchestration agent

### Key Components

- **main.py**: Entry point with argument parsing for mode selection
- **multi_tool_agent/agent.py**: Core agent implementation with all tool functions and agent definitions
- **documents/**: Directory containing certificate PDFs for analysis
- **aboutCivilUnionInChile.txt**: Reference document with Chilean civil union legal information

### Data Models
The system uses Pydantic models for structured data:
- `ReadPdfResult`: PDF text extraction results
- `AnalyzeCertificateResult`: Certificate analysis outcomes
- `ExtractCertificateInfoResult`: Basic certificate information
- `AnalyzeUnionTypeResult`/`AnalyzeRegimeTypeResult`: Specialized analysis results
- `FinalAnalysisResult`: Comprehensive analysis summary

### Legal Context
The system analyzes two types of unions under Chilean law:

**Matrimonio (Marriage)**:
- Three patrimonial regimes: Sociedad Conyugal (default), Separación de Bienes, Participación en los Gananciales

**Unión Civil (Civil Union)**:
- Default regime: Separación de Bienes
- Available to same-sex or different-sex couples

## File Structure

```
/
├── multi_tool_agent/
│   ├── agent.py          # Main agent implementation and tool functions
│   ├── __init__.py       # Package initialization
│   └── .env              # Environment variables (Google API key)
├── documents/            # Certificate PDFs for analysis
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── aboutCivilUnionInChile.txt  # Legal reference information
└── README.md            # Project documentation
```

## Testing Certificates

The system includes three sample certificates for testing:
- `Certificado_Cristian.pdf`
- `Certificado_Jaimar.pdf`
- `Certificado_Rodrigo.pdf`

## Dependencies

- `google-adk>=0.1.0`: Google Agent Development Kit
- `google-generativeai>=0.3.0`: Google Gemini API client
- `PyPDF2>=3.0.0`: PDF text extraction
- `python-dotenv>=1.0.0`: Environment variable management
- `litellm>=1.0.0`: Optional multi-model support