
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

    - created a github repository and cloned it onto local machine 
    - created a new conda environment to reduce the risk of version conflicts 
    - installed the relevant python packages to the new conda environment (psycopg2-binary, SQLAlchemy, PyYaml and Pandas)

- Milestone 2, Extarct the loans data from the cloud:

    - created db_utils.py file 
    - defined RDSDatabaseConnector class
    - created a credentials.yaml file
    - created .gitignore file and added credentials.yaml file to it for security
    - defined read_crednetials( ) function to load the credentials.yaml file and return the data dictionary contained within
    - wrote the \_\_init\_\_ method of the RDSDatabaseConnector class
    - wrote the SQLAlchemy_engine method of the RDSDatabaseConnector class which initialises a SQLAlchemy engine from the credentials provided to the class
    - wrote the get_loan_payments_df method which extracts data from the RDS database and returns it as a Pandas DataFrame
    - defined create_csv_file(df) function to save the data in .csv format, since we're dealing with tabular data (creating the local_csv_file.csv)

- Milestone 3, Exploratory Data Analysis

    - created a DataTransform class to handle column conversions to correct format.
    - created a DataFrameInfo class which contains methods that generate useful information about the DataFrame.
    - created a Plotter class to visualise insights from the data.
    - created a DataFrameTransform class to perform EDA transformations on the data.
    - removed/imputed missing values in the data and then created a method in the Plotter class to visualise the data and check that all null values had been removed.
    - identified skewed columns then created methods in the DateFrameTransform class to reduce this skew.
    - created a method to find outliers in the dataset.
    - created a method in the DataFrameTransform class to transform or remove the outliers from the dataset. 
    - identified which columns are highly correlated using the correlation matrix for the dataset to visualise it. 

- Milestone 4, Analysis and Visualisation

    - queried the data to check the current state of the payments.
    - checked what percentage of loans have been a loss to the company.
    - calculated the projected loss of the loans marked as Charged Off.
    - calculated the loss in revenue these loans would have generated for the company if they had finished their term.
    - calculated the total amount of customers who are currently behind with their loan payments and how much loss the company would incur if their status was changed to Charged Off.
    - compared columns which might be indicators against customers who have already stopped paying and customers who are currently behind on payments.
    - made the analysis and determined the columns contributing to loans not being paid off and visualised any interesting indicators.

