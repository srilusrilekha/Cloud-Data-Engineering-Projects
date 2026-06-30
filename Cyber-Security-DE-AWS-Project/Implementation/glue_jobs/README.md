# AWS Glue ETL Jobs

This folder contains sample AWS Glue ETL jobs demonstrating the layered data engineering approach used to ingest, transform, and prepare data for enterprise reporting.

The scripts have been simplified and anonymized for portfolio purposes while preserving the overall ETL workflow and implementation approach.

---

## 1. Source to Raw Layer

**File:** `01_source_to_raw.py`

### Purpose

Extracts data from enterprise source systems, performs basic validation and standardization, and loads the data into the Amazon Redshift Raw Layer.

### Workflow

| Step | Activity |
|------|----------|
| 1 | 🚀 Glue Job Trigger |
| 2 | ⚙️ Read Runtime Parameters |
| 3 | 🔐 Retrieve Credentials (AWS Secrets Manager) |
| 4 | 🗄️ Connect to Source Database |
| 5 | 📥 Extract Source Data |
| 6 | ✔️ Validate & Standardize Data |
| 7 | 📤 Load into Redshift Raw Layer |
| 8 | 📊 Logging & Job Completion |

---
                                         
## 2. Raw Layer to Integrated Layer

**File:** `02_raw_to_integrated.py`

### Purpose

Transforms raw datasets into standardized business entities by executing Amazon Redshift stored procedures.

### Workflow

| Step | Activity |
|------|----------|
| 1 | 🚀 Glue Job Trigger |
| 2 | ⚙️ Read Runtime Parameters |
| 3 | 🔐 Retrieve Credentials (AWS Secrets Manager) |
| 4 | 🗄️ Connect to Amazon Redshift |
| 5 | ⚡ Execute Stored Procedures |
| 6 | 🔄 Apply Business Rules & Transformations |
| 7 | 📦 Populate Integrated Layer |
| 8 | 📊 Logging & Job Completion |

---                                                

## 3. Integrated Layer to Linked Layer

**File:** `03_integrated_to_linked.py`

### Purpose

Generates reporting-ready metric tables by executing stored procedures that populate the Linked Layer for Power BI dashboards.

### Workflow

| Step | Activity |
|------|----------|
| 1 | 🚀 Glue Job Trigger |
| 2 | ⚙️ Read Runtime Parameters |
| 3 | 🔐 Retrieve Credentials (AWS Secrets Manager) |
| 4 | 🗄️ Connect to Amazon Redshift |
| 5 | 📈 Execute Metric Stored Procedures |
| 6 | 📊 Generate KPI & Business Metrics |
| 7 | 📦 Populate Linked Layer |
| 8 | ✅ Power BI Ready |

---                                                                                                                                                         

## Technologies Used
- AWS Glue
- PySpark
- Python
- AWS Secrets Manager
- Amazon Redshift
- SQL Stored Procedures

---

## Confidentiality Notice

The scripts included in this repository are representative examples created for portfolio purposes. Business logic, table names, stored procedures, credentials, and implementation-specific details have been generalized or replaced with placeholders to protect confidential business information while demonstrating the overall ETL design and implementation approach.  
                                                                                                                                                
