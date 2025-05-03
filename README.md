# Multi-Node Kubernetes Cluster with Kind, Flask, and Nginx

A comprehensive demo project showcasing a local Kubernetes development environment using Kind (Kubernetes in Docker), featuring a Flask application, Nginx service, and ingress configurations. This setup demonstrates best practices for local Kubernetes development and deployment.

## 📁 Project Structure

```
.
├── src/
│   ├── app/              # Main Flask application
│   └── app4/             # PHP application
├── k8s/
│   ├── base/            # Base Kubernetes configurations
│   │   ├── app/        # Flask application manifests
│   │   ├── app4/       # PHP application manifests
│   │   ├── nginx/      # Nginx service configurations
│   │   └── ingress/    # Ingress controller setup
│   ├── configs/        # Kind cluster configurations
│   ├── dashboard/      # Kubernetes dashboard resources
│   └── overlays/       # Environment-specific configurations (dev/prod)
```

## 🛠 Prerequisites

The following tools must be installed on your machine before getting started:

- Docker - Container runtime
- Kind - Tool for running Kubernetes clusters in Docker
- kubectl - Kubernetes command-line tool
- kubens - Kubernetes namespace switching utility
- Helm - Package manager for Kubernetes (required for dashboard)
- Kustomize - Kubernetes configuration management (included with kubectl v1.14+)

## 🚀 Getting Started

### 1. Cluster Setup
```bash
# Create a new Kind cluster with ingress configuration
kind create cluster --config k8s/configs/kind-ingress-config

# Install the Nginx Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml

# Wait for the ingress controller to be ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s
```

### 2. Dashboard Setup
```bash
# Install Kubernetes dashboard using Helm
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard \
  --create-namespace --namespace kubernetes-dashboard

# Create dashboard admin user
kubectl apply -f k8s/dashboard/dashboard-adminuser.yaml

# Get admin user token
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath="{.data.token}" | base64 -d

# Access dashboard (will be available at https://localhost:8443)
kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
```

### 3. Application Deployment
```bash
# Create and switch to application namespace
kubectl create ns sir-ns
kubens sir-ns

# Build application Docker images
docker build -t sirrupesh/sample:v2 src/app/
docker build -t sirrupesh/app4:latest src/app4/

# Load images into Kind cluster
kind load docker-image sirrupesh/sample:v2 --name sir-multi-node-ingress-cluster
kind load docker-image sirrupesh/app4:latest --name sir-multi-node-ingress-cluster

# Create OpenAI secret (replace with your actual API key)
kubectl create secret generic openai-secret --from-literal=api-key="your-api-key"

# Deploy applications using Kustomize
kubectl apply -k k8s/base/
```

## 🔍 Monitoring and Debugging

```bash
# View all resources in the namespace
kubectl get all,ingress -n sir-ns

# Check deployment status
kubectl describe deployments -n sir-ns

# View application logs
kubectl logs -n sir-ns -l my-app=llm-app
kubectl logs -n sir-ns -l my-app=nginx

# Check ingress configuration
kubectl describe ingress -n sir-ns
```

## 🧹 Cleanup

```bash
# Delete the Kind cluster
kind delete cluster --name sir-multi-node-ingress-cluster
```

## 📝 Notes
- The cluster uses a multi-node setup for better production similarity
- Ingress is configured for local development
- Dashboard access requires token authentication
- Environment-specific configurations are managed through Kustomize overlays