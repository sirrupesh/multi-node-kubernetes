kind create cluster --config kind-ingress-config
kubectl create ns sir-ns
kubens sir-ns
kubectl get all -n sir-ns

-------
kubectl apply \
    --filename https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml

-------
https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/

helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard

kubectl apply -f dashboard-adminuser.yaml

# kubectl -n kubernetes-dashboard create token admin-user
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath="{.data.token}" | base64 -d

kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443

----
docker build -t sirrupesh/sample:v2 my-app/

kubectl create secret generic openai-secret --from-literal=api-key="123456"

kubectl apply -f project.yaml
kubectl apply -f ng-service.yaml
kubectl get all -n sir-ns

https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/

kubectl apply -f https://k8s.io/examples/application/deployment.yaml

kubectl apply -f ingress-resource.yaml

kind delete cluster --name sir-multi-node-ingress-cluster