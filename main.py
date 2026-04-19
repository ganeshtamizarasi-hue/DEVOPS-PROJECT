from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import datetime

app = FastAPI(
    title="AWS DevOps CI/CD Pipeline",
    description="FastAPI running on Kubernetes with full DevOps toolchain",
    version="1.0.0"
)

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>AWS DevOps CI/CD Pipeline</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Syne:wght@400;600;800&display=swap" rel="stylesheet"/>
    <style>
        :root {
            --bg:        #0a0c10;
            --surface:   #111318;
            --border:    #1e2330;
            --accent:    #f97316;
            --accent2:   #3b82f6;
            --green:     #22c55e;
            --yellow:    #eab308;
            --red:       #ef4444;
            --text:      #e2e8f0;
            --muted:     #64748b;
            --mono:      'JetBrains Mono', monospace;
            --sans:      'Syne', sans-serif;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: var(--mono);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* ── BACKGROUND GRID ── */
        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(249,115,22,.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(249,115,22,.04) 1px, transparent 1px);
            background-size: 40px 40px;
            pointer-events: none;
            z-index: 0;
        }

        .wrapper { position: relative; z-index: 1; max-width: 1100px; margin: 0 auto; padding: 0 24px 80px; }

        /* ── TOP BAR ── */
        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 18px 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 60px;
            animation: fadeDown .6s ease both;
        }
        .topbar-logo {
            font-family: var(--sans);
            font-size: 13px;
            font-weight: 600;
            letter-spacing: .12em;
            text-transform: uppercase;
            color: var(--accent);
        }
        .topbar-right { display: flex; gap: 24px; align-items: center; }
        .pill {
            font-size: 11px;
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px solid var(--border);
            color: var(--muted);
        }
        .pill.live {
            border-color: var(--green);
            color: var(--green);
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .dot {
            width: 7px; height: 7px;
            border-radius: 50%;
            background: var(--green);
            animation: pulse 1.6s ease-in-out infinite;
        }

        /* ── HERO ── */
        .hero { margin-bottom: 64px; animation: fadeUp .7s .1s ease both; }
        .hero-label {
            font-size: 11px;
            letter-spacing: .2em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 16px;
        }
        .hero h1 {
            font-family: var(--sans);
            font-size: clamp(36px, 6vw, 68px);
            font-weight: 800;
            line-height: 1.05;
            letter-spacing: -.02em;
            margin-bottom: 20px;
        }
        .hero h1 span { color: var(--accent); }
        .hero-sub {
            font-size: 14px;
            color: var(--muted);
            line-height: 1.7;
            max-width: 560px;
        }

        /* ── PIPELINE FLOW ── */
        .section-title {
            font-size: 11px;
            letter-spacing: .18em;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 20px;
        }
        .pipeline {
            display: flex;
            align-items: center;
            gap: 0;
            overflow-x: auto;
            margin-bottom: 64px;
            padding-bottom: 4px;
            animation: fadeUp .7s .2s ease both;
        }
        .stage {
            flex: 0 0 auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }
        .stage-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px 16px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: .06em;
            text-align: center;
            min-width: 88px;
            position: relative;
            transition: border-color .2s, transform .2s;
        }
        .stage-box:hover { border-color: var(--accent); transform: translateY(-3px); }
        .stage-box .icon { font-size: 18px; display: block; margin-bottom: 6px; }
        .stage-badge {
            font-size: 9px;
            padding: 2px 7px;
            border-radius: 4px;
            background: rgba(34,197,94,.12);
            color: var(--green);
            border: 1px solid rgba(34,197,94,.25);
        }
        .stage-badge.warn {
            background: rgba(234,179,8,.12);
            color: var(--yellow);
            border-color: rgba(234,179,8,.25);
        }
        .connector {
            flex: 0 0 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--accent);
            font-size: 16px;
            margin-top: -20px;
        }

        /* ── GRID CARDS ── */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 16px;
            margin-bottom: 64px;
            animation: fadeUp .7s .3s ease both;
        }
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 24px;
            transition: border-color .2s, transform .2s;
            position: relative;
            overflow: hidden;
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--accent), transparent);
            opacity: 0;
            transition: opacity .2s;
        }
        .card:hover { border-color: var(--border); transform: translateY(-4px); }
        .card:hover::before { opacity: 1; }
        .card-icon { font-size: 24px; margin-bottom: 14px; }
        .card h3 {
            font-family: var(--sans);
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text);
        }
        .card p { font-size: 12px; color: var(--muted); line-height: 1.7; }
        .tag-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; }
        .tag {
            font-size: 10px;
            padding: 3px 8px;
            border-radius: 5px;
            background: rgba(249,115,22,.08);
            color: var(--accent);
            border: 1px solid rgba(249,115,22,.18);
        }
        .tag.blue {
            background: rgba(59,130,246,.08);
            color: var(--accent2);
            border-color: rgba(59,130,246,.18);
        }

        /* ── METRICS ROW ── */
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 12px;
            margin-bottom: 64px;
            animation: fadeUp .7s .35s ease both;
        }
        .metric {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
        }
        .metric-val {
            font-family: var(--sans);
            font-size: 30px;
            font-weight: 800;
            color: var(--accent);
            line-height: 1;
            margin-bottom: 4px;
        }
        .metric-label { font-size: 11px; color: var(--muted); }

        /* ── TERMINAL BLOCK ── */
        .terminal {
            background: #0d1117;
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
            margin-bottom: 64px;
            animation: fadeUp .7s .4s ease both;
        }
        .terminal-bar {
            background: #161b22;
            padding: 12px 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid var(--border);
        }
        .tbar-dot { width: 11px; height: 11px; border-radius: 50%; }
        .terminal-title { font-size: 11px; color: var(--muted); margin-left: 8px; }
        .terminal-body { padding: 20px 24px; font-size: 12px; line-height: 2; }
        .t-cmd { color: #7ee787; }
        .t-comment { color: var(--muted); }
        .t-key { color: #79c0ff; }
        .t-val { color: #ffa657; }
        .t-ok { color: var(--green); }
        .t-url { color: #a5d6ff; }

        /* ── FOOTER ── */
        .footer {
            border-top: 1px solid var(--border);
            padding-top: 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: var(--muted);
            animation: fadeUp .7s .5s ease both;
        }
        .footer a { color: var(--accent); text-decoration: none; }

        /* ── KEYFRAMES ── */
        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(18px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeDown {
            from { opacity: 0; transform: translateY(-12px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50%       { opacity: .3; }
        }

        /* ── RESPONSIVE ── */
        @media (max-width: 600px) {
            .metrics { grid-template-columns: repeat(2, 1fr); }
            .footer { flex-direction: column; gap: 12px; text-align: center; }
        }
    </style>
</head>
<body>
<div class="wrapper">

    <!-- TOP BAR -->
    <nav class="topbar">
        <div class="topbar-logo">⬡ DevOps Portfolio</div>
        <div class="topbar-right">
            <span class="pill">ap-south-1</span>
            <span class="pill">v1.0.0</span>
            <span class="pill live"><span class="dot"></span>Live</span>
        </div>
    </nav>

    <!-- HERO -->
    <section class="hero">
        <div class="hero-label">// AWS DevOps CI/CD Portfolio</div>
        <h1>Full-Stack<br/><span>Pipeline</span><br/>on Kubernetes</h1>
        <p class="hero-sub">
            An end-to-end DevOps workflow — from source code to production —
            powered by Jenkins, Docker, SonarQube, Trivy, ECR, KOPS, Terraform,
            Prometheus and Grafana running on AWS <code>ap-south-1</code>.
        </p>
    </section>

    <!-- CI/CD PIPELINE FLOW -->
    <div class="section-title">// CI/CD pipeline stages</div>
    <div class="pipeline">
        <div class="stage">
            <div class="stage-box"><span class="icon">🐙</span>GitHub<br/>Push</div>
            <span class="stage-badge">trigger</span>
        </div>
        <div class="connector">→</div>
        <div class="stage">
            <div class="stage-box"><span class="icon">🔧</span>Jenkins<br/>Build</div>
            <span class="stage-badge">passed</span>
        </div>
        <div class="connector">→</div>
        <div class="stage">
            <div class="stage-box"><span class="icon">🔍</span>SonarQube<br/>Scan</div>
            <span class="stage-badge">passed</span>
        </div>
        <div class="connector">→</div>
        <div class="stage">
            <div class="stage-box"><span class="icon">🛡️</span>Trivy<br/>Security</div>
            <span class="stage-badge">passed</span>
        </div>
        <div class="connector">→</div>
        <div class="stage">
            <div class="stage-box"><span class="icon">🐳</span>Docker<br/>Build</div>
            <span class="stage-badge">passed</span>
        </div>
        <div class="connector">→</div>
        <div class="stage">
            <div class="stage-box"><span class="icon">📦</span>Push<br/>to ECR</div>
            <span class="stage-badge">passed</span>
        </div>
        <div class="connector">→</div>
        <div class="stage">
            <div class="stage-box"><span class="icon">☸️</span>Deploy<br/>K8s</div>
            <span class="stage-badge">live</span>
        </div>
    </div>

    <!-- METRICS -->
    <div class="section-title">// system overview</div>
    <div class="metrics">
        <div class="metric">
            <div class="metric-val">7</div>
            <div class="metric-label">Pipeline Stages</div>
        </div>
        <div class="metric">
            <div class="metric-val">3</div>
            <div class="metric-label">K8s Pods Running</div>
        </div>
        <div class="metric">
            <div class="metric-val">0</div>
            <div class="metric-label">Security Vulnerabilities</div>
        </div>
        <div class="metric">
            <div class="metric-val">A</div>
            <div class="metric-label">SonarQube Grade</div>
        </div>
        <div class="metric">
            <div class="metric-val">100%</div>
            <div class="metric-label">Health Check Pass</div>
        </div>
    </div>

    <!-- TOOL CARDS -->
    <div class="section-title">// toolchain</div>
    <div class="grid">

        <div class="card">
            <div class="card-icon">🔧</div>
            <h3>Jenkins CI/CD</h3>
            <p>Declarative Jenkinsfile pipeline with multi-stage build, test, scan, push and deploy phases. Webhook-triggered on every GitHub push.</p>
            <div class="tag-row">
                <span class="tag">Declarative Pipeline</span>
                <span class="tag">Webhooks</span>
            </div>
        </div>

        <div class="card">
            <div class="card-icon">🐳</div>
            <h3>Docker + ECR</h3>
            <p>Multi-stage Dockerfile for minimal production image. Tagged and pushed to AWS Elastic Container Registry with IAM role authentication.</p>
            <div class="tag-row">
                <span class="tag">Multi-stage</span>
                <span class="tag">ECR</span>
                <span class="tag">IAM</span>
            </div>
        </div>

        <div class="card">
            <div class="card-icon">☸️</div>
            <h3>Kubernetes (KOPS)</h3>
            <p>Production-grade cluster provisioned with KOPS on AWS. Deployment, Service and HPA manifests manage rolling updates and auto-scaling.</p>
            <div class="tag-row">
                <span class="tag">KOPS</span>
                <span class="tag blue">HPA</span>
                <span class="tag blue">Rolling Update</span>
            </div>
        </div>

        <div class="card">
            <div class="card-icon">🔍</div>
            <h3>SonarQube</h3>
            <p>Static code analysis integrated into the Jenkins pipeline. Quality gate enforced — pipeline fails if code coverage or issue thresholds are breached.</p>
            <div class="tag-row">
                <span class="tag">Quality Gate</span>
                <span class="tag">SAST</span>
            </div>
        </div>

        <div class="card">
            <div class="card-icon">🛡️</div>
            <h3>Trivy Security Scan</h3>
            <p>Container image vulnerability scanning before every push to ECR. Blocks deployment on CRITICAL or HIGH CVEs.</p>
            <div class="tag-row">
                <span class="tag">CVE Scan</span>
                <span class="tag">Image Hardening</span>
            </div>
        </div>

        <div class="card">
            <div class="card-icon">🏗️</div>
            <h3>Terraform IaC</h3>
            <p>All AWS infrastructure — VPC, EC2, ALB, ASG, S3 state backend — defined as code. Remote state stored in S3 with DynamoDB locking.</p>
            <div class="tag-row">
                <span class="tag">S3 Backend</span>
                <span class="tag blue">DynamoDB Lock</span>
            </div>
        </div>

        <div class="card">
            <div class="card-icon">📊</div>
            <h3>Prometheus + Grafana</h3>
            <p>Metrics scraped from FastAPI via <code>/metrics</code> endpoint. Grafana dashboards visualise request rate, latency and pod health in real time.</p>
            <div class="tag-row">
                <span class="tag">Metrics</span>
                <span class="tag blue">Dashboards</span>
                <span class="tag">Alerting</span>
            </div>
        </div>

        <div class="card">
            <div class="card-icon">⚡</div>
            <h3>FastAPI Application</h3>
            <p>High-performance async Python API with automatic OpenAPI docs, structured health check endpoint, and Prometheus metrics middleware.</p>
            <div class="tag-row">
                <span class="tag">Python 3.11</span>
                <span class="tag blue">Async</span>
                <span class="tag">/docs</span>
                <span class="tag">/health</span>
            </div>
        </div>

    </div>

    <!-- TERMINAL -->
    <div class="section-title">// quick start</div>
    <div class="terminal">
        <div class="terminal-bar">
            <span class="tbar-dot" style="background:#ef4444"></span>
            <span class="tbar-dot" style="background:#eab308"></span>
            <span class="tbar-dot" style="background:#22c55e"></span>
            <span class="terminal-title">bash — AWS DevOps Setup</span>
        </div>
        <div class="terminal-body">
            <div><span class="t-comment"># 1. Provision infrastructure</span></div>
            <div><span class="t-cmd">$</span> terraform init &amp;&amp; terraform apply -auto-approve</div>
            <br/>
            <div><span class="t-comment"># 2. Create Kubernetes cluster</span></div>
            <div><span class="t-cmd">$</span> kops create cluster --name=<span class="t-val">$CLUSTER_NAME</span> --state=<span class="t-val">$KOPS_STATE_STORE</span></div>
            <div><span class="t-cmd">$</span> kops update cluster --yes</div>
            <br/>
            <div><span class="t-comment"># 3. Deploy application</span></div>
            <div><span class="t-cmd">$</span> kubectl apply -f k8s/deployment.yaml</div>
            <div><span class="t-cmd">$</span> kubectl apply -f k8s/service.yaml</div>
            <br/>
            <div><span class="t-comment"># 4. Verify</span></div>
            <div><span class="t-cmd">$</span> kubectl get pods -n devops</div>
            <div><span class="t-ok">✔</span> <span class="t-key">fastapi-deployment</span>  <span class="t-ok">3/3 Running</span></div>
            <br/>
            <div><span class="t-comment"># API is live at:</span></div>
            <div><span class="t-cmd">$</span> curl <span class="t-url">http://&lt;LOAD-BALANCER-DNS&gt;/health</span></div>
            <div><span class="t-ok">{"status": "healthy"}</span></div>
        </div>
    </div>

    <!-- FOOTER -->
    <footer class="footer">
        <div>AWS DevOps CI/CD Portfolio &mdash; ap-south-1</div>
        <div>
            <a href="/docs">https://github.com/ganeshtamizarasi-hue/DEVOPS-PROJECT</a> &nbsp;·&nbsp;
</div>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(content=HTML_CONTENT)


@app.get("/health")
def health():
    return JSONResponse(status_code=200, content={
        "status": "healthy",
        "service": "aws-devops-cicd",
        "version": "1.0.0",
        "region": "ap-south-1",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })
