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
     --selector=my-app=llm-app \
     --timeout=90s

   kubectl wait --namespace sir-ns \
     --for=condition=ready pod \
     --selector=my-app=nginx \
     --timeout=90s
   ```

6. Verify the deployment status:
   ```bash
   # Get all resources in the namespace
   kubectl get all,ingress -n sir-ns

   # Check detailed status of deployments
   kubectl describe deployments -n sir-ns

   # Check application logs
   kubectl logs -n sir-ns -l my-app=llm-app
   kubectl logs -n sir-ns -l my-app=nginx

   # Check ingress status
   kubectl describe ingress -n sir-ns
   ```

7. Access the applications:
   - Flask app: http://sirrupesh.localhost
   - Nginx service: http://cambridge.localhost

## Working with Local Images

When developing locally, you can load Docker images directly into your Kind cluster without pushing them to a registry:

1. Build your local Docker image:
   ```bash
   # For app4
   cd src/app4 && docker build -t app4:latest .
   # For main app
   cd src/app && docker build -t app:latest .
   ```

2. Load the image into Kind cluster:
   ```bash
   # Load app4 image
   kind load docker-image app4:latest --name sir-multi-node-ingress-cluster
   # Load main app image
   kind load docker-image app:latest --name sir-multi-node-ingress-cluster
   ```

3. Make sure your Kubernetes manifests use the correct image name and pull policy:
   ```yaml
   spec:
     containers:
     - name: your-container
       image: app4:latest  # Use the same tag as built locally
       imagePullPolicy: Never  # Important for using local images
   ```

Note: The `imagePullPolicy: Never` setting ensures Kubernetes uses the local image instead of trying to pull from a registry.

## Cleanup

To delete the cluster:
```bash
kind delete cluster --name sir-multi-node-ingress-cluster
```