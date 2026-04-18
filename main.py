from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Ganesh FastAPI App",
    description="DevOps CI/CD demo – FastAPI on Kubernetes",
    version="1.0.0",
)

templates = Jinja2Templates(directory="/code")


@app.get("/")
def home(request: Request):
    """Serve the main welcome page."""
    return templates.TemplateResponse("form.html", {"request": request})


@app.get("/health")
def health_check():
    """Health-check endpoint used by Kubernetes liveness/readiness probes."""
    return JSONResponse(status_code=200, content={"status": "healthy"})
