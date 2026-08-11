# Kubernetes Capstone Project
 
Production-grade Kubernetes setup with dev and production
namespaces, autoscaling, resource quotas, and Ingress.
 
## Architecture
Two isolated namespaces on one cluster:
- dev: 1 Flask replica, 512Mi storage, strict quotas
- production: 3 Flask replicas + HPA (3-10), 2Gi storage,
  Ingress for clean URLs
 
## Prerequisites
- Minikube running
- kubectl installed
- nginx Ingress addon enabled: minikube addons enable ingress
 
## Deploy Everything
    ./deploy.sh
 
## Access
- Dev:        http://MINIKUBE_IP:30081
- Production: http://MINIKUBE_IP:30080
- Production: http://flask.local (add to /etc/hosts)
 
## Key Features
- Namespace isolation: dev mistakes cannot affect production
- HPA: production auto-scales 3-10 pods on CPU > 50%
- ResourceQuota: dev capped at 2 CPU, production at 8 CPU
- PVC: database data persists across pod restarts
- Ingress: clean /api/* routing in production
- Separate secrets per environment: dev and prod
  never share credentials
 
## Useful Commands
    # see all resources per namespace
    kubectl get all -n dev
    kubectl get all -n production
 
    # watch autoscaling
    kubectl get hpa -n production -w
 
    # check quota usage
    kubectl describe resourcequota -n production
 
    # delete dev safely
    kubectl delete all --all -n dev
 
    # full teardown
    kubectl delete namespace dev production