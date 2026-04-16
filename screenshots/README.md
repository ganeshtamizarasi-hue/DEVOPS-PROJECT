# Screenshots

Add your screenshots here after completing the project setup.

| File name | What to capture |
|-----------|----------------|
| `jenkins-pipeline.png` | Jenkins Stage View — all stages green |
| `sonarqube-analysis.png` | SonarQube project — Quality Gate Passed |
| `trivy-scan.png` | Trivy CVE scan output from Jenkins build artifacts |
| `ecr-image.png` | AWS ECR console — image with build number tag |
| `kubernetes-pods.png` | PuTTY terminal — `kubectl get pods` output |
| `prometheus-targets.png` | Prometheus → Status → Targets — all UP |
| `grafana-dashboard.png` | Grafana live dashboard with metrics |
| `fastapi-app.png` | Browser showing live FastAPI app |

## How to Take Screenshots on Windows
- Press `Win + Shift + S` to snip any area of your screen
- Save as PNG into this folder
- Commit and push to GitHub:
  ```
  git add screenshots/
  git commit -m "Add project screenshots"
  git push
  ```
