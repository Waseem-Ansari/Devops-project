# Terraform: AWS VPC with CI/CD

Provisions an AWS network and a web server with Terraform, planned and
applied through GitHub Actions.

## What it creates
- VPC (10.0.0.0/16)
- Public subnet (route to internet gateway) and private subnet (no internet route)
- Internet gateway, public route table and association
- Security group (SSH from one IP, app port 8080)
- EC2 (Ubuntu 22.04) with Docker installed through user data

## Pipeline
- Pull request: terraform fmt, validate, plan
- Merge to main: plan, then manual approval, then apply
- Manual workflow: destroy

## State
Remote state in S3 (versioned, encrypted) with DynamoDB locking.

## Not included (known limitations)
- No NAT gateway (cost); private subnet has no outbound internet
- Pipeline uses an IAM user with access keys; GitHub OIDC with a
  scoped role would be better
- Single availability zone

## Run locally
    cd devops-project-terraform
    terraform init
    terraform plan -var key_name=YOUR_KEY -var ssh_cidr=YOUR_IP/32

## Lessons learned
- A subnet is public because of its route table, not its name
- References between resources build the dependency order automatically
- Reading the plan before apply catches destructive changes
- tfvars and state never go in Git
