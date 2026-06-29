# CloudFormation

## Purpose

This folder contains sample Infrastructure as Code (IaC) templates used to provision and manage AWS Glue resources required for the data ingestion pipeline.

---

## Files

### service.yml

Defines AWS infrastructure components required for the ETL pipeline.

Typical resources include:

- AWS Glue Jobs
- Glue Workflows
- Glue Triggers
- IAM Roles
- CloudWatch Integration
- EventBridge Scheduling

---

### sample.json

Provides deployment parameters consumed during CloudFormation stack deployment.

Typical parameters include:

- Environment
- Job Name
- IAM Role
- Script Location
- Connection Details
- Worker Configuration

---

## Deployment Flow

```text
GitHub Actions
        │
        ▼
Read Parameter File
(sample.json)
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
- Amazon S3
- AWS IAM
- Amazon CloudWatch
- Amazon EventBridge

---

## Confidentiality Notice

The templates included in this repository have been simplified and anonymized for portfolio purposes. All resource names, account identifiers, connection details, and deployment parameters have been replaced with generic placeholders while preserving the Infrastructure as Code implementation approach.
