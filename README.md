# INI8 Document Management System – Full Stack PoC

This is a full-stack Proof-of-Concept (PoC) document management system for INI8 Labs. It allows authenticated users to upload,list view, download, and delete patient-related PDF documents.

---

## Tech Stack

- **Frontend**: React.js, Material UI
- **Backend**: Flask (REST API)
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Token)
- **Orchestration**: Docker & Docker Compose
- **Optional**: Redis caching for file listing

---

## Setup Instructions

### Prerequisites

- Docker + Docker Compose
- Git

### Run via Docker Compose

```bash
git clone <your-repo-url>
cd ini8_assessment

# Build and run all services
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

---

## Default Credentials

| Username | Password |
|----------|----------|
| admin    | password |

---

## API Endpoints (Protected)

| Method | Endpoint         | Description          |
|--------|------------------|----------------------|
| POST   | `/login`     | Get JWT token        |
| POST   | `/documents/upload`    | Upload PDF           |
| GET    | `/documents`     | List uploaded documents  |
| GET    | `/documents/<id>/download` | Download file |
| DELETE | `/documents/<id>` | Delete file   |

Use the JWT token in headers:

```
Authorization: Bearer <your_token>
```

---

## Example Requests

### Login (get token)

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### Upload PDF

```bash
curl -X POST http://localhost:5000/documents/upload \
  -H "Authorization: Bearer <token>" \
  -F "file=@test.pdf" \
  -F "patient_id=patient123"
```

## Design Document

See [DesignDocument.md](./DesignDocument.md) for architecture and details.

---

## Folder Structure

```
├── ini8-frontend/
├── ini8_backend/
├── docker-compose.yml
├── README.md
├── DesignDocument.md
```

---

## Author

**Candidate**: Segu Sai Bharadwaj
**Submitted to**: INI8 Labs  
**Date**: July 2025
