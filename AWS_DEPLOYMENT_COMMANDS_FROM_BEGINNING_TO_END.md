# Secure Multi-Layer Proxy Architecture -- Command Reference

This document collects the commands that were explicitly used or
discussed during the AWS deployment and the later GitHub documentation
workflow.

> **Accuracy note:** Commands marked **Used** were recorded in the
> project conversation. Commands marked **Suggested / not confirmed**
> were discussed as possible next steps but were not confirmed as
> executed. Some installation/download commands and the exact SSH
> command could not be recovered, so they are not guessed here.

------------------------------------------------------------------------

## 1. Connect to the EC2 instance

The project was operated on an Amazon Linux 2023 EC2 instance using SSH
from Windows.

The exact `ssh` command and key-file path used to connect could not be
recovered from the available conversation history.

The EC2 project directory was:

``` bash
cd /home/ec2-user/Secure-Multi-Layer-Proxy-Architecture
```

## 2. Update Amazon Linux and install Docker

**Used on EC2:**

``` bash
sudo dnf update -y
sudo dnf install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl status docker
docker --version
sudo docker run hello-world
sudo systemctl is-active docker
```

These commands update the operating system, install Docker, start and
enable the Docker service, check its status/version, and run Docker's
test container.

## 3. Install Docker Compose

**Used / attempted on EC2:**

``` bash
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
docker compose version
sudo dnf install docker-compose-plugin -y
```

The `dnf install docker-compose-plugin` attempt was unsuccessful. Docker
Compose V2 was instead installed manually as a Docker CLI plugin.

The exact `curl` or download command used to obtain the Compose binary
could not be recovered and is intentionally not reconstructed.

## 4. Check architecture and install Git

**Used on EC2:**

``` bash
uname -m
sudo dnf install git -y
git --version
```

## 5. Clone the GitHub repository on EC2

**Used on EC2:**

``` bash
git clone https://github.com/Shirisha356/Secure-Multi-Layer-Proxy-Architecture.git
cd Secure-Multi-Layer-Proxy-Architecture
ls -la
```

Validate the Docker Compose configuration:

``` bash
docker compose config --quiet
```

## 6. Build and start application containers

The AWS deployment used the `t3.micro` EC2 instance. The following
service startup commands were recorded.

**Users service -- used:**

``` bash
docker compose up -d --build users
docker compose ps
docker stats --no-stream
```

**HAProxy -- used:**

``` bash
docker compose up -d haproxy
docker compose ps
docker stats --no-stream
```

**Nginx -- used:**

``` bash
docker compose up -d nginx
docker compose ps
docker stats --no-stream
```

**Kong API Gateway -- used:**

``` bash
docker compose up -d kong
docker compose ps
docker stats --no-stream
free -h
```

The deployment scope on AWS was HAProxy, Nginx, Kong, Users, Orders, and
Payments. Squid, proxy-test, cAdvisor, Prometheus, and Grafana were not
started on the `t3.micro` instance.

## 7. Inspect Kong logs and test the APIs

**Used on EC2:**

``` bash
docker compose logs --tail=30 kong
```

Test the three API routes locally on the EC2 instance:

``` bash
curl -i http://localhost:8080/api/users
curl -i http://localhost:8080/api/orders
curl -i http://localhost:8080/api/payments
```

All three routes returned HTTP 200 during the recorded successful
validation.

The external browser URL format used was:

``` text
http://YOUR-EC2-PUBLIC-IP:8080/api/users
```

The corresponding `/api/orders` and `/api/payments` routes were also
checked through the EC2 public address and returned HTTP 200. The exact
external `curl` command was not recoverable.

The EC2 public IPv4 address was dynamic. Do not assume an old public IP
will remain valid after stop/start or termination.

## 8. Failure test for the Users service

**Used on EC2:**

``` bash
docker compose stop users
```

After stopping the Users service, a browser request to the Users API
produced an error, demonstrating the effect of the backend service being
unavailable.

The following command was discussed as the recovery command, but
successful execution and recovery were **not confirmed**:

``` bash
docker compose start users
```

A successful recovery result must therefore not be claimed in project
documentation.

## 9. Other Docker Compose commands discussed

The following commands appeared in the troubleshooting / wrap-up
discussion:

