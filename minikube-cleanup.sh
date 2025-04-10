#!/bin/bash

echo "===== Cleaning up URL Shortener in Minikube ====="

echo "Deleting Kubernetes resources..."
kubectl delete -f deployment.yaml || echo "Resources already deleted or not found."

echo "Do you want to stop Minikube? (y/n)"
read -r stop_minikube

if [[ "$stop_minikube" =~ ^[Yy]$ ]]; then
    echo "Stopping Minikube..."
    minikube stop
    echo "Minikube stopped."
else
    echo "Minikube is still running."
fi

echo "===== How to Run Your Application ====="
echo "Choose the appropriate script based on your needs:"
echo ""
echo "1. For Docker setup (recommended for most users):"
echo "   ./run.sh docker-redis    # Start Redis"
echo "   ./run.sh docker          # Build and run the URL shortener"
echo ""
echo "2. For Minikube/Kubernetes setup:"
echo "   ./minikube-deploy.sh     # Deploy to Minikube"
echo ""
echo "3. For local development:"
echo "   ./run.sh local           # Run Flask app locally"
echo ""
echo "See README.md for more detailed instructions."

echo "Cleanup complete."
