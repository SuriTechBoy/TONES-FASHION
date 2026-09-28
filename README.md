# TONES FASHION — AI Shopping Assistant

An AI-powered shopping assistant for **TONES Fashion** that helps users discover fashion products using natural-language queries such as:

* "Show me black t-shirts"
* "Find oversized shirts"
* "Show products under ₹1000"
* "I want casual clothes"
* "Find black hoodies"

The system combines a **React frontend**, **FastAPI backend**, structured product knowledge, product retrieval, and an LLM layer to provide an AI-powered shopping experience.

---

## 🚀 Overview

TONES FASHION is designed as an AI shopping platform where users can interact with fashion products using natural language instead of traditional filters.

### Main Flow

```text
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI Backend
 │
 ├── Query Router
 │
 ├── Product Retrieval
 │
 ├── RAG Context
 │
 └── LLM Adapter
 │
 ▼
AI Response
 │
 ▼
React Frontend
```

---

## 🏗️ Architecture

```text
TONES-FASHION/
│
├── 00_MASTER/
├── 01_RAW_DATA/
├── 02_CLEANED/
├── 03_STRUCTURED/
├── 04_VALIDATED/
├── 05_CANONICAL/
├── 06_RAG/
│
├── api/
│   ├── main.py
│   └── __init__.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
└── scripts/
    ├── llm_adapter.py
    ├── query_router.py
    ├── build_rag_context.py
    ├── unified_knowledge_retrieval.py
    ├── unified_product_retrieval.py
    ├── structured_product_search.py
    └── validation / collection scripts
```

---

# ✨ Features

### 🤖 AI Shopping Assistant

Users can ask natural-language questions about TONES Fashion products.

Example:

```text
Show me black t-shirts
```

The backend processes the query and returns matching products.

### 🔎 Natural-Language Product Search

The system supports product discovery based on information such as:

* Product type
* Colour
* Style
* Category
* Price
* Other available product attributes

### 📚 Knowledge Base

The project maintains a structured data pipeline:

```text
RAW DATA
   ↓
CLEANED DATA
   ↓
STRUCTURED DATA
   ↓
VALIDATED DATA
   ↓
CANONICAL DATA
   ↓
RAG DATA
```

### 🧠 RAG Architecture

The project includes retrieval components for preparing relevant product/business information before generating AI responses.

### 🌐 Web Application

The frontend is built using:

* React
* React DOM
* Vite
* JavaScript
* CSS

### ⚡ Backend API

The backend is built using:

* Python
* FastAPI
* Uvicorn
* Pydantic
* Requests

---

# 🛠️ Technology Stack

| Layer               | Technology               |
| ------------------- | ------------------------ |
| Frontend            | React                    |
| Frontend Build Tool | Vite                     |
| Backend             | FastAPI                  |
| Server              | Uvicorn                  |
| Language            | Python                   |
| Product Retrieval   | Python Retrieval Scripts |
| RAG                 | Custom RAG Pipeline      |
| LLM Integration     | LLM Adapter              |
| Version Control     | Git / GitHub             |
| Node.js             | Node.js 24               |
| Python              | Python 3.11              |

---

# 📦 Local Setup

## 1. Clone Repository

```powershell
git clone https://github.com/SuriTechBoy/TONES-FASHION.git
```

Move into the project:

```powershell
cd TONES-FASHION
```

Check the repository:

```powershell
git status
```

Expected:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

---

# 🐍 Backend Setup

## Python Requirements

The backend uses Python 3.11.

Verify Python:

```powershell
python --version
```

Expected:

```text
Python 3.11.9
```

Verify pip:

```powershell
python -m pip --version
```

---

## Install Backend Dependencies

If dependencies have not already been installed:

```powershell
python -m pip install fastapi uvicorn pydantic requests
```

Verify them:

```powershell
python -c "import fastapi, uvicorn, pydantic, requests; print('Backend dependencies OK')"
```

Expected:

```text
Backend dependencies OK
```

---

# 🟢 Start Backend

Open **Terminal 1**.

Move to the project:

```powershell
cd "$([Environment]::GetFolderPath('Desktop'))\TONES-FASHION"
```

For local development/testing, use the mock provider:

```powershell
$env:TONES_LLM_PROVIDER="mock"
```

Verify:

```powershell
echo $env:TONES_LLM_PROVIDER
```

Expected:

```text
mock
```

Start FastAPI:

```powershell
python -m uvicorn api.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

Keep this terminal running.

---

# 🔵 Frontend Setup

Open **Terminal 2**.

Move into the frontend:

```powershell
cd "$([Environment]::GetFolderPath('Desktop'))\TONES-FASHION\frontend"
```

Install frontend dependencies:

```powershell
npm.cmd install
```

Start the Vite development server:

```powershell
npm.cmd run dev
```

Expected:

```text
VITE v8.3.1 ready

➜ Local: http://localhost:5173/
```

Open:

```text
http://localhost:5173/
```

---

# 🌐 Frontend + Backend

The complete local development environment requires both servers.

### Terminal 1 — Backend

```powershell
cd "$([Environment]::GetFolderPath('Desktop'))\TONES-FASHION"

$env:TONES_LLM_PROVIDER="mock"

python -m uvicorn api.main:app --reload
```

### Terminal 2 — Frontend

```powershell
cd "$([Environment]::GetFolderPath('Desktop'))\TONES-FASHION\frontend"

npm.cmd run dev
```

Then open:

```text
http://localhost:5173/
```

---

# 🩺 Backend Health Check

Open another terminal.

Run:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Expected:

```json
{
  "status": "healthy",
  "llm_configured": true
}
```

A successful response confirms that the backend API is running.

---

# 💬 Test AI Chat API

PowerShell can sometimes interpret `curl` differently, so the recommended Windows test is:

```powershell
$body = @{ message = "Show me black t-shirts" } | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/api/v1/chat" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

