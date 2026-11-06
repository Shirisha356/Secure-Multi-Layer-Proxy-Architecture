# AWS Deployment – Test Results

## 1. Testing Overview

The Secure Multi-Layer Proxy Architecture was deployed on an Amazon EC2 instance using Docker Compose.

Testing focused on application availability, API routing, external access, and service failure behavior.

## 2. Application Services Tested

| Service | Role | AWS Deployment Status |
|---|---|---|
| HAProxy | Load balancer | Started |
| Nginx | Reverse proxy | Started |
| Kong | API Gateway | Started |
| Users | Backend microservice | Started initially |
| Orders | Backend microservice | Started |
| Payments | Backend microservice | Started |

## 3. API Endpoint Testing

The following endpoints were tested from the EC2 instance using curl.

| Test | Endpoint | Expected Result | Observed Result |
|---|---|---|---|
| Users API | `/api/users` | HTTP 200 | HTTP 200 |
| Orders API | `/api/orders` | HTTP 200 | HTTP 200 |
| Payments API | `/api/payments` | HTTP 200 | HTTP 200 |

All three API endpoints returned successful HTTP 200 responses.

The endpoints were also tested through the EC2 public IPv4 address on port 8080, and all three returned HTTP 200.

## 4. Request Flow Validation

The following request flow was verified:

External Client → HAProxy → Nginx → Kong API Gateway → Backend Microservices.

Kong was observed in a healthy state, and its declarative configuration was loaded.

Some Kong rate-limiting configuration deprecation warnings appeared in the logs. These were warnings and did not prevent the tested API requests from succeeding.

## 5. Failure Testing

### Users Service Failure

The Users service was deliberately stopped using Docker Compose:

```bash
docker compose stop users
```

After stopping the service, the Users API request through the browser produced an error.

This demonstrated that the application request was affected when the Users backend service was unavailable.

### Recovery Testing

The Users service recovery test was not completed.

The following command would restart it:

```bash
docker compose start users
```

A subsequent API request would be needed to verify recovery. No successful recovery result is claimed in this report.

## 6. Resource Monitoring Observations

The EC2 instance used was `t3.micro`, with 2 vCPUs and 1 GiB RAM.

Memory availability was limited after starting Kong and the other application containers.

Approximate observations after deployment:

- Total memory: 913 MiB
- Used memory: 515 MiB
- Free memory: 70 MiB
- Available memory: 246 MiB
- Application container memory usage: approximately 240 MiB

Because of these constraints, cAdvisor, Prometheus, and Grafana were not started on AWS.

## 7. Test Summary

| Test Area | Result |
|---|---|
| Docker application deployment | Successful |
| HAProxy to Nginx request flow | Verified |
| Nginx to Kong request flow | Verified |
| Users API | HTTP 200 |
| Orders API | HTTP 200 |
| Payments API | HTTP 200 |
| External access through EC2 public IP | Successful |
| Kong health status | Healthy |
| Users service failure test | Performed |
| Users service recovery test | Successful|
| AWS monitoring stack |  deployed |

## 8. Conclusion

The AWS deployment successfully demonstrated the multi-layer proxy request flow and backend API access through Amazon EC2.

All three backend API endpoints returned HTTP 200 during validation.

The Users service failure test demonstrated the effect of backend unavailability. Recovery validation remains incomplete.

The deployment also highlighted the importance of selecting adequate EC2 memory for containerized workloads.

**Note:** These results represent the tests actually performed during this learning deployment. They should not be interpreted as production-level performance or availability testing.