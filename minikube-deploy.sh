#!/bin/bash

set -e  # Exit on any error

echo "===== URL Shortener Minikube Deployment with Scaling & Monitoring ====="

echo "Step 1: Checking Minikube status..."
if ! command -v minikube &> /dev/null; then
    echo "Error: Minikube not found. Please install Minikube first."
    exit 1
fi

if ! minikube status | grep -q "Running"; then
    echo "Starting Minikube..."
    minikube start
else
    echo "Minikube is already running."
fi

echo "Step 2: Configuring Docker to use Minikube's Docker daemon..."
eval $(minikube docker-env)

echo "Step 3: Building Docker image inside Minikube..."
docker build -t url-shortener:latest .
echo "Image built successfully."

echo "Step 4: Enabling metrics-server for autoscaling..."
minikube addons enable metrics-server

echo "Step 5: Applying Kubernetes YAMLs (config, Redis, URL shortener)..."
kubectl apply -f url-shortener-config.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f redis-secret.yaml
kubectl apply -f redis-service.yaml
kubectl apply -f url-shortener-deployment.yaml
kubectl apply -f url-shortener-service.yaml

echo "Step 6: Setting up Ingress controller..."
minikube addons enable ingress
kubectl apply -f ingress.yaml || echo "⚠️ No ingress.yaml file found or applied"

echo "Step 7: Creating or updating Horizontal Pod Autoscaler..."
kubectl delete hpa url-shortener --ignore-not-found
kubectl autoscale deployment url-shortener --cpu-percent=50 --min=1 --max=5

echo "Step 8: Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=url-shortener --timeout=60s || true
kubectl wait --for=condition=ready pod -l app=redis --timeout=60s || true

echo "Step 9: Displaying runtime stats..."

echo
echo "🟢 Current Pods:"
kubectl get pods -o wide

echo
echo "📊 HPA Status:"
kubectl get hpa

echo
echo "🧠 Resource Usage (via metrics-server):"
kubectl top pods || echo "⚠️ 'kubectl top pods' needs more time or may not be supported"

echo
echo "🌐 LoadBalancer or NodePort Service:"
minikube service url-shortener-service --url

echo
echo "📋 Ingress routes:"
kubectl get ingress

echo
echo "===== Deployment with Scaling, Load Balancing & Monitoring Complete ====="
echo "To clean up later, run: ./minikube-cleanup.sh"
