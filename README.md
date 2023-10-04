## README.md

## Project Overview

The `prh_api` project is a Python application that fetches data for Finnish companies from PRH (https://www.prh.fi/) YTJ (https://www.ytj.fi/) API and uploads it to a PostgreSQL database. It provides functionality for both bulk data retrieval and single company data retrieval.
Bulk retrieval fetches the "input" company numbers from a specified PostgreSQL database.

## Project Setup

1. Create an `.env` file in the project root directory.
2. Add the following environmental variables to the `.env` file:

POSTGRES_OUTPUT_DB=<postgres_output_db_address>
POSTGRES_INPUT_DB=<postgres_input_db_address>

## Input Data Source

By default, the `bulk.py` file queries the "company" table in the `POSTGRES_INPUT_DB` database using the "company_number" and "pk" values to fetch data. This data is then uploaded to the `POSTGRES_OUTPUT_DB` database. If a "pk" value is supplied this will be used as a primary key for the companies and as a foreign key on linked tables.

If you want to use a different table and values, you can pass a query statement as a parameter to the `bulk_run` function in the `bulk.py` file. The query statement should be a SQLalchemy select() function queries. The query statement should return a company identifier (optional) and a Finnish company number (in the format "1234567-8").

## Building the Docker Image

To build the Docker image for the `prh_api` application, run the following command:
>`docker build -t prh_api:v1.0 .`


## Running the Program

Before running the program, you need to create the tables in the `POSTGRES_OUTPUT_DB` database. This can be done with the following command:
>`docker run <image_name>:<tag> python create_tables.py`


### Bulk Run

The bulk run fetches data for all companies provided with the query from the `POSTGRES_OUTPUT_DB` database. Existing companies in the `POSTGRES_OUTPUT_DB` database will be updated, and new entries will be made for companies that don't exist.

To perform a bulk run, use the following command:
>`docker run <image_name>:<tag>`


### Single Run

The single run fetches data for a single company and writes the data to the `POSTGRES_OUTPUT_DB` database.

To perform a single run, provide the company number as a command-line argument. Optionally, you can also provide a company UID (if not provided, one will be generated).

Use the following command for a single run:
>`docker run <image_name>:<tag> python single.py <company_number> --<company_uid> (optional)`

Make sure to replace `<image_name>` and `<tag>` with the appropriate values for your Docker image, and `<company_number>` and `<company_uid>` with appropriate values.