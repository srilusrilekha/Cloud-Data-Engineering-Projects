# AWS Glue ETL Jobs

This folder contains sample AWS Glue ETL jobs demonstrating the layered data engineering approach used to ingest, transform, and prepare data for enterprise reporting.

The scripts have been simplified and anonymized for portfolio purposes while preserving the overall ETL workflow and implementation approach.

---

# 1. Source to Raw Layer

File: 01_source_to_raw.py

## Purpose

Extracts data from enterprise source systems, performs basic validation and standardization, and loads the data into the Amazon Redshift Raw Layer.

## Workflow

            Glue Job Trigger    ---->   Read Runtime Parameters   ---->    Retrieve Credentials   ---->  Connect to Source Database
                                                                          (AWS Secrets Manager)
                                                                                                                   │
                                                                                                                   ▼
                                                                                                                                                                            Logging & Job Completion    <----    Load Data into    <----    Basic Validation &     <----    Extract Source Data
                                                Redshift Raw Layer        Column Standardization


# 2. Raw Layer to Integrated Layer

File: 02_raw_to_integrated.py

## Purpose

Transforms raw datasets into standardized business entities by executing Redshift stored procedures that apply business rules and data relationships.

## Workflow

             Glue Job Trigger    ---->   Read Runtime Parameters   ---->    Retrieve Credentials   ---->  Connect to Redshift Database
                                                                          (AWS Secrets Manager)
                                                                                                                   │
                                                                                                                   ▼
                                                                                                                                                                            Logging & Job Completion    <----    Populate Integrated Layer   <----    Apply Business Rules     <----    Execute Stored Procedures
                                                
# 3. Integrated Layer to Linked Layer

File: 03_integrated_to_linked.py

## Purpose

Generates reporting-ready metric tables by executing stored procedures that populate the Linked Layer for downstream analytics and Power BI dashboards.

## Workflow

            Glue Job Trigger    ---->   Read Runtime Parameters   ---->    Retrieve Credentials   ---->  Connect to Source Database
                                                                          (AWS Secrets Manager)
                                                                                                                      │
                                                                                                                      ▼
                                                                                                                                                                            Power BI Ready   <----    Populate Linked Layer   <----  Generate Business Metrics  <----  Execute Metric Stored Procedures
                                                                                                                                                            
                                                                                                                                                       
# Technologies Used
- AWS Glue
- PySpark
- Python
- AWS Secrets Manager
- Amazon Redshift
- SQL Stored Procedures

# Confidentiality Notice

The scripts included in this repository are representative examples created for portfolio purposes. Business logic, table names, stored procedures, credentials, and implementation-specific details have been generalized or replaced with placeholders to protect confidential business information while demonstrating the overall ETL design and implementation approach.  
                                                                                                                                                