Expected response:

```text
answer
------
Here are the matching TONES Fashion products:...
```

---

# 🔐 LLM Configuration

The project supports an LLM provider through the LLM adapter.

For local testing without an external API:

```powershell
$env:TONES_LLM_PROVIDER="mock"
```

For OpenRouter, configure the API key as an environment variable.

**Never commit the API key to GitHub.**

Example PowerShell configuration:

```powershell
$env:OPENROUTER_API_KEY="YOUR_ACTUAL_KEY"
$env:TONES_LLM_PROVIDER="openrouter"
```

Verify without displaying the actual key:

```powershell
python -c "import os; print('Provider:', os.getenv('TONES_LLM_PROVIDER')); print('API key:', 'SET' if os.getenv('OPENROUTER_API_KEY') else 'NOT SET')"
```

Expected:

```text
Provider: openrouter
API key: SET
```

---

# 📁 Data Pipeline

TONES Fashion uses a multi-stage knowledge pipeline.

```text
00_MASTER
    ↓
01_RAW_DATA
    ↓
02_CLEANED
    ↓
03_STRUCTURED
    ↓
04_VALIDATED
    ↓
05_CANONICAL
    ↓
06_RAG
```

This structure separates raw collection data from validated and retrieval-ready knowledge.

---

# 🔧 Important Scripts

The `scripts/` directory contains the data collection, processing, retrieval, RAG, and validation utilities.

### Data Collection

```text
collect_products.py
collect_collections.py
collect_business_pages.py
collect_collection_pagination.py
```

### Data Processing

```text
parse_collections.py
parse_collection_products_json.py
parse_all_collection_products.py
clean_business_pages.py
```

### Product Processing

```text
build_canonical_products.py
build_product_search_index.py
structured_product_search.py
unified_product_retrieval.py
```

### RAG

```text
build_rag_context.py
build_product_rag_chunks.py
validate_rag_chunks.py
generate_rag_prompt.py
```

### LLM

```text
llm_adapter.py
test_llm_answers.py
validate_llm_answers.py
```

### Knowledge Retrieval

```text
unified_knowledge_retrieval.py
query_router.py
test_unified_knowledge_retrieval.py
```

---

# 🧪 Testing

Backend dependency test:

```powershell
python -c "import fastapi, uvicorn, pydantic, requests; print('Backend dependencies OK')"
```

Backend health test:

```powershell
curl.exe http://127.0.0.1:8000/health
```

AI chat test:

```powershell
$body = @{ message = "Show me black t-shirts" } | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/chat" -Method Post -ContentType "application/json" -Body $body
```

Frontend dependency check:

```powershell
cd frontend
npm.cmd list --depth=0
```

---

# 📋 Current Verified Environment

The project has been tested with:

```text
Python     3.11.9
pip        24.0
Node.js    24.21.0
npm        11.x
React      19.x
Vite       8.3.1
FastAPI    Installed
Uvicorn    Installed
Pydantic   Installed
Requests   Installed
```

The following have been successfully verified:

* Git repository cloned successfully
* Git working tree available
* Python installed and working
* Backend dependencies installed
* Node.js installed
* Frontend dependencies installed
* Vite development server working
* FastAPI backend working
* Backend `/health` endpoint working
* `/api/v1/chat` endpoint responding
* Frontend accessible through `localhost:5173`

---

# ⚠️ Windows PowerShell Note

On this Windows setup, PowerShell may block `npm.ps1` because of the execution policy.

If:

```powershell
npm install
```

produces an execution-policy error, use:

```powershell
npm.cmd install
```

Similarly:

```powershell
npm.cmd run dev
```

instead of:

```powershell
npm run dev
```

This does not mean Node.js is broken. `node --version` should still work.

---

# 🛑 Stopping the Application

To stop the backend:

```text
Ctrl + C
```

To stop the frontend:

```text
Ctrl + C
```

The project files and installed dependencies remain available for the next session.

---

# 🔄 Starting the Project Again

After closing VS Code or restarting the computer, you do **not** need to reinstall the dependencies.

### Backend

```powershell
cd "$([Environment]::GetFolderPath('Desktop'))\TONES-FASHION"

$env:TONES_LLM_PROVIDER="mock"

python -m uvicorn api.main:app --reload
```

### Frontend

Open another terminal:

```powershell
cd "$([Environment]::GetFolderPath('Desktop'))\TONES-FASHION\frontend"

npm.cmd run dev
```

Then open:

```text
http://localhost:5173/
```

---

# 🔒 Security

Do not commit:

* API keys
* Passwords
* Authentication tokens
* Private credentials
* `.env` files containing secrets

Use environment variables for sensitive configuration.

---

# 📌 Project Status

### Current Development Status

```text
✅ Git repository
✅ Data pipeline
✅ Product knowledge structure
✅ RAG structure
✅ Backend API
✅ Product retrieval
✅ LLM adapter
✅ React frontend
✅ Vite development server
✅ Health endpoint
✅ Chat API
🔄 AI provider integration / refinement
🔄 Further product and RAG improvements
```

---

# 👨‍💻 Development

This repository is being developed as an AI-powered fashion shopping assistant for TONES Fashion.

The project focuses on combining:

```text
Fashion Product Data
        +
Knowledge Engineering
        +
Product Retrieval
        +
RAG
        +
LLM
        +
React UI
        =
AI Shopping Assistant
```

---

## 📄 License

Add the appropriate project license here when the project license is finalized.
