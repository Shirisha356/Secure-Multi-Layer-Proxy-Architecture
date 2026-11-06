# AWS Resource Cleanup Guide

## 1. Purpose

This guide explains how to clean up AWS resources created for the Secure Multi-Layer Proxy Architecture project to avoid unnecessary AWS charges.

**Important:** Terminating an EC2 instance does not automatically remove every associated AWS resource.

## 2. EC2 Instance

1. Open the AWS Management Console.
2. Navigate to EC2 → Instances.
3. Select `secure-proxy-server`.
4. Check its state.
5. If it is still running, choose Instance state → Terminate instance.

Termination is irreversible. Confirm that important data and project files are backed up before proceeding.

## 3. EBS Volumes

1. Navigate to EC2 → Volumes.
2. Check for volumes associated with the terminated instance.
3. Review whether any volumes remain available.
4. Delete only volumes that are no longer required.

## 4. Elastic IP Addresses

1. Navigate to EC2 → Elastic IPs.
2. Check whether any Elastic IP addresses are allocated.
3. Release unused Elastic IP addresses.

An Elastic IP was not confirmed as part of this deployment.

## 5. NAT Gateway

1. Navigate to VPC → NAT Gateways.
2. Check for any NAT Gateway created for the project.
3. Delete unused NAT Gateways if present.

No NAT Gateway was created during this deployment.

## 6. Network Resource Cleanup

After confirming that dependent resources are no longer required, clean up in this order:

1. Detach and delete the Internet Gateway `secure-proxy-igw`.
2. Delete the public and private route tables if they are no longer required.
3. Delete the public and private subnets.
4. Delete the security group `secure-proxy-ec2-sg`.
5. Delete the VPC `secure-proxy-vpc`.

AWS may prevent deletion while dependencies or network interfaces remain. Resolve those dependencies before retrying.

## 7. Final Cost Verification

Check the following AWS services:

- EC2 Instances
- EBS Volumes and Snapshots
- Elastic IP Addresses
- NAT Gateways
- Load Balancers
- CloudWatch resources
- Other resources created during the project

Review AWS Billing → Bills and Cost Explorer for any remaining charges.

## 8. Important Notes

- Do not delete resources belonging to other projects.
- Verify the AWS region is `ap-south-1`.
- Terminate unused instances.
- Check for unattached storage.
- Confirm that no billable networking resources remain.

