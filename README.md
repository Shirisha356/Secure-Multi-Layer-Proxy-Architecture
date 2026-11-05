# Secure Multi-Layer Proxy Architecture

## Project Objective
Build a secure proxy architecture using Docker.

## Components
1. Squid Forward Proxy
2. HAProxy Load Balancer
3. Nginx Reverse Proxy
4. Kong API Gateway
5. User Service
6. Order Service
7. Payment Service

## Security Objectives
- Restrict direct internet access for internal users.
- Protect backend services.
- Implement network isolation.
- Enable logging at every layer.
- Test failure scenarios.

## Deployment
Docker Compose on Windows.