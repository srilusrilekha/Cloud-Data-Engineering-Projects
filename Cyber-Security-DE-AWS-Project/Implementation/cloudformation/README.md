# CloudFormation

## Purpose

This folder contains sample Infrastructure as Code (IaC) templates demonstrating how AWS resources required for the data engineering pipeline can be provisioned and managed using AWS CloudFormation.

The templates have been simplified and anonymized to illustrate the deployment approach while protecting confidential implementation details.

---

## Files

### service.yml

Defines AWS infrastructure components required for the ETL pipeline.

Typical resources include:

- AWS Glue Job
- Secret Manager Secrets
- IAM Role
- Job Configuration
- Runtime Parameters
- Logging Configuration

---

### deployment_parameters.json

Provides environment-specific deployment parameters consumed by the CloudFormation template during deployment.

Sample Parameters

Environment
Glue Job Name
IAM Role
Script Location
Source Secret
Redshift Secret
Target Schema
Target Table
Worker Configuration

---

## Deployment Flow

```text
GitHub Actions
        │
        ▼
Read Parameter File
(deployment_parameters.json)
        │
        ▼
Deploy Infrastructure
(service.yml)
        │
        ▼
Provision AWS Resources
        │
        ▼
Ready for Glue Job Execution
```

---

## Technologies Used

- AWS CloudFormation
- AWS Glue
- AWS IAM
- AWS Secrets Manager
- Amazon S3
- Amazon Redshift

---

## Business Value
Enables Infrastructure as Code (IaC) for consistent deployments.
Standardizes AWS resource provisioning across environments.
Supports repeatable and automated deployments through CI/CD.
Reduces manual configuration effort and deployment errors.
Simplifies maintenance and future enhancements.

---

## Confidentiality Notice

The templates included in this repository are representative examples created for portfolio purposes. Resource names, account information, infrastructure details, and deployment parameters have been generalized or replaced with placeholders to protect confidential business information while demonstrating the overall deployment strategy.
