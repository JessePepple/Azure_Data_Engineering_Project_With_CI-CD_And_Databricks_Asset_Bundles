# Azure_Data_Engineering_Project_With_CI-CD_And_Databricks_Asset_Bundles
## Overview

This project demonstrates a complete Azure Data Engineering solution that processes data from ingestion to transformation and delivery using modern cloud-native best practices. The architecture leverages Azure SQL, Azure Data Factory, Azure Databricks, and Delta Live Tables (DLT) to build a scalable, reliable, and production-ready data pipeline.

<img width="1444" height="902" alt="CI:CD Spotify Project" src="https://github.com/user-attachments/assets/e4fefba5-4a79-4c3f-b0fa-0f8f27162fe5" />


## Architecture Summary
1. Data Source: Azure SQL Database

Azure SQL serves as the primary data source. The data extracted from relational tables forms the raw dataset that flows through various pipeline stages.

2. Data Ingestion: Azure Data Factory

Azure Data Factory (ADF) orchestrates and manages data ingestion activities.

Raw data is ingested into the Raw Bronze Layer.

Ingestion is designed to be incremental, reducing cost and runtime.

Pipelines use triggers, datasets, and linked services to securely move data.

Logic Apps was also used to track and give updates on piepline developmnents.

3. Data Processing & Enrichment: Azure Databricks

Azure Databricks handles data transformations using:

Spark Structured Streaming for processing enriched Silver Layer datasets.

Auto Loader and schema evolution where applicable.

Transformations include cleaning, enrichment, and business logic application.

4. Curated Gold Layer: Delta Live Tables (DLT)

Delta Live Tables (DLT) is used to build high‑quality curated datasets.

Slowly Changing Dimensions (SCD Type 2) are applied to dimension tables for historical tracking.

Upserts (SCD Type 1) are applied to fact tables to keep data up to date.

DLT ensures data quality, lineage, and reliability.

## Data Layers
Bronze (Raw Layer)

Stores ingested data exactly as received.

Incrementally loaded using ADF.

Maintains full fidelity of the source.

Silver (Enriched Layer)

Processed using Spark Structured Streaming.

Includes cleaned, joined, and enriched data elements.

Gold (Curated Layer)

Built using DLT Pipelines.

Dimensional models with SCD Type 2.

Fact tables using SCD Type 1 Upsert logic.

Used for analytics and BI consumption.

## CI/CD Deployment Practices
Azure DevOps & Git Integration

The project follows CI/CD standards for reliable deployment:

Source control maintained in Git.

Databricks notebooks and configurations managed with version control.

ADF pipelines integrated with ARM templates / Bicep / Git mode.

Environments follow Dev → Test → Prod promotion workflows.

## Data Factory CI/CD

Published ADF code is exported via ARM templates.

Release pipelines deploy to higher environments.

## Databricks CI/CD

Uses Asset Bundles or Repos CI to automate deployment.

Supports testing and promotion of notebooks, DLT configs, and workflows.

## Key Technologies

Azure SQL Database – Source system

Azure Data Factory – Orchestration & ingestion (incremental loads)

Azure Databricks – Spark transformations and streaming

Delta Lake / Delta Live Tables – Pipeline reliability, SCD feature implementation

Azure Storage / ADLS Gen2 – Data lake storage layers

## Languages 
SQL
Python(PySpark)

## Phase 1 Ingestion With Azure Data Factory
The project was initiated by establishing a Git repository for version-controlling and deploying our Data Factory code, after which a dedicated development branch was created for feature updates.
<img width="1440" height="718" alt="Screenshot 2025-11-18 at 18 20 16" src="https://github.com/user-attachments/assets/cb8882e5-9fb0-4714-8d85-11f502b80e0d" />

During pipeline development, I implemented the JSON watermark method. I created two JSON files: one called last_load.json, which stores a backfilled timestamp set far before the earliest record (to support the initial full load), and a second empty JSON file used during the process of shifting from historical backfill into incremental ingestion.


<img width="1440" height="718" alt="Screenshot 2025-11-18 at 20 37 40" src="https://github.com/user-attachments/assets/0a3ce0ef-c118-4080-808f-02e01e84fb37" />

The pipeline leverages an IF Statement activity to manage data ingestion. When new data is available, it is processed and backfilled based on the latest load_date. If no new data is found, the pipeline automatically removes ingested datasets to maintain data integrity and avoid duplicates. Before doing this I created pipeline parameters for our ingestion from the SQL source using this method means our data was dynamic and can be used for multiple ingestions for different tables



<img width="1440" height="718" alt="Screenshot 2025-11-18 at 20 37 51" src="https://github.com/user-attachments/assets/6f586640-dac3-4081-853a-cc56ef7c3bb0" />

