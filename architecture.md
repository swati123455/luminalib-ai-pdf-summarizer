# LuminaLib – Architecture Overview

## 1. Introduction

LuminaLib is an intelligent, content-aware library backend designed using Clean Architecture principles.  
The system ingests uploaded PDF books, processes them asynchronously using an LLM, and stores AI-generated summaries for later retrieval.

The primary goal of this architecture is:

- Extensibility
- Provider independence
- Asynchronous processing
- Production readiness
- Clear separation of concerns

---

## 2. High-Level Architecture

The application follows **Clean Architecture** with layered separation:

API Layer \
↓ \
Service Layer (Business Logic) \
↓ \
Domain Layer (Entities / Models) \
↓ \
Infrastructure Layer (DB / External Services)


### Components

- FastAPI REST API
- PostgreSQL Database
- Background ingestion pipeline
- Pluggable LLM providers
- Dockerized deployment
- Ollama (Local LLM Runtime)

---

## 3. Layered Design

### 3.1 API Layer (`app/api/`)

Responsibilities:
- HTTP request handling
- Authentication
- File upload endpoints
- Dependency injection

Example:
- `/auth/login`
- `/books/` upload endpoint

The API layer contains **no business logic**.

---

### 3.2 Service Layer (`app/services/`)

Core application logic lives here.

Services include:

- `AuthService`
- `BookService`
- `IngestionService`
- `LLMProvider`

Responsibilities:
- Business workflows
- Orchestration
- External integrations

Example flow:
Upload Book → Save Metadata → Background Ingestion → LLM Summary → DB Update


---

### 3.3 Domain Layer (`app/domain/`)

Contains pure business entities:

- `User`
- `Book`

This layer is independent of frameworks and external systems.

---

### 3.4 Infrastructure Layer (`app/infrastructure/`)

Handles external dependencies:

- Database sessions
- ORM configuration
- Storage interaction

Technologies:
- SQLAlchemy Async ORM
- AsyncPG driver

---

## 4. Dependency Injection & Provider Pattern

A core requirement was the ability to swap LLM providers easily.

LuminaLib implements a **provider-based abstraction**:

IngestionService \
↓ \
LLM Provider Interface \
↓ \
<<<<<<< HEAD
┌───────────────┬───────────────┐
│ \ MockLLM │ OllamaLLM │
=======
┌───────────────┬───────────────┐\
│ MockLLM │ OllamaLLM │
>>>>>>> ac7ae01 (Update README, architecture, Docker setup and TinyLlama provider)
│ (Testing) │ (Real AI) │
└───────────────┴───────────────┘


### Supported Providers

1. **Mock LLM**
   - Used for testing
   - No external dependencies

2. **Ollama Provider**
   - Uses local Llama3 / TinyLlama models
   - Fully offline AI processing

The provider can be swapped by changing configuration without modifying business logic.

---

## 5. File Ingestion Pipeline

### Workflow

1. User uploads PDF
2. File stored locally
3. Background task triggered
4. PDF text extracted
5. Text split into chunks
6. Each chunk summarized via LLM
7. Partial summaries combined
8. Final summary generated
9. Stored in PostgreSQL

### Why Chunking?

LLMs have token limits.  
Chunking enables processing large documents safely.

PDF → Text → Chunks → Partial Summaries → Final Summary


---

## 6. Asynchronous Processing

Ingestion runs as a **FastAPI background task**.

Benefits:

- Non-blocking API responses
- Better scalability
- Improved user experience

User receives immediate response while AI processing continues.

---

## 7. Database Design

### Tables

#### Users
- id
- email
- hashed_password

#### Books
- id
- title
- file_path
- owner_id
- summary

Relationship:
User (1) → (N) Books


---

## 8. Authentication

JWT-based authentication:

- Password hashing via bcrypt
- Token generation using JWT
- Protected endpoints require authorization header

---

## 9. Dockerized Deployment

Entire stack runs using:

docker compose up

Services:

- API container
- PostgreSQL container
- Ollama container

Benefits:
- Reproducible environment
- One-command startup
- Easy evaluation

---

## 10. LLM Integration Strategy

The system is intentionally LLM-agnostic.

Possible providers:

- Ollama (Local Llama3)
- OpenAI API
- Mock LLM (Testing)

Only the provider implementation changes.

No business logic modification required.

---

## 11. Error Handling Strategy

Handled at multiple levels:

- API validation errors
- DB transaction rollback
- Background task isolation
- Provider failure protection

---

## 12. Scalability Considerations

Future improvements:

- Message queue (Celery / Redis)
- Object storage (S3)
- Vector database for semantic search
- Recommendation engine

---

## 13. Design Decisions

| Decision | Reason |
|---------|--------|
| Clean Architecture | Maintainability |
| Async SQLAlchemy | Performance |
| Background Tasks | Non-blocking ingestion |
| Provider Pattern | LLM swap capability |
| Docker | Reproducibility |

---

## 14. Conclusion

LuminaLib demonstrates a production-oriented backend architecture capable of:

- Handling real file ingestion
- Integrating AI services asynchronously
- Supporting multiple LLM providers
- Running fully containerized

The system is designed for extensibility and operational maturity rather than simple CRUD functionality.
