# LuminaLib  — AI Powered PDF Summarization Backend

LuminaLib is an AI-powered backend system that allows users to upload PDF documents and automatically generate concise summaries using Large Language Models (LLMs).

The system demonstrates asynchronous processing, clean architecture, authentication, and pluggable AI provider integration.

---

##  Features

- User Authentication (JWT)
- Upload PDF documents
- Background ingestion pipeline
- PDF text extraction
- Chunk-based processing
- AI-powered summarization
- PostgreSQL database storage
- Async FastAPI backend
- Pluggable LLM provider architecture

---

## LLM Provider Architecture

The project is designed with a **provider-based AI architecture**, allowing different LLM backends to be used without modifying business logic.

### Supported Providers

####  Mock LLM Provider
- Used for development and testing
- Generates deterministic summaries
- Allows testing without AI cost or GPU usage

#### Ollama LLM Provider (Default)
- Runs **local AI models** (e.g., Llama3)
- No API cost
- Works offline
- Used by the current implementation

#### OpenAI Provider (Optional)
- Can be enabled by adding API key
- Same interface as other providers
- Easily switchable

---

### Provider Switching

The ingestion service depends only on an abstract LLM interface:

IngestionService → LLM Provider Interface → Actual Model


This means:

- No code changes required in ingestion logic
- Providers can be swapped based on requirements
- Supports scalability and experimentation

Example:

MockLLM → Testing,
OllamaProvider → Local AI,
OpenAIProvider → Cloud AI


---

## Architecture

The project follows **Clean Architecture** principles:

API Layer → Services → Domain Models → Infrastructure


### Components

- **FastAPI** – API framework
- **PostgreSQL** – Database
- **SQLAlchemy Async** – ORM
- **JWT Auth** – Authentication
- **Ollama / OpenAI / Mock LLM** – AI summarization
- **Background Tasks** – Async ingestion

---

## Project Structure
app/
├── api/ # API routes
│ └── v1/
├── core/ # configs & dependencies
├── domain/ # database models
├── infrastructure/ # DB setup
├── services/
│ ├── ingestion_service.py
│ ├── pdf_service.py
│ ├── llm_provider.py
│ └── mock_llm.py
└── workers/ # background processing

main.py
requirements.txt

## 🤖 LLM Provider Configuration

LuminaLib is designed using a **provider-based architecture**, allowing the AI engine to be swapped without modifying business logic.

The ingestion pipeline depends on an abstract LLM provider which can be changed based on requirements.

---

### Supported Providers

#### 1️⃣ Mock LLM (Default for Testing)

Used during development or when no AI service is available.

Location:
app/services/llm/mock_llm.py


Behavior:
- Returns simulated summaries
- No external dependencies
- Fast execution

---

#### 2️⃣ Ollama Provider (Local AI – Recommended)

The project currently utilizes **Ollama** with **TinyLlama / Llama3** for real AI-based summarization.

Benefits:
- Runs locally
- No API cost
- Offline processing
- Easily reproducible environment

Models supported:
- `tinyllama` (lightweight)
- `llama3` (higher quality)

---

## 🔄 How to Change LLM Provider

The provider is injected into the `IngestionService`.

### File to Modify
app/api/v1/books.py

---

### Example: Using Mock LLM

```python
from app.services.llm.mock_llm import MockLLM

ingestion = IngestionService(
    llm_provider=MockLLM()
)
```
### Example: Using Ollama (Real AI)
```python
from app.services.llm.ollama_provider import OllamaProvider

ingestion = IngestionService(
    llm_provider=OllamaProvider(model="tinyllama")
)
```
### Switching Model

Inside:
```bash
app/services/llm/ollama_provider.py
```

Change:
```bash
model="tinyllama"
```

to:
```bash
model="llama3"
```
## Setup Instructions

### 1️. Clone Repository

```bash
git clone <repo-url>
cd LuminaLib
```

### 2️. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3️. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️. Create .env

Create .env file:
```bash
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/luminalib
JWT_SECRET=your_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

(Optional — only if using OpenAI)
```bash
OPENAI_API_KEY=your_key
```

### 5️. Setup PostgreSQL

Create database:
```bash
CREATE DATABASE luminalib;
```

### 6️. Run Ollama (Local AI)

- **Install Ollama**: https://ollama.com

- **Start server**: ollama serve

- **Pull model**:
ollama pull llama3

### 7️. Run Backend
```bash
uvicorn app.main:app --reload
```

Open API docs:
http://127.0.0.1:8000/docs

## AI Processing Flow

1. User uploads PDF 
2. Background task triggered
3. PDF text extracted 
4. Text split into chunks 
5. Partial summaries generated 
6. Final summary created 
7. Summary stored in database

## API Endpoints
### 1. Authentication
```bash
POST /auth/signup

POST /auth/login
```

### 2. Books
```bash
POST /books/ → Upload PDF and generate summary
```

#### Example Database Result
```bash
SELECT summary FROM books;
```
Returns AI-generated summary of uploaded document.


## Author

Swati Angadi \
LLM and GenAI Engineer

### Project Goal

This project demonstrates how modern backend systems can integrate AI models using scalable architecture while remaining provider-agnostic and production-ready.


