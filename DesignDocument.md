# Design Document: INI8 Document Management System (PoC)

## Overview

This document outlines the design of a Proof-of-Concept (PoC) full-stack document management system built for INI8 Labs. The system allows uploading, listing, downloading, and deleting PDF health documents tied to unique patient IDs. It includes authentication, file validation, secure storage, and scalable service orchestration using Docker.

---

## Objectives

- Secure upload and storage of patient-related PDF documents
- Retrieve, list, and delete documents via authenticated API
- Provide a simple, responsive web UI for the system
- Containerized deployment via Docker Compose

---

## Architecture Overview

```
+-------------+        +----------------+        +---------------+
|   Frontend  |  <---> |   Flask API    |  <---> | PostgreSQL DB |
| React + MUI |        | Python + JWT   |        | File metadata |
+-------------+        +----------------+        +---------------+
       |                        |                        |
       |                        +--> Redis Cache (opt.)  |
       |                        |                        |
       +--> Docker Compose -->  All services orchestrated
```

---

## Components

### 1. **Frontend (React + Material UI)**

- Upload PDF via drag-drop or file selector
- Input patient ID
- Display uploaded files (with download/delete buttons)
- Handles JWT token in localStorage for auth

### 2. **Backend (Flask REST API)**

- Endpoints:
  - `/login`: Authenticate user
  - `/documents/upload`: Upload document (protected)
  - `/documents`: List documents (protected)
  - `/documents/<id>/download`: Download (protected)
  - `/documents/<id>`: Delete (protected)
- JWT-based authorization
- Uses `Flask-RESTful`, `Flask-JWT-Extended`, `Flask-SQLAlchemy`

### 3. **Database (PostgreSQL)**

- Stores file metadata:
  - Filename
  - Patient ID
  - Upload timestamp
  - Uploaded by (optional)

### 4. **Caching (Redis)**

- Caches file listing (`/documents`) for performance
- TTL: 30 seconds

---

## Authentication

- Login with hardcoded credentials (for PoC)
- JWT is issued upon login
- All protected endpoints require `Authorization: Bearer <token>`

---

## File Upload Logic

- Validates file type (`.pdf`)
- Max size: 10MB
- Saved to `uploads/` inside the Flask container
- Filename collisions are handled by UUID renaming
- Metadata is saved to PostgreSQL

---

## Docker Orchestration

- Services defined in `docker-compose.yml`:
  - `frontend`: React app
  - `backend`: Flask API
  - `db`: PostgreSQL (persistent volume)
  - `redis`: Caching service (optional)

```yaml
services:
  db:
    image: postgres
    ...
  redis:
    image: redis
    ...
  backend:
    build: ./ini8_backend
    ...
  frontend:
    build: ./ini8-frontend
    ...
```

- Environment variables are passed via `docker-compose.yml` and `.env`

---

## Assumptions

- Admin credentials are hardcoded (`admin:password`)
- No user registration or RBAC
- Only `.pdf` files accepted
- Local volume used for file storage
- Redis is optional but included for caching demonstration
- Not built for production — this is a PoC

---

## Future Improvements

- User registration & role-based access control
- File versioning
- Upload progress and error handling UI
- Pagination and filtering for file list
- Cloud storage integration (e.g., S3)
- CI/CD pipeline for production readiness

---

## Author

**Candidate**: Segu Sai Bharadwaj
**Submission**: INI8 Labs Full-Stack Developer Assignment  
**Date**: July 2025
