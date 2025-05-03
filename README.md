# Multi-Service Kubernetes Demo

A production-ready Kubernetes demonstration using Kind, featuring multiple microservices:
- Flask-based visitor counter with metrics
- PHP environment diagnostics service
- Nginx static content server
- Ingress-based routing with domain mapping

## Table of Contents
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Development Guide](#development-guide)
- [Monitoring](#monitoring)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Cleanup](#cleanup)
- [Contributing](#contributing)
- [Security Notes](#security-notes)

## Quick Start

```bash
# 1. Create cluster
kind create cluster --config k8s/configs/kind-ingress-config

# 2. Setup namespace
kubectl create ns sir-ns
kubens sir-ns

# 3. Install ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml

# 4. Wait for ingress
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

## Architecture

### Components
- **Flask App**: Visitor tracking service with Prometheus metrics
- **PHP App**: System diagnostics and environment information
- **Nginx**: Static content delivery
- **Ingress**: Domain-based routing to services

### Access Points
- Visitor Counter: http://sirrupesh.localhost
- System Info: http://app4.localhost
- Static Content: http://cambridge.localhost

## Development Guide

### Prerequisites
- Docker 20.10.0+
- Kind 0.11.0+
- kubectl 1.20.0+
- kubens
- Helm v3 (dashboard)
- Kustomize

### Local Setup

1. **Configure Secrets**
```bash
kubectl create secret generic openai-secret --from-literal=api-key="your-api-key"
```

2. **Build Images**
```bash
# Build all services
docker build -t sirrupesh/app4:latest src/app4/
docker build -t sirrupesh/flask:latest src/app/
docker build -t sirrupesh/nginx:latest src/nginx/

# Load into Kind
kind load docker-image sirrupesh/app4:latest --name sir-multi-node-ingress-cluster
kind load docker-image sirrupesh/flask:latest --name sir-multi-node-ingress-cluster
kind load docker-image sirrupesh/nginx:latest --name sir-multi-node-ingress-cluster
```

3. **Deploy Services**
```bash
# Base configuration
kubectl apply -k k8s/base/

# Environment-specific (optional)
kubectl apply -k k8s/overlays/dev/   # Development
kubectl apply -k k8s/overlays/prod/  # Production
```

## Monitoring

### Resource Status
```bash
# View all resources
kubectl get all,ingress -n sir-ns

# Check pod health
kubectl get pods -n sir-ns -o wide

# View logs
kubectl logs -l app=flask-app -n sir-ns  # Flask app
kubectl logs -l my-app=app4 -n sir-ns    # PHP app
```

### Health Checks
- Liveness probes: `/health/live`
- Readiness probes: `/health/ready`
- Metrics (Production): `/metrics`

## Configuration

### Development Environment
- Single replica per service
- Debug mode enabled
- Minimal resource limits
- Hot reload support

### Production Environment
- High availability (3 replicas)
- Resource optimization
- Security hardening
- Prometheus metrics
- Pod anti-affinity
- Rolling updates

## Project Structure
```
.
├── k8s/                 # Kubernetes manifests
│   ├── base/           # Base configurations
│   ├── overlays/       # Environment overlays
│   ├── configs/        # Cluster config
│   └── dashboard/      # K8s dashboard
└── src/                # Application source
    ├── app/           # Flask service
    ├── app4/          # PHP service
    └── nginx/         # Static server
```

## Troubleshooting

### Common Issues

1. **Service Unavailable**
   ```bash
   # Check ingress status
   kubectl get ingress -n sir-ns
   kubectl describe ingress multi-app-ingress -n sir-ns
   ```

2. **Pod Startup Failure**
   ```bash
   # View pod details
   kubectl describe pod <pod-name> -n sir-ns
   ```

3. **Image Issues**
   ```bash
   # Verify images in cluster
   docker exec -it kind-control-plane crictl images
   ```

### Logs
```bash
# Container logs
kubectl logs -l my-app=flask-backend -n sir-ns
kubectl logs -l my-app=php-backend -n sir-ns
```

## Cleanup

### Full Cleanup
```bash
kind delete cluster --name sir-multi-node-ingress-cluster
```

### Partial Cleanup
```bash
kubectl delete -k k8s/base/          # Remove services
kubectl delete namespace sir-ns      # Remove namespace
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Security Notes
- Development setup uses insecure defaults
- Production overlay includes:
  - Non-root user execution
  - Resource limits
  - Network policies
  - Secure probes
  - RBAC configuration
