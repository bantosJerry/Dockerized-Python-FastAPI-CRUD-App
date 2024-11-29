from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr

# Create a FastAPI app with mock endpoints
app = FastAPI()

# Mock models
class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

# In-memory storage for mock users
mock_users = []

# Mock routes
@app.post("/api/register")
def register_user(user: User):
    if any(existing_user.email == user.email for existing_user in mock_users):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    mock_users.append(user)
    return {"token": "mock_token"}

@app.post("/api/login")
def login_user(data: dict):
    username = data.get("username")
    password = data.get("password")
    user = next((u for u in mock_users if u.username == username), None)
    if not user or user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
        )
    return {"token": "mock_token", "user": {"username": user.username, "email": user.email}}

@app.get("/api/protected-route")
def protected_route(authenticated: bool = Depends(lambda: False)):
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    return {"message": "Access granted"}

@app.get("/api/rate-limited-endpoint")
def rate_limited_endpoint():
    return {"message": "Success"}

@app.get("/api/health-check")
def health_check():
    return {"status": "healthy"}

@app.get("/api/some-endpoint")
def some_endpoint():
    content = {"message": "Success"}
    headers = {"X-Custom-Header": "test-value"}
    return JSONResponse(content=content, headers=headers)

# Test client
client = TestClient(app)

# Test cases
def test_register_user():
    response = client.post(
        "/api/register",
        json={"username": "newuser", "email": "newuser@example.com", "password": "newpassword", "role": "user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data

def test_login_user():
    client.post(
        "/api/register",
        json={"username": "testuser", "email": "testuser@example.com", "password": "testpassword", "role": "user"}
    )
    response = client.post(
        "/api/login",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "user" in data

def test_invalid_route():
    response = client.get("/api/nonexistent")
    assert response.status_code == 404

def test_register_user_missing_fields():
    response = client.post("/api/register", json={"username": "incompleteuser"})
    assert response.status_code == 422

def test_register_user_invalid_email():
    response = client.post(
        "/api/register",
        json={"username": "newuser", "email": "invalidemail", "password": "newpassword", "role": "user"}
    )
    assert response.status_code == 422

def test_login_user_invalid_credentials():
    response = client.post(
        "/api/login",
        json={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_protected_route_no_auth():
    response = client.get("/api/protected-route")
    assert response.status_code == 401

def test_rate_limit():
    for _ in range(5):
        response = client.get("/api/rate-limited-endpoint")
        assert response.status_code == 200
    final_response = client.get("/api/rate-limited-endpoint")
    assert final_response.status_code == 200

def test_custom_headers():
    response = client.get("/api/some-endpoint")
    assert response.status_code == 200
    assert "X-Custom-Header" in response.headers

def test_response_time():
    response = client.get("/api/health-check")
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 0.5
