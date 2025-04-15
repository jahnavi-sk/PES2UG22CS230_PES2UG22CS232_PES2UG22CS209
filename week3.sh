#!/bin/bash

echo "=== Week 3: Scaling, Load Balancing & Monitoring ==="

# Step 1: Enable metrics-server for HPA
echo "[Step 1] Enabling metrics-server..."
minikube addons enable metrics-server

# Step 2: Apply deployment and service files
echo "[Step 2] Applying Deployment and Service..."
kubectl apply -f url-shortener-config.yaml
kubectl apply -f url-shortener-deployment.yaml
kubectl apply -f url-shortener-service.yaml

# Step 3: Set up Horizontal Pod Autoscaler
echo "[Step 3] Creating Horizontal Pod Autoscaler..."
kubectl autoscale deployment url-shortener-deployment --cpu-percent=50 --min=1 --max=5

# Step 4: Enable ingress or load balancer (using LoadBalancer here)
echo "[Step 4] Starting Minikube tunnel for LoadBalancer..."
echo "Note: This terminal will be blocked; use another terminal if needed."
minikube tunnel

# Optional: Display pods and HPA status
# kubectl get pods
# kubectl get hpa
