# Research

## Decisions

### Language/Runtime
- Decision: Python 3.11
- Rationale: Mature web ecosystem, strong typing support with Pydantic, and common in CMS backends.
- Alternatives considered: Node.js 20, Java 17

### Web Framework
- Decision: FastAPI
- Rationale: Clear API contracts, async support for file uploads, integrates with OpenAPI.
- Alternatives considered: Django, Flask

### Persistence
- Decision: PostgreSQL for relational data; object storage for manuscript files.
- Rationale: Strong relational integrity for submissions/reviews; object storage for large files.
- Alternatives considered: MySQL, SQLite (insufficient for scale)

### Testing
- Decision: pytest
- Rationale: Standard Python testing with rich fixtures for integration testing.
- Alternatives considered: unittest, nose

### Deployment Target
- Decision: Linux server
- Rationale: Standard production target for Python services.
- Alternatives considered: Windows Server, serverless only
