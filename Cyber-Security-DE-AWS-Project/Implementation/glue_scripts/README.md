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
