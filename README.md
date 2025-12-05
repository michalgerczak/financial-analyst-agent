# Financial Analyst Agent

**Status:** Active development  
**Stack:** Python 3.10+, LangChain, LlamaParse, OpenAI, Anthropic

## Goal
Build an agentic RAG system that can analyze complex financial reports (10-Ks, annual reports) with high precision. Standard LLM retrieval often fails on multi-column financial tables, so this project uses computer vision and specialized parsing to solve that problem.

## Key features
- **Robust ingestion pipeline:** Benchmarked multiple strategies to handle "unreadable" PDFs.  
- **Vision-first approach:** Uses OCR (LlamaParse, Claude 4.5 Vision) to bypass corrupted text layers in financial documents.  
- **Automated testing:** Connectivity and integration tests included.

## Benchmark Results (Day 2)
Tested extraction strategies on the Accenture FY23 balance sheet (page 79).

| Model | Type | Result | Time |
| :--- | :--- | :--- | :--- |
| **pypdf** | Local (text) | FAILED (garbage characters) | 0.1s |
| **pdfplumber** | Local (heuristic) | PARTIAL (lost structure) | 0.4s |
| **pymupdf4llm** | Local (Markdown) | FAILED (Empty/Gibberish) | 0.7s |
| **LlamaParse** | Cloud (vision) | SUCCESS (fastest) | 13.0s |
| **GPT-4o** | Cloud (vision) | SUCCESS | 30.8s |
| **Claude 4.5** | Cloud (vision) | BEST QUALITY | 26.9s |

**Decision:** Use **LlamaParse** for bulk ingestion and **Claude 4.5** for high-precision table extraction.

## Setup and usage

### Prerequisites
- Python 3.10 or newer  
- Poppler (for image conversion): `sudo apt install poppler-utils`

### Installation
```bash
git clone https://github.com/michalgerczak/financial-analyst-agent.git
cd financial-analyst-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
