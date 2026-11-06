# AWS Deployment Guide – Secure Multi-Layer Proxy Architecture

## 1. Project Overview

This project demonstrates a multi-layer proxy architecture deployed on AWS using Docker Compose.

The AWS deployment runs the application services on an Amazon EC2 instance. Traffic passes through multiple proxy and gateway layers before reaching backend microservices.

**Deployment region:** Asia Pacific (Mumbai) – `ap-south-1`

## 2. AWS Services Used

| AWS Service | Purpose |
|---|---|
| Amazon VPC | Isolated virtual network |
| Public Subnet | Hosts the EC2 instance |
| Private Subnet | Reserved for future workloads |
| Internet Gateway | Provides internet connectivity to the public subnet |
| Route Tables | Control network traffic routing |
| Amazon EC2 | Hosts Docker containers |
| Security Group | Controls inbound network access |
| Amazon EBS | Provides EC2 storage |

## 3. VPC and Network Configuration

VPC name: `secure-proxy-vpc`

CIDR block: `10.0.0.0/16`

### Public Subnet

- Name: `secure-proxy-public-subnet`
- CIDR: `10.0.1.0/24`
- Availability Zone: `ap-south-1a`
- Auto-assign public IPv4: Enabled

### Private Subnet

- Name: `secure-proxy-private-subnet`
- CIDR: `10.0.2.0/24`
- Availability Zone: `ap-south-1b` (or the selected available AZ)
- Auto-assign public IPv4: Disabled

### Internet Gateway

- Name: `secure-proxy-igw`
- Attached to the VPC.
- Public route table has a default route to the Internet Gateway.

### Route Tables

**Public route table:** `secure-proxy-public-rt`

- Associated with the public subnet.
- Default route: `0.0.0.0/0` → Internet Gateway.

**Private route table:** `secure-proxy-private-rt`

- Associated with the private subnet.
- No default internet route was configured.

**NAT Gateway:** Not created, to avoid additional charges.

## 4. Amazon EC2 Configuration

| Parameter | Configuration |
|---|---|
| Instance name | `secure-proxy-server` |
| Operating system | Amazon Linux 2023 |
| Instance type | `t3.micro` |
| vCPU | 2 |
| Memory | 1 GiB |
| Region | `ap-south-1` |
| Deployment location | Public subnet |
| Key pair | `secure-proxy-key.pem` |

The private subnet was created for future use. The application containers were hosted on one EC2 instance in the public subnet.

## 5. Security Group Configuration

Security group: `secure-proxy-ec2-sg`

Inbound rules:

| Protocol | Port | Source | Purpose |
|---|---:|---|---|
| TCP | 22 | My IP | SSH administration |
| TCP | 8080 | My IP | Application access |

The application was not configured to expose backend service ports directly to the internet.

**Security note:** Restrict SSH and application access to trusted IP addresses. Never commit private keys, credentials, or `.pem` files to GitHub.

## 6. EC2 Software Installation

The following tools were installed on the Amazon Linux 2023 instance:

- Docker Engine – 25.0.18
- Docker Compose V2
- Docker Buildx – 0.17.1
- Git

The `ec2-user` account was configured to use Docker.

Docker Compose and Buildx were installed and verified before deploying the application.

## 7. Application Deployment

The GitHub repository was cloned into:

`/home/ec2-user/Secure-Multi-Layer-Proxy-Architecture`

The Docker Compose project contains the following services:

### Application services

- HAProxy
- Nginx
- Kong API Gateway
- Users service
- Orders service
- Payments service

### Other services in the complete Compose project

- Squid proxy
- Proxy test
- cAdvisor
- Prometheus
- Grafana

**AWS deployment scope:** Due to the limited memory of the `t3.micro` instance, only HAProxy, Nginx, Kong, Users, Orders, and Payments were started on AWS. Squid, proxy-test, cAdvisor, Prometheus, and Grafana were not started on the EC2 instance.

### Application request flow

External client → HAProxy → Nginx → Kong API Gateway → Backend microservice.

## 8. Application Access and Validation

The application was accessed through the EC2 public IPv4 address on TCP port 8080.

The following endpoints returned HTTP 200:

| Endpoint | Result |
|---|---|
| `/api/users` | HTTP 200 |
| `/api/orders` | HTTP 200 |
| `/api/payments` | HTTP 200 |

The same three endpoints were tested through the EC2 public address.

The public IP was dynamically assigned. It should not be treated as permanent because no Elastic IP was confirmed.

## 9. Resource and Performance Considerations

The `t3.micro` instance has limited memory (1 GiB).

After starting the application services, memory availability was limited. Docker container memory usage was approximately 240 MiB at the time of observation.

Monitoring services were therefore postponed on AWS to avoid overloading the instance.

For a production deployment, consider a larger EC2 instance, private worker workloads, appropriate monitoring, and a more robust deployment architecture.

## 10. Deployment Limitations

- All running application containers were hosted on a single EC2 instance.
- The private subnet was not hosting application workloads.
- No NAT Gateway was created.
- AWS monitoring containers were not deployed.
- No Elastic IP was confirmed.
- The Users service failure test was performed, but its recovery test was not completed.
- This was a learning deployment, not a production-ready high-availability setup.

## 11. Security and Cost Awareness

- Do not expose internal backend ports publicly.
- Restrict SSH access to your own IP.
- Never push `.pem` files or credentials to GitHub.
- Avoid unnecessary NAT Gateway and other billable resources.
- Terminate unused EC2 instances and verify associated EBS volumes and other resources.

---

**Project:** Secure Multi-Layer Proxy Architecture  
**Platform:** AWS  
**Region:** ap-south-1  
**Deployment method:** Docker Compose on Amazon EC2