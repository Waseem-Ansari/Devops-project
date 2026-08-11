#!/bin/bash

# This script deploys the application to the production environment in Kubernetes.
# stops script execution if any command fails
set -e

echo "🚀 Deploying K8s Capstone Project..."

# step 1: create the production namespace
echo "📂 Creating production namespace..."
kubectl apply -f k8s/namespaces/

# step 2:Deploy dev environment
echo "🔧 Deploying DEV environment..."
kubectl apply -f k8s/dev/

# step 3: Deploy production environment
echo "🚀 Deploying PRODUCTION environment..."
kubectl apply -f k8s/production/

# step 4: wait for the pods to be ready
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=flask -n dev --timeout=120s
kubectl wait --for=condition=ready pod -l app=flask -n production --timeout=120s

# step 5: show status
echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "=== DEV Environment ==="
kubectl get all -n dev

echo ""
echo "=== PRODUCTION Environment ==="
kubectl get all -n production

echo ""
echo "=== ACCESS URLS ==="
echo "DEV:   http://$(minikube ip):30081"
echo "PRODUCTION:  http://$(minikube ip):30080"
echo "PRODUCTION:  https://flask.local (via ingress, make sure to add flask.local to your /etc/hosts file)"