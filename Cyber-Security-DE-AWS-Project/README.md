# Data Model

This folder contains the conceptual data model representing the logical relationships between key business entities used in the enterprise data engineering platform.The model illustrates how data from multiple source systems is integrated through a layered architecture to produce standardized, analytics-ready datasets for downstream reporting.

---

## 1. Conceptual Data Model

**File:** `1_Conceptual_DataModel.png`

### Purpose

Provides a high-level conceptual representation of the enterprise data model, showing how raw source data is transformed, integrated, and organized into business-ready datasets.

### Data Model Layers

### Raw Layer

The Raw Layer captures data from multiple enterprise source systems without applying business transformations. It serves as the landing zone for data ingestion while preserving source fidelity.

**Primary Data Sources**

- Tanium
- Tenable.io
- Tenable WAS
- KEV
- ServiceNow CMDB

---

### Integrated Layer

The Integrated Layer standardizes and consolidates data from multiple source systems into unified business entities.

Key entities include:

- Vulnerability
- Asset
- CMDB
- KEV
- Other Domains

This layer applies business rules, validation logic, and relationships to create consistent, analytics-ready datasets.

---

### Linked Layer

The Linked Layer contains business-ready datasets optimized for reporting and analytics.

Tables:

- vm_metrics
- vm_master_metrics`

This layer serves as the primary consumption layer for downstream reporting and Power BI dashboards.

---

## Key Features

- Multi-layer enterprise data architecture
- Standardized business entities
- Cross-domain relationship mapping
- Centralized data integration
- Analytics-optimized data model
- Scalable design supporting future data domains

---

## Business Value

The conceptual data model provides a standardized enterprise data foundation that enables:

- Consistent reporting across multiple source systems
- Improved data quality and governance
- Reusable business entities
- Simplified analytics development
- Scalable integration of additional data domains
- Reliable consumption for enterprise reporting and dashboards

---

## Design Highlights

- Layered enterprise data architecture
- Separation of Raw, Integrated, and Linked data layers
- Business-centric entity relationships
- Reusable data model for multiple reporting use cases
- Optimized for analytics and business intelligence

---

## Confidentiality Notice

This conceptual data model has been simplified and anonymized for portfolio purposes. Sensitive business information, proprietary table structures, internal identifiers, and implementation-specific details have been modified or omitted while preserving the overall architectural design and data modeling approach.
