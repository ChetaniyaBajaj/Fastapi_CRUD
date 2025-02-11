from fastapi import FastAPI
from routers import contact_router, auth_router
from database.database import Base, engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router.router, tags=["Authentication"])
app.include_router(contact_router.router, tags=["Contacts CRUD"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
