import yaml
from sqlalchemy import create_engine
import pandas as pd

def read_crednetials():
    with open('credentials.yaml','r') as f:
        cred_dict = yaml.safe_load(f)
    return cred_dict

class RDSDatabaseConnector:
    def __init__(self, cred_dict):
        self.HOST = cred_dict['RDS_HOST']
        self.USER = cred_dict['RDS_USER']
        self.PASSWORD = cred_dict['RDS_PASSWORD']
        self.DATABASE = cred_dict['RDS_DATABASE']
        self.PORT = cred_dict['RDS_PORT']
        self.DATABASE_TYPE = 'postgresql'
        self.DBAPI = 'psycopg2'

    def SQLAlchemy_engine(self):
        engine = create_engine(f"{self.DATABASE_TYPE}+{self.DBAPI}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}")
        engine.execution_options(isolation_level='AUTOCOMMIT').connect()
        return engine

def get_loan_payments_df():
    cred_dict = read_crednetials()
    test = RDSDatabaseConnector(cred_dict)
    engine = test.SQLAlchemy_engine()
    loan_payments_df = pd.read_sql_table('loan_payments', engine)
    return loan_payments_df

def create_csv_file(df):
    df.to_csv('local_csv_file.csv')

df = get_loan_payments_df()
# df_size = df.size
# df_shape = df.shape
# print(f'Information on df')
# print(f'Size: {df_size}')
# print(f'Shape: {df_shape}')
# df_info = df.info()
print(df.columns)

# create_csv_file(get_loan_payments_df())