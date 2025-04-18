kind create cluster --config kind-ingress-config
kubectl create ns sir-ns
kubens sir-ns
-------
kubectl apply \
    --filename https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/kind/deploy.yaml

-------
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard

kubectl apply -f dashboard-adminuser.yaml
----

kubectl create secret generic openai-secret --from-literal=api-key="123456"

kubectl apply -f project.yaml
kubectl apply -f ingress-resource.yaml