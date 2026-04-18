from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(
    title="AWS DevOps CI/CD Pipeline - FastAPI App",
    version="1.0.0",
)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>FastAPI DevOps Project</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #0a0f1e 0%, #0d1b35 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #e2e8f0;
            }
            .card {
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(59,130,246,0.3);
                border-radius: 16px;
                padding: 48px 56px;
                text-align: center;
                max-width: 560px;
                width: 90%;
            }
            .badge {
                display: inline-block;
                background: rgba(59,130,246,0.15);
                border: 1px solid rgba(59,130,246,0.4);
                color: #60a5fa;
                font-size: 12px;
                font-weight: 600;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                padding: 6px 16px;
                border-radius: 20px;
                margin-bottom: 24px;
            }
            h1 {
                font-size: 32px;
                font-weight: 700;
                margin-bottom: 12px;
                background: linear-gradient(135deg, #3b82f6, #06b6d4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            p {
                color: #94a3b8;
                font-size: 15px;
                line-height: 1.6;
                margin-bottom: 32px;
            }
            .stack {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                justify-content: center;
                margin-bottom: 32px;
            }
            .pill {
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.1);
                color: #cbd5e1;
                font-size: 12px;
                padding: 4px 12px;
                border-radius: 20px;
            }
            .btn {
                background: #2563eb;
                color: white;
                border: none;
                padding: 12px 28px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
            }
            .btn:hover { background: #1d4ed8; }
            .status {
                margin-top: 24px;
                font-size: 13px;
                color: #22c55e;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="badge">Production</div>
            <h1>AWS DevOps CI/CD Pipeline</h1>
            <p>FastAPI application deployed via Jenkins pipeline on Kubernetes cluster in AWS ap-south-1.</p>
            <div class="stack">
                <span class="pill">Jenkins</span>
                <span class="pill">Docker</span>
                <span class="pill">SonarQube</span>
                <span class="pill">Trivy</span>
                <span class="pill">AWS ECR</span>
                <span class="pill">Kubernetes</span>
                <span class="pill">Terraform</span>
                <span class="pill">Prometheus</span>
                <span class="pill">Grafana</span>
            </div>
            <button class="btn" onclick="checkHealth()">Check Health</button>
            <div class="status" id="status"></div>
        </div>
        <script>
            function checkHealth() {
                fetch('/health')
                    .then(r => r.json())
                    .then(d => {
                        document.getElementById('status').innerText = '✓ App Status: ' + d.status;
                    });
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health")
def health():
    return JSONResponse(status_code=200, content={"status": "healthy"})
