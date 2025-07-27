# Civil Union Certificate Analyzer

This project uses Google's Agent Development Kit (ADK) with the Gemini 2.0 Flash model to analyze marriage and civil union certificates in Chile. The agent can determine the type of union and patrimonial regime based on the certificate content.

## Project Structure

```
/
├── multi_tool_agent/
│   ├── __init__.py     # Package initialization
│   ├── agent.py        # Agent implementation
│   └── .env            # Environment variables
├── documents/          # Directory containing certificate PDFs
├── aboutCivilUnionInChile.txt  # Reference info about civil unions in Chile
├── main.py             # Main entry point
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Configure your API key:
   - Edit the `.env` file in the `multi_tool_agent` directory
   - Add your Google API key (required for Gemini 2.0 Flash model)
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. Make sure your certificate PDF files are placed in the `documents` directory.

4. The reference information about civil unions in Chile should be in the file `aboutCivilUnionInChile.txt`.

## Usage

### Running the Agent from Command Line

```bash
# Run in simple mode (default)
python main.py

# Run in team mode with multiple specialized agents
python main.py --mode team
```

### Using ADK Web Interface

Alternatively, you can run the agent using the ADK web interface:

```bash
adk web
```

Then access the web interface at http://localhost:8000

### Example Queries

Once the agent is running, you can enter queries like:

- "Analyze Certificado_Cristian.pdf"
- "Read and determine the type of union in Certificado_Jaimar.pdf"
- "What type of civil union does Rodrigo have according to his certificate?"

Type 'exit' to quit the program.

## How It Works

The agent uses the Google Agent Development Kit (ADK) with the Gemini 2.0 Flash model to create an intelligent system that can:

1. Read and extract text from PDF certificates
2. Analyze the content to determine the type of civil union
3. Identify the patrimonial regime based on Chilean law
4. Provide a comprehensive analysis with explanations

### Agent Modes

#### Simple Mode
A single agent handles all processing tasks with three main tools:
- `read_pdf_certificate`: Extracts text from PDF certificates
- `get_civil_union_info`: Retrieves reference information about civil unions in Chile
- `analyze_certificate`: Analyzes the certificate content

#### Team Mode
A team of specialized agents collaborate to analyze certificates:
- **document-reader**: Specialized in reading PDF files
- **info-extractor**: Extracts structured information from certificates
- **union-analyzer**: Determines the type of union (Matrimonio or Unión Civil)
- **regime-analyzer**: Determines the patrimonial regime
- **final-analysis**: Creates a comprehensive summary of all findings
- **civil-union-analyzer-root**: Orchestrates the other agents and manages delegation

This approach follows the design patterns described in the ADK "Agent Team" tutorial.

## Available Certificates

- Certificado_Cristian.pdf
- Certificado_Jaimar.pdf
- Certificado_Rodrigo.pdf 