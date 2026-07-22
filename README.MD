# RAG Fin

A Retrieval-Augmented Generation (RAG) backend application for financial data analysis.

## Architecture

- **FastAPI** - Web framework for building APIs
- **PostgreSQL** - Primary database
- **Qdrant** - Vector database for embeddings
- **Redis** - Caching layer
- **OpenAI** - LLM and embedding models

## Project Structure

```
backend/
├── app/
│   ├── api/          # API routes and configuration
│   ├── database/     # Database models and connection
│   ├── ingestion/    # Data ingestion pipelines
│   ├── models/       # ML/AI model definitions
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic services
│   └── utils/        # Utility functions
├── storage/          # File storage
│   └── reports/      # Generated reports
└── tests/            # Test suite
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your configuration values:
   ```bash
   cp backend/.env.example backend/.env
   ```
5. Run the application:
   ```bash
   uvicorn app.api.app:app --reload
   ```

## Environment Variables

See `backend/.env.example` for all required configuration values.

## API Endpoints

- `GET /` - Health check endpoint

