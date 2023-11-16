
# Exploratory Data Analysis - Customer Loans in Finance
This project is to improve the performance and profitability of a loan portfolio for a large financial institution, where managing loans is a critical component of business operations.

## Why?
- Ensure informed decisions are made about loan approvals and risk is efficiently managed.
- Uncover patterns, relationships, and anomalies in the loan data.
- Enable the business to make more informed decisions about loan approvals, pricing, and risk management.
- Gain a deeper understanding of the risk and return associated with the business' loans.

## How?
- Gain a comprehensive understanding of the loan portfolio data.
- Perform exploratory data analysis on the loan portfolio, using various statistical and data visualisation techniques.
- Conduct exploratory data analysis on the loan data.

## Milestones
These are the steps made in completing the project.
- Milestone 1, Setting up the dev environment:
\
    - created a github repository and cloned it onto local machine 
    - created a new conda environment to reduce the risk of version conflicts 
    - installed the relevant python packages to the new conda environment (psycopg2-binary, SQLAlchemy, PyYaml and Pandas)

- Milestone 2, Extarct the loans data from the cloud:
\
    - created db_utils.py file 
    - defined RDSDatabaseConnector class
    - created a credentials.yaml file
    - created .gitignore file and added credentials.yaml file to it for security
    - defined read_crednetials( ) function to load the credentials.yaml file and return the data dictionary contained within
    - wrote the \_\_init\_\_ method of the RDSDatabaseConnector class
    - wrote the SQLAlchemy_engine method of the RDSDatabaseConnector class which initialises a SQLAlchemy engine from the credentials provided to the class
    - wrote the get_loan_payments_df method which extracts data from the RDS database and returns it as a Pandas DataFrame
    - defined create_csv_file(df) function to save the data in .csv format, since we're dealing with tabular data (creating the local_csv_file.csv)