# Kubernetes Demo Project

This project demonstrates a multi-node Kubernetes cluster setup using Kind, running a Flask application and Nginx service with ingress configurations.

## Project Structure

```
.
├── src/
│   └── app/              # Flask application
├── k8s/
│   ├── base/            # Base Kubernetes manifests
│   │   ├── app/        # Flask app manifests
│   │   ├── nginx/      # Nginx service manifests
│   │   └── ingress/    # Ingress configurations
│   ├── configs/        # Cluster configurations
│   ├── dashboard/      # Kubernetes dashboard setup
│   └── overlays/       # Environment-specific overlays
```

## Prerequisites

- Docker
- Kind
- kubectl
- kubens
- Helm (for dashboard)
- Kustomize (included with kubectl v1.14+)

## Getting Started

1. Create the Kind cluster:
   ```bash
   kind create cluster --config k8s/configs/kind-ingress-config
   ```

2. Create namespace and switch context:
   ```bash
   kubectl create ns sir-ns
   kubens sir-ns
   ```

3. Install Nginx Ingress Controller:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml
   ```

4. Build and deploy the application:
   ```bash
   # Build the Docker image
   docker build -t sirrupesh/sample:v2 src/app/

   # Create OpenAI secret
   kubectl create secret generic openai-secret --from-literal=api-key="your-api-key"

   # Deploy using Kustomize
   # For base configuration:
   kubectl apply -k k8s/base/

   # Or for specific environments:
   # Development:
   # kubectl apply -k k8s/overlays/dev/
   
   # Production:
   # kubectl apply -k k8s/overlays/prod/
   ```

5. Wait for all resources to be ready:
   ```bash
   # Wait for ingress controller to be ready
   kubectl wait --namespace ingress-nginx \
     --for=condition=ready pod \
     --selector=app.kubernetes.io/component=controller \
     --timeout=90s

   # Wait for application deployments to be ready
   kubectl wait --namespace sir-ns \
     --for=condition=ready pod \
     --selector=app=llm-app \
     --timeout=90s

   kubectl wait --namespace sir-ns \
     --for=condition=ready pod \
     --selector=app=nginx \
     --timeout=90s
   ```

6. Verify the deployment status:
   ```bash
   # Get all resources in the namespace
   kubectl get all,ingress -n sir-ns

   # Check detailed status of deployments
   kubectl describe deployments -n sir-ns

   # Check application logs
   kubectl logs -n sir-ns -l app=llm-app
   kubectl logs -n sir-ns -l app=nginx

   # Check ingress status
   kubectl describe ingress -n sir-ns
   ```

7. Access the applications:
   - Flask app: http://sirrupesh.localhost
   - Nginx service: http://cambridge.localhost

## Dashboard Setup

1. Install the dashboard:
   ```bash
   helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard \
     --create-namespace --namespace kubernetes-dashboard
   ```

2. Create dashboard admin user:
   ```bash
   kubectl apply -f k8s/dashboard/dashboard-adminuser.yaml
   ```

3. Get the token:
   ```bash
   kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath="{.data.token}" | base64 -d
   ```

4. Access dashboard:
   ```bash
   kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
   ```

## Cleanup

To delete the cluster:
```bash
kind delete cluster --name sir-multi-node-ingress-cluster
```