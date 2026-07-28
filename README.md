# enterprise-mdm-azure-medallion-architecture
Enterprise Master Data Management (MDM) solution implemented using Azure Data Lake Storage Gen2, Azure Databricks, Delta Lake, and Medallion Architecture.

# Enterprise Master Data Management using Azure Medallion Architecture

## Project Overview

This project demonstrates the implementation of an Enterprise Master Data Management (MDM) solution using Microsoft Azure.

The solution follows the Medallion Architecture to ingest, clean, standardize, and master customer data from multiple enterprise source systems using Azure Data Lake Storage Gen2, Azure Databricks, Delta Lake, and PySpark.

---

## Architecture

![Azure Medallion Architecture](Architecture/Azure_MDM_Medallion_Architecture.png)

---

## Architecture Workflow

```
                Synthetic Data Generation
      (generator.py → transformer.py → exporter.py)
                          │
                          ▼
                 master_customer_dirty.csv
                          │
                          ▼
           Azure Data Lake Storage Gen2 (Landing)
                          │
                          ▼
             Azure Databricks (Bronze Layer)
        Raw CSV → Delta Lake + Metadata Columns
                          │
                          ▼
             Azure Databricks (Silver Layer)
      Data Cleaning • Standardization • Validation
                          │
                          ▼
              Azure Databricks (Gold Layer)
         Golden Customer Records (Master Data)
                          │
                          ▼
          Analytics / Reporting / BI Applications
```

---

# Azure Services Used

- Azure Data Lake Storage Gen2 (ADLS Gen2)
- Azure Databricks
- Delta Lake
- Unity Catalog
- PySpark
- Azure Resource Group

---

# Project Structure

```
enterprise-mdm-azure-medallion-architecture/
│
├── Architecture/
│
├── data-generation/
│     generator.py
│     transformer.py
│     exporter.py
│
├── notebooks/
│     Bronze.py
│     Silver.py
│     Gold.py
│
├── sample-data/
│     master_customer_dirty.csv
│
├── screenshots/
│
├── documentation/
│
└── README.md
```

---

# Data Generation

Three Python modules were developed to simulate enterprise customer data.

### generator.py

- Generates synthetic customer data
- Creates CRM, ERP, Banking and Marketing datasets
- Simulates duplicate customer identities

### transformer.py

Introduces realistic data quality issues including:

- Missing values
- Typographical errors
- Mixed casing
- Invalid formats
- Duplicate records

### exporter.py

Exports generated datasets into CSV files that are uploaded into Azure Data Lake Storage Gen2.

---

# Medallion Architecture

## Landing Layer

- Stores raw CSV files
- Source for Azure Databricks ingestion

---

## Bronze Layer

- Reads raw CSV
- Adds ingestion timestamp
- Adds source file metadata
- Stores data as Delta Lake

---

## Silver Layer

Data standardization performed:

- Trimmed whitespace
- Standardized names
- Converted emails to lowercase
- Standardized city/state names
- Standardized gender values
- Corrected data types
- Removed invalid records

---

## Gold Layer

Creates the Enterprise Master Customer.

Features include:

- Golden Customer Record
- Customer deduplication
- Survivorship using customer_id
- Delta Lake storage

---

# Technologies Used

- Python
- PySpark
- Azure Databricks Runtime 17.x
- Azure Data Lake Storage Gen2
- Delta Lake
- Unity Catalog
- Git
- GitHub

---

# Record Counts

| Layer | Records |
|--------|---------:|
| Landing | 13,367 |
| Bronze | 13,367 |
| Silver | 13,367 |
| Gold | 12,868 |

A total of **499 duplicate customer records** were consolidated into Golden Customer Records.

---

# Repository Contents

- End-to-end Azure MDM pipeline
- Synthetic customer data generation
- Bronze notebook
- Silver notebook
- Gold notebook
- Architecture diagram
- Screenshots
- Sample dataset

---

# Future Enhancements

- Implement Delta Live Tables
- Integrate Azure Data Factory
- Automate orchestration using Azure Pipelines
- Implement advanced survivorship rules
- Real-time ingestion using Azure Event Hubs / Kafka

---