<img width="1440" height="718" alt="Screenshot 2025-11-18 at 20 38 01" src="https://github.com/user-attachments/assets/8fdaee45-33a9-4ec3-9d2b-fcf84358ee21" />

Pipeline parameters were configured for sink ingestion. Although a ForEach activity was initially considered, the limited number of tables meant a simpler approach without an array of dictionaries was sufficient.

<img width="1440" height="718" alt="Screenshot 2025-11-18 at 20 38 09" src="https://github.com/user-attachments/assets/f158e233-1453-485a-aabb-19d2a4310e1f" />

<img width="1440" height="718" alt="Screenshot 2025-11-18 at 20 38 17" src="https://github.com/user-attachments/assets/c54a8914-2690-457f-9d85-3054b487b337" />

Using the output from the MAX CDC script, an additional column was created in the update_cdc copy activity to backfill data up to the last_load value, ensuring that the last_load.json in the data lake accurately reflects the latest processed records.

<img width="1440" height="718" alt="Screenshot 2025-11-18 at 20 38 29" src="https://github.com/user-attachments/assets/e58efe42-fc00-43de-8e56-55d98e727e77" />

## Our If Condition
Using this condition with if data read is greater than 0 means that only incremental loads will be processed, if not then data will be deleted to avoid duplications

<img width="1440" height="718" alt="Screenshot 2025-11-18 at 20 42 59" src="https://github.com/user-attachments/assets/3c00c69a-717d-41f4-8969-bf8ae5327159" />

Initial Load
<img width="1440" height="718" alt="Screenshot 2025-11-18 at 20 52 40" src="https://github.com/user-attachments/assets/7e6a85fc-c9fa-42cf-9988-6a46fda43908" />

Initial Load Again with No new Data read
<img width="1440" height="718" alt="Screenshot 2025-11-18 at 20 46 38" src="https://github.com/user-attachments/assets/358f39aa-635d-42dc-b99d-70c541451261" />
Processed data is automatically removed using the delete activity, maintaining data integrity and avoiding duplicates. With this approach, the data is fully ingested into the data lake and prepared for subsequent transformations using Azure Databricks.

## Phase 2 Transformations(Silver Enrichment Layer)

To kick off the project, I first created external locations for our Bronze, Silver, and Gold containers, followed by creating schemas for the Silver and Gold layers. With Unity Catalog enabled and previous projects already configured, it was straightforward to begin this new phase of the project.


<img width="1440" height="718" alt="Screenshot 2025-11-18 at 23 29 31" src="https://github.com/user-attachments/assets/b75acebf-5a9f-45ce-a10e-234ae779735a" />


<img width="1440" height="718" alt="Screenshot 2025-11-18 at 23 30 23" src="https://github.com/user-attachments/assets/10381610-1a12-40ad-9c7f-181d14a46358" />
<img width="1440" height="718" alt="Screenshot 2025-11-18 at 23 31 01" src="https://github.com/user-attachments/assets/4032c601-28cd-456c-8a18-3a5f5ff82c96" />

For the Silver layer, I leveraged Spark Structured Streaming with Auto Loaders. Compared to traditional batch processing, Structured Streaming enables incremental loads, while storing schema details and metadata via checkpoint locations and RocksDB, making it an ideal choice for this project. After transforming the data, the streams were written to the Silver layer.

<img width="1440" height="718" alt="Screenshot 2025-11-20 at 17 46 54" src="https://github.com/user-attachments/assets/b2866da3-f5f3-49c7-9af3-ecc8678d535e" />


<img width="1440" height="718" alt="Screenshot 2025-11-20 at 17 47 05" src="https://github.com/user-attachments/assets/1d6bc689-c980-4834-97f3-83bd604f1361" />

## Phase 3 Curating and Preparing Our Data With DLT(Gold Curated Layer)

For the Curated (Gold) layer, I utilized LakeFlow Declarative Pipelines (DLT). I implemented Slowly Changing Dimensions (SCD) Type 2 for dimension tables and SCD Type 1 for  our fact table. Since the dimension tables were already prepared at the source, there was no need to create new DimKeys or perform additional modeling compared to my other projects. The main task was to create an auto_cdc_flow to handle both SCD Type 1 and Type 2. After curating the data via DLT, it was successfully loaded into the SQL Data Warehouse.



