from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from routes import auth_router

# Create the FastAPI app
app = FastAPI()

# CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend) from 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define routes to serve HTML files
@app.get("/", response_class=HTMLResponse)
async def read_index():
    home_path = os.path.join(os.getcwd(), "static", "home.html")
    with open(home_path) as f:
        return HTMLResponse(content=f.read())
    
@app.get("/home", response_class=HTMLResponse)
async def read_home():
    home_path = os.path.join(os.getcwd(), "static", "home.html")
    with open(home_path) as f:
        return HTMLResponse(content=f.read())    

@app.get("/login", response_class=HTMLResponse)
async def read_login():
    login_path = os.path.join(os.getcwd(), "static", "login.html")
    with open(login_path) as f:
        return HTMLResponse(content=f.read())

@app.get("/register", response_class=HTMLResponse)
async def read_register():
    register_path = os.path.join(os.getcwd(), "static", "register.html")
    with open(register_path) as f:
        return HTMLResponse(content=f.read())

# Include auth routes
app.include_router(auth_router)

# Start the FastAPI app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
