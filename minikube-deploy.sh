#!/bin/bash

set -e  # Exit on any error

echo "===== URL Shortener Minikube Deployment ====="

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

echo "Step 4: Creating Kubernetes resources..."
# Use indianexpress.com as the domain
DOMAIN_NAME="indianexpress.com"
echo "Using domain: ${DOMAIN_NAME}"

cat <<EOF > deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: url-shortener
spec:
  replicas: 1
  selector:
    matchLabels:
      app: url-shortener
  template:
    metadata:
      labels:
        app: url-shortener
    spec:
      containers:
      - name: url-shortener
        image: url-shortener:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 5000
        env:
        - name: REDIS_HOST
          value: redis-service
        - name: DOMAIN_NAME
          value: "${DOMAIN_NAME}"
---
apiVersion: v1
kind: Service
metadata:
  name: url-shortener-service
spec:
  selector:
    app: url-shortener
  ports:
  - port: 80
    targetPort: 5000
  type: NodePort
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:alpine
        ports:
        - containerPort: 6379
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
EOF

kubectl apply -f deployment.yaml

echo "Step 5: Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=url-shortener --timeout=60s
kubectl wait --for=condition=ready pod -l app=redis --timeout=60s

echo "Step 6: Getting access information..."
echo "To access your application, run the following command in a separate terminal:"
echo 
echo "minikube service url-shortener-service"
echo
echo "This will display the service information table and open the application in your browser."

echo
echo "===== Deployment Complete ====="
echo "To clean up later, run: ./minikube-cleanup.sh"
