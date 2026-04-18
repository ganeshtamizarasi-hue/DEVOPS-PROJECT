from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
 
app = FastAPI()
 
 
@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(content="""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <title>AWS DevOps CI/CD Pipeline</title>
</head>
<body>
    <h1>AWS DevOps CI/CD Pipeline</h1>
    <p>FastAPI running on Kubernetes</p>
</body>
</html>""")
 
 
@app.get("/health")
def health():
    return JSONResponse(status_code=200, content={"status": "healthy"})

