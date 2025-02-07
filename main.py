from fastapi import FastAPI
from routers import contact_router, auth_router
from fastapi.openapi.utils import get_openapi

app = FastAPI()

app.include_router(contact_router.router, tags=["Contacts CRUD"])
app.include_router(auth_router.router, tags = ["Authentication"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Contacts API",
        version="1.0.0",
        description="API for managing contacts with JWT authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path:
            path[method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi  # Apply the schema fix

@app.get("/")
def root():
    return {"message": "Welcome to the Contacts API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
