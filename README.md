# Multi-Service Kubernetes Demo Project

A production-grade demonstration of running multiple microservices in a high-availability Kubernetes cluster using Kind, featuring advanced configurations like ingress routing, health monitoring, and metrics collection.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Development Guide](#development-guide)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)
- [Cleanup](#cleanup)
- [Service URLs](#service-urls)

## Overview

This project demonstrates enterprise-level Kubernetes practices including:
- High-availability cluster setup with multiple control planes
- Microservices architecture with Flask, Nginx, and PHP services
- Advanced ingress configuration with SSL support
- Health monitoring and metrics collection
- Environment-specific deployments using Kustomize
- Local development workflow with Kind

## Architecture

### Cluster Configuration
- Multi-node setup with 2 control planes for high availability
- 3 worker nodes for workload distribution
- Ingress controller for external access
- Node labels for specialized workload placement

### Services
1. **Flask Application**
   - Visit tracking with session management
   - Health monitoring endpoints
   - Optional Prometheus metrics
   - Pod diagnostics capabilities

2. **Nginx Frontend**
   - Static content serving
   - Reverse proxy configuration
   - SSL termination

3. **PHP Application**
   - System diagnostics
   - Apache-based setup

## Prerequisites

Required tools:
- Docker Desktop 4.x or newer
- Kind v0.20 or newer
- kubectl v1.27 or newer
- kubens
- Helm v3.x (for dashboard)
- Kustomize (included with recent kubectl)

## Project Structure

```
.
├── src/                  # Application source code
│   ├── app/             # Flask application
│   │   ├── app.py       # Main application code
│   │   └── Dockerfile   # Flask container configuration
│   ├── nginx/           # Nginx frontend
│   │   ├── src/        # Static content
│   │   └── Dockerfile   # Nginx container configuration
│   └── app4/           # PHP application
│       ├── src/        # PHP source files
│       └── Dockerfile   # PHP-Apache configuration
├── k8s/                 # Kubernetes configurations
    ├── base/           # Base Kubernetes manifests
    ├── configs/        # Cluster configurations
    ├── dashboard/      # Kubernetes dashboard
    └── overlays/       # Environment overlays
```

## Setup Instructions

### 1. Cluster Creation
```bash
# Create high-availability cluster
kind create cluster --config k8s/configs/kind-ingress-config

# Verify cluster status
kubectl cluster-info
kubectl get nodes
```

### 2. Environment Setup
```bash
# Create namespace
kubectl create ns sir-ns
kubens sir-ns

# Install ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml

# Wait for ingress controller
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

### 3. Building and Loading Images
```bash
# Build all images
docker build -t sirrupesh/myflask:latest src/app/
docker build -t sirrupesh/mynginx:latest src/nginx/
docker build -t sirrupesh/myphp:latest src/app4/

# Load images into Kind
kind load docker-image sirrupesh/myflask:latest
kind load docker-image sirrupesh/mynginx:latest
kind load docker-image sirrupesh/myphp:latest
```

### 4. Application Deployment
```bash
# Configure secrets
kubectl create secret generic openai-secret --from-literal=api-key="your-api-key"

# Deploy applications
kubectl apply -k k8s/base/  # For base environment
# kubectl apply -k k8s/overlays/dev/   # For development
# kubectl apply -k k8s/overlays/prod/  # For production
```

### 5. Verify Deployment
```bash
# Check all resources
kubectl get all,ingress -n sir-ns

# Verify pod health
kubectl get pods -n sir-ns -o wide

# Check application logs
kubectl logs -l app=flask-app -n sir-ns
```

## Development Guide

### Local Development
1. **Environment Setup**
   ```bash
   # Start local development cluster
   kind create cluster --config k8s/configs/kind-ingress-config
   ```

2. **Code Changes**
   - Flask app: Edit src/app/app.py
   - Nginx: Modify files in src/nginx/src/
   - PHP: Update files in src/app4/src/

3. **Testing Changes**
   ```bash
   # Rebuild and load updated images
   docker build -t sirrupesh/myflask:latest src/app/
   kind load docker-image sirrupesh/myflask:latest
   
   # Restart deployment
   kubectl rollout restart deployment flask-app-deployment -n sir-ns
   ```

### Health Monitoring
Access health endpoints:
- Flask: http://sirrupesh.localhost/health/live
- Metrics: http://sirrupesh.localhost/metrics (if enabled)
- PHP: http://php.localhost/health.php

## Monitoring & Maintenance

### Health Checks
- Monitor liveness: `kubectl get pods -n sir-ns`
- Check readiness: `kubectl describe pods -n sir-ns`
- View metrics: Enable Prometheus metrics in Flask app

### Regular Maintenance
1. Update dependencies regularly
2. Monitor resource usage
3. Review logs for issues
4. Test failover scenarios
5. Verify ingress configurations

## Troubleshooting

Common issues and solutions:
1. **Pods not starting**
   ```bash
   kubectl describe pod <pod-name> -n sir-ns
   kubectl logs <pod-name> -n sir-ns
   ```

2. **Ingress issues**
   ```bash
   kubectl describe ingress -n sir-ns
   kubectl get events -n sir-ns
   ```

3. **Image pull errors**
   - Verify image names and tags
   - Check imagePullPolicy
   - Ensure images are loaded in Kind

## Cleanup

Remove cluster and resources:
```bash
kind delete cluster --name sir-multi-node-ingress-cluster
```

## Service URLs

The following services are accessible through ingress routing:

| Service | URL | Description |
|---------|-----|-------------|
| Flask Counter App | http://sirrupesh.localhost | Visit tracking application with health monitoring |
| Nginx Frontend | http://cambridge.localhost | Static content serving |
| PHP System Info | http://app4.localhost | System diagnostics interface |

### Local DNS Setup
To access these services, ensure your system can resolve `.localhost` domains. The following hosts are configured:
```
127.0.0.1 sirrupesh.localhost
127.0.0.1 cambridge.localhost
127.0.0.1 app4.localhost
```

### Available Endpoints

1. **Flask Application** (http://sirrupesh.localhost)
   - `/` - Visit counter
   - `/hostname` - Pod hostname information
   - `/health/live` - Liveness probe endpoint
   - `/health/ready` - Readiness probe endpoint
   - `/metrics` - Prometheus metrics (if enabled)

2. **Nginx Frontend** (http://cambridge.localhost)
   - `/` - Static content

3. **PHP System Info** (http://app4.localhost)
   - `/` - System information dashboard