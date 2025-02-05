from fastapi import FastAPI
from routers import contact_router

app = FastAPI()

app.include_router(contact_router.router, tags=["Contacts CRUD"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
