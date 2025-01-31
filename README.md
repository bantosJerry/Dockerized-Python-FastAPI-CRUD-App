
# Dockerized Python FastAPI CRUD Application
A simple CRUD application built with Python's FastAPI framework, using Docker for containerization. It includes user registration, login, and management features, backed by a PostgreSQL database.

A PostgreSQL database is used to persist user data, while the FastAPI application provides API endpoints for CRUD operations. The application is containerized using Docker, ensuring a consistent development and deployment environment.

## Prerequisites
- Docker  
- Docker Compose  

## Setup
Clone the repository
```bash
git clone <repo_url>
cd Dockerized-Python-FastAPI-CRUD-App
```

### Starting the Application
To build and start the application along with the PostgreSQL database, run:

```bash
docker-compose up --build
```

This will:
- Start the PostgreSQL database on port `5433`.
- Build and run the FastAPI application on port `8080`.

Visit `http://localhost:8080` to access the application.

## Project Structure
- `Dockerfile`: Defines the container setup for the FastAPI application and testing environments.  
- `docker-compose.yml`: Configuration for running the app, database, and tests as services.  
- `main.py`: The entry point of the FastAPI application.  
- `requirements.txt`: Dependency management file for Python packages.  
- `tests/`: Contains tests for the application.

## Notes
- Ensure that Docker and Docker Compose are installed on your system before running the application.  
- Modify the `docker-compose.yml` or `.env` file if you need to change the database credentials or ports.  
- The database service runs on port `5433` (mapped from `5432` inside the container).  
- The FastAPI application runs on port `8080`.  
- Tests will automatically run after starting the application if configured in the `docker-compose.yml`.
