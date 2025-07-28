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
# Use ADK web interface (primary method)
adk web

# Note: Command line interface not currently implemented
```

### Environment Configuration
The application requires a `.env` file in the `marriage_document_agent/` directory:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## Architecture

### Current Implementation
Currently implemented as a single agent:

- **marriage_document_agent**: Analyzes marriage and civil union certificates in Chile
  - Specialized in identifying and extracting key information from documents
  - Uses Gemini 2.0 Flash model
  - Configured for Chilean legal context and Spanish language
  - Currently has no tools defined (tools array is empty)

### Key Components

- **marriage_document_agent/agent.py**: Main agent implementation using Google ADK
- **documents/**: Directory containing certificate PDFs for analysis
- **README.md**: Comprehensive project documentation
- **GEMINI.md, adk-guide.md, about-matrimonio-chile.md**: Additional reference documentation

### Agent Configuration
The agent is configured with Spanish instructions for analyzing Chilean marriage and civil union certificates. It focuses on:
- Extracting key information like names, dates, places
- Interpreting data within Chilean legal context
- Identifying document relevance and validity
- Providing structured and accurate information

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
├── marriage_document_agent/
│   ├── agent.py          # Main agent implementation using Google ADK
│   ├── __init__.py       # Package initialization
│   └── .env              # Environment variables (Google API key)
├── documents/            # Certificate PDFs for analysis
├── venv/                 # Python virtual environment
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── CLAUDE.md             # This file - guidance for Claude Code
├── GEMINI.md             # Gemini-specific documentation
├── adk-guide.md          # ADK usage guide
├── about-matrimonio-chile.md  # Legal reference information
└── civil_union_analyzer.log   # Application logs
```

## Testing Certificates

The system includes three sample certificates for testing:
- `Certificado_Cristian.pdf`
- `Certificado_Jaimar.pdf`
- `Certificado_Rodrigo.pdf`

## Dependencies

- `google-adk[database]==0.3.0`: Google Agent Development Kit with database support
- `google-generativeai==0.8.5`: Google Gemini API client
- `python-dotenv==1.0.1`: Environment variable management