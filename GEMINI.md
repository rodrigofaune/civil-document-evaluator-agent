This project is a Civil Union Certificate Analyzer. It uses Google's Agent Development Kit (ADK) with the Gemini 2.0 Flash model to analyze marriage and civil union certificates in Chile. The agent can determine the type of union and patrimonial regime based on the certificate content.

The main files are:
- `main.py`: The main entry point for the application.
- `multi_tool_agent/agent.py`: The implementation of the agent.
- `documents/`: This directory contains the certificate PDFs to be analyzed.
- `about-matrimonio-chile.md`: This file contains reference information about civil unions in Chile.
- `requirements.txt`: This file lists the Python dependencies.

To run the project, you can use the following command:
```bash
python main.py
```