Using DLT I created expectations for certain tables to ensure proper data quality afterwards I then created our SCD Type 2
<img width="1440" height="718" alt="Screenshot 2025-11-20 at 05 31 23" src="https://github.com/user-attachments/assets/11eae7e0-7b54-4949-ab12-5ab2f2f1fdf1" />
<img width="1440" height="718" alt="Screenshot 2025-11-20 at 05 31 15" src="https://github.com/user-attachments/assets/9e4485c5-77c1-43e7-baac-3af05841d27e" />
<img width="1440" height="718" alt="Screenshot 2025-11-20 at 05 31 07" src="https://github.com/user-attachments/assets/fa402b51-9849-4134-900e-c720b1aca44e" />
<img width="1440" height="718" alt="Screenshot 2025-11-20 at 05 30 14" src="https://github.com/user-attachments/assets/b5db1618-8275-4452-93b4-e1569ba24262" />

After testing our data with a  DryRun for our DLT Tables I ran our Tables which was a success


<img width="1440" height="718" alt="Screenshot 2025-11-20 at 05 32 38" src="https://github.com/user-attachments/assets/fa161d91-bb54-4fc8-9d28-aeae34e694ba" />

The successful upsert of records demonstrates that our SCD Type 2 implementation was effective, allowing historical changes to be tracked in the curated data. All project expectations were met also, marking the completion of the pipeline development and data curation process.

<img width="1440" height="718" alt="Screenshot 2025-11-20 at 05 32 54" src="https://github.com/user-attachments/assets/3e099a95-688a-472c-866e-1af704f8fea7" />


<img width="1440" height="718" alt="Screenshot 2025-11-20 at 05 33 04" src="https://github.com/user-attachments/assets/7dae21d7-82cc-4d1f-a3cf-88b9ffa10012" />

As shown this is one of our curated tables with SCD Type 2 implemented

<img width="1440" height="718" alt="Screenshot 2025-11-20 at 04 50 17" src="https://github.com/user-attachments/assets/dd1d48b4-b658-40b2-858e-9e3c8afcdb5a" />


## Loading Curated Gold Data To The Gold Container In The Data Lake

Curated tables from Databricks were loaded into the Gold layer of our Data Lake before being ingested into the Synapse Data Warehouse. This setup ensures that both data analysts and data scientists can leverage the datasets either in Databricks or in Synapse, depending on their workflow requirements.


<img width="1440" height="718" alt="Screenshot 2025-11-20 at 06 35 41" src="https://github.com/user-attachments/assets/95242f46-9750-4730-9bdf-0631376bdd43" />


## Databricks SQL Warehouse

Since our Data was loaded in Databricks SQL Warehouse I tested the curated data by running basic queries for analysis and creating Dashboards for visualisation thus validating our data

<img width="1440" height="718" alt="Screenshot 2025-11-20 at 06 39 17" src="https://github.com/user-attachments/assets/2d253826-9a8f-4850-bfc2-b690076ff3a4" />
<img width="1440" height="718" alt="Screenshot 2025-11-20 at 06 39 25" src="https://github.com/user-attachments/assets/fee422dc-d5b3-4fdb-a9ad-d790fcd910d8" />
<img width="1440" height="718" alt="Screenshot 2025-11-20 at 06 39 49" src="https://github.com/user-attachments/assets/9f80411f-f059-44c4-a9d7-82b373f8efd9" />
<img width="1440" height="718" alt="Screenshot 2025-11-20 at 06 40 35" src="https://github.com/user-attachments/assets/e8d6243a-8525-4e73-9a02-46a00917cddd" />
<img width="1440" height="718" alt="Screenshot 2025-11-20 at 06 40 49" src="https://github.com/user-attachments/assets/b7c2651c-fb81-4023-a65f-b25d93afaa1d" />
<img width="1440" height="718" alt="Screenshot 2025-11-20 at 06 42 51" src="https://github.com/user-attachments/assets/bf9f3d34-b041-4446-8d3d-6fde816197e7" />
<img width="1440" height="718" alt="Screenshot 2025-11-20 at 06 43 33" src="https://github.com/user-attachments/assets/4abf65a5-b7e9-4d71-b17b-5147b098246e" />

<img width="1440" height="718" alt="Screenshot 2025-11-20 at 06 45 11" src="https://github.com/user-attachments/assets/57616cac-09d9-43c7-bd3d-b4a7e6d41e87" />
<img width="1440" height="718" alt="Screenshot 2025-11-20 at 06 45 38" src="https://github.com/user-attachments/assets/e208df1b-7629-46a4-a319-55cede507684" />

## BI REPORTING

Thanks to Databricks Partner Connect, I was able to provide the BI connector to the Data Analyst, enabling them to directly query and visualize the cleaned data in Power BI with ease—without needing to rely on the SQL Data Warehouse. Followed after was loading my data in Synapse Warehouse.