``` bash
docker compose ps
docker compose down
```

`docker compose ps` was used during the deployment checks.
`docker compose down` was suggested during wrap-up, but its execution
was not confirmed.

To return to the project folder on EC2:

``` bash
cd /home/ec2-user/Secure-Multi-Layer-Proxy-Architecture
```

## 10. Windows PowerShell -- clone the repository after EC2 termination

After the EC2 instance was terminated, the repository was cloned onto
the Windows computer so the documentation could be added and pushed
without using EC2.

**Used on Windows PowerShell:**

``` powershell
cd $HOME\Documents
git clone https://github.com/Shirisha356/Secure-Multi-Layer-Proxy-Architecture.git
cd Secure-Multi-Layer-Proxy-Architecture
git status
```

The working tree was reported as clean after cloning.

## 11. Windows PowerShell -- create the documentation branch

**Used on Windows PowerShell:**

``` powershell
git switch -c docs/aws-deployment
git branch
```

The branch list showed:

``` text
docs/aws-deployment
main
```

The current working branch was `docs/aws-deployment`; `main` was
retained.

## 12. Windows PowerShell -- create and open the documentation folder

**Used on Windows PowerShell:**

``` powershell
New-Item -ItemType Directory -Force -Path "docs\aws-deployment"
code .
```

The following documentation files were then created in VS Code:

``` text
docs/
└── aws-deployment/
    ├── AWS_DEPLOYMENT_GUIDE.md
    ├── AWS_ARCHITECTURE.md
    ├── AWS_TEST_RESULTS.md
    └── AWS_CLEANUP.md
```

The root `README.md` was also updated with an AWS Deployment section and
links to these files.

## 13. Git commands to check, commit, and push the documentation

The status check was requested after the files were created:

``` powershell
git status
```

The output of this final status check and the commit/push steps were not
yet provided in the conversation.

**Next commands to run when ready (these are pending steps, not commands
confirmed as already executed):**

``` powershell
git status
git add README.md docs/aws-deployment/
git diff --cached
git commit -m "Add AWS deployment documentation"
git push -u origin docs/aws-deployment
```

After pushing, open the repository on GitHub and create a Pull Request
from `docs/aws-deployment` into `main`.

Do not run `git push` until the commit succeeds. Review
`git diff --cached` before committing.

## 14. AWS Console actions (not shell commands)

The AWS infrastructure was configured through the AWS Management
Console. The resources and settings recorded were:

-   Region: Mumbai -- `ap-south-1`
-   VPC: `secure-proxy-vpc` -- `10.0.0.0/16`
-   Public subnet: `secure-proxy-public-subnet` -- `10.0.1.0/24`
-   Private subnet: `secure-proxy-private-subnet` -- `10.0.2.0/24`
-   Internet Gateway: `secure-proxy-igw`
-   Public route table: `secure-proxy-public-rt`
-   Private route table: `secure-proxy-private-rt`
-   EC2 instance: `secure-proxy-server` -- Amazon Linux 2023, `t3.micro`
-   Security group: `secure-proxy-ec2-sg`
-   Inbound access: SSH TCP 22 from My IP; application TCP 8080 from My
    IP
-   NAT Gateway: not created

The application EC2 instance was in the public subnet. The private
subnet was reserved for future workloads and did not host the deployed
application containers.

The EC2 instance was later terminated by the user. This document does
not assert that every associated AWS resource (for example, EBS volumes,
snapshots, security groups, or networking resources) was also deleted.
Check the AWS Console and Billing separately.

------------------------------------------------------------------------

## 15. Important security reminders

-   Never commit `secure-proxy-key.pem` or any private key to GitHub.
-   Do not commit AWS access keys, passwords, tokens, or `.env` secrets.
-   Keep SSH access restricted to trusted IP addresses.
-   Review the staged files with `git diff --cached` before committing.
-   The AWS deployment used one EC2 instance and was a learning
    deployment, not a production high-availability architecture.

## 16. Command history limitations

This reference includes commands recoverable from the project
conversation. It does not invent missing commands. In particular, the
exact SSH connection command, manual Docker Compose download command,
and some AWS Console click-by-click actions were not available in the
conversation history.
