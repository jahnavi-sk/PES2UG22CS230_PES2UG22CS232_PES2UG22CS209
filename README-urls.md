# URL Shortener - URL Structure Guide

This document explains the URL structure for the URL shortener application.

## Application Access URLs

Depending on how you run the application, you'll access it at different URLs:

1. **Local Development**:
   * URL: `http://localhost:5000`
   * Example: http://localhost:5000

2. **Docker**:
   * URL: `http://localhost:5000`
   * Example: http://localhost:5000

3. **Kubernetes/Minikube**:
   * URL via port-forwarding: `http://localhost:5000`
   * URL via Minikube service: (Varies, displayed when you run `minikube-deploy.sh`)
   * Example: http://192.168.49.2:31234 (actual port will be different)

## Shortened URL Format

When you create a shortened URL through the application:

1. **Default Configuration**:
   * Format: `http://{host}/{short-id}`
   * Example: `http://localhost:5000/a1b2c3`

2. **With Custom Domain** (when `DOMAIN_NAME` is set to "indianexpress.com"):
   * Format: `https://indianexpress.com/{short-id}`
   * Example: `https://indianexpress.com/a1b2c3`

## API Endpoints

The application provides the following API endpoints:

1. **Shorten URL**:
   * Endpoint: `/api/shorten`
   * Method: POST
   * Example: `http://localhost:5000/api/shorten`
   
2. **Redirect to Original URL**:
   * Endpoint: `/{short-id}`
   * Method: GET
   * Example: `http://localhost:5000/a1b2c3`
   
3. **Delete Shortened URL**:
   * Endpoint: `/api/delete/{short-id}`
   * Method: DELETE
   * Example: `http://localhost:5000/api/delete/a1b2c3`

## Notes on Custom Domains

If you've configured the application to use "indianexpress.com" as the domain:

1. For local development, you'll need to modify your hosts file to map this domain to localhost
2. In a production environment, you would need to own the domain and configure DNS properly
3. The actual redirection will happen through your local/deployment URL, not directly through indianexpress.com

For more details on configuration options, refer to the main README.md file.
