from datetime import datetime as dt
from matplotlib import pyplot as plt
from scipy import stats
from sqlalchemy import create_engine
from statsmodels.graphics.gofplots import qqplot
import missingno as msno
import numpy as np
import pandas as pd
import yaml

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

    def get_loan_payments_df(self):
        engine = self.SQLAlchemy_engine()
        loan_payments_df = pd.read_sql_table('loan_payments', engine)
        loan_payments_df.fillna(value = np.nan, inplace=True)
        return loan_payments_df
    
class DataTransform:
    def __init__(self, df):
        self.df = df

    def transform(self):
        def month_year(column_name): # for "issue_date" and "earliest_credit_line" columns
            self.df[column_name] = pd.to_datetime(self.df[column_name].apply(lambda x: dt.strptime(x, '%b-%Y')))

        def make_float_int(column_name):
            self.df[column_name] = self.df[column_name].astype('int64')

        def xmonths(column_name):
            # self.df[column_name] = self.df[column_name].apply(lambda x:x.split()[0])
            self.df[column_name] = self.df[column_name].str[:2].astype('float64')
            self.df.rename(columns={column_name: column_name + " (months)"}, inplace=True)
        def xyears(column_name):
            # self.df[column_name] = self.df[column_name].apply(lambda x:x.split()[0])
            self.df[column_name] = self.df[column_name].str[:2]
            self.df[column_name] = df[column_name].str.replace(' ', '')
            self.df.loc[df[column_name] == "<", column_name] = "0"
            self.df[column_name] = self.df[column_name].astype('float64')
            self.df.rename(columns={column_name: column_name + " (years)"}, inplace=True)

        month_year("issue_date")
        month_year("earliest_credit_line")
        xmonths("term")
        xyears("employment_length")

class DataFrameInfo:
    def __init__(self, df):
        self.df = df

    def describe_columns(self):
        print(self.df.info(verbose=True))

    def statistical_values(self):
        print(self.df.describe())

    def count_distinct_values_col(self):
        count_distinct_values_col_lst = []
        for (columnName, columnData) in self.df.items():
            count_distinct_values_col_lst.append(columnName, len(columnData.unique()))
        return count_distinct_values_col_lst

    def df_shape(self):
        print(self.df.shape)

    def null_count_percentage(self):
        null_count_percentage_lst = []
        for (columnName, columnData) in self.df.items():
            null_count_percentage_lst.append((columnName, (df[columnName].isna().sum() / len(df.index)) * 100))
        null_count_percentage_df = pd.DataFrame(null_count_percentage_lst, columns =['Column', 'Null_Count_Percentage'])
        return null_count_percentage_df

    def null_count(self):
        null_count_lst = []
        for (columnName, columnData) in self.df.items():
            null_count_lst.append((columnName, df[columnName].isna().sum()))
        null_count_df = pd.DataFrame(null_count_lst, columns =['Column', 'Null_Count'])
        return null_count_df
        
class Plotter:
    def __init__(self, df):
        self.df = df

    def null_matrix(self):
        msno.matrix(df)
    
    def null_bar(self):
        msno.bar(df)

    def col_skew(self, column_name):
        try:
            column_name_skew = column_name+"_skew"
            df[column_name_skew].hist(bins=50)
            print(f"Skew of {column_name} column is {df[column_name_skew].skew(numeric_only=True)}")
        except:
            df[column_name].hist(bins=50)
            print(f"Skew of {column_name} column is {df[column_name].skew(numeric_only=True)}")


    def qq_plot(self, column_name):
        qq_plot = qqplot(df[column_name] , scale=1 ,line='q', fit=True)
        plt.show()

    def iqr_visual(self, outlier_values):
        for column, values in outlier_values.items():
            plt.figure(figsize=(8, 6)) 
            plt.scatter(df.index, df[column], label='Data points', alpha=0.3) 
            if values:  # Check if there are outliers for this column
                plt.scatter(df.index[df[column].isin(values)], df[column][df[column].isin(values)],
                        color='red', label='Outliers')
            plt.xlabel('Index')  
            plt.ylabel(column)   
            plt.title(f"{column} Data with Outliers Highlighted")  
            plt.legend() 
            plt.show()

class DataFrameTransform:
    def __init__(self, df):
        self.df = df

    def drop_columns(self):
        self.df.drop(columns=['mths_since_last_delinq', 'mths_since_last_record',
                             'next_payment_date', 'mths_since_last_major_derog'], 
                    inplace=True)

    def impute(self):
        self.df['term (months)'] = df['term (months)'].fillna(df['term (months)'].median())
        self.df['employment_length (years)'] = df['employment_length (years)'].fillna(df['employment_length (years)'].median())
        self.df['funded_amount'] = df['funded_amount'].fillna(df['funded_amount'].mean())
        self.df['int_rate'] = df['int_rate'].fillna(df['int_rate'].mean())
        self.df.dropna(inplace=True)
    def null_count_percentage(self):
        null_count_percentage_lst = []
        for (columnName, columnData) in self.df.items():
            null_count_percentage_lst.append((columnName, (df[columnName].isna().sum() / len(df.index)) * 100))
        null_count_percentage_df = pd.DataFrame(null_count_percentage_lst, columns =['Column', 'Null_Count_Percentage'])
        return null_count_percentage_df

    def null_count(self):
        null_count_lst = []
        for (columnName, columnData) in self.df.items():
            null_count_lst.append((columnName, df[columnName].isna().sum()))
        null_count_df = pd.DataFrame(null_count_lst, columns =['Column', 'Null_Count'])
        return null_count_df

    def skew_data(self):
        def skew_log(column_name):
            df[column_name+"_skew"] = np.log(df[column_name])

        def skew_boxcox(column_name):
            transformed_data, lambda_value = stats.boxcox(df[column_name])
            df[column_name+"_skew"] = transformed_data

        def skew_yeojohnson(column_name):
            transformed_data, lambda_value = stats.yeojohnson(df[column_name])
            return transformed_data

        new_df = df.select_dtypes(include=['int64', 'float64'])
        for col in new_df.columns:
            if col in ["id", "member_id"]:
                continue
            else:
                column_name = str(col)+"_skew"
                df[column_name] = skew_yeojohnson(col)
                # print(f"Skew of {col} column is {new_df[column_name].skew(numeric_only=True)}")
    
    def outliers(self):
        def iqr_method(df):
            stats = df.describe()
            outlier_values = {}
            for columnName in df.columns:
                if columnName not in ["id", "member_id"] and columnName[-4:] != "skew":
                    columnData = df[columnName]
                    q1 = stats.loc['25%', columnName]
                    q3 = stats.loc['75%', columnName]
                    iqr = q3 - q1
                    check1 = q1 - 1.5 * iqr
                    check2 = q3 + 1.5 * iqr
                    values = df[(df[columnName] < check1) | (df[columnName] > check2)][columnName].tolist()
                    outlier_values[columnName] = values
            return outlier_values

        def zscore_method(df, threshold=3):
            outlier_values = {}
            for col in df.columns:
                data = df[col]
                zscores = np.abs((data - data.mean()) / data.std())
                outlier_values[col] = data[zscores > threshold].tolist()
            return outlier_values

        def outlier_comparison(outlier_values_iqr, outlier_values_zscore):
            true_outliers = {}
            for col in outlier_values_iqr.keys():
                iqr_outliers = set(outlier_values_iqr[col])
                zscore_outliers = set(outlier_values_zscore[col])  # Get outliers for the column, default to an empty list
                intersecting_outliers = list(iqr_outliers.intersection(zscore_outliers))
                if intersecting_outliers:
                    true_outliers[col] = intersecting_outliers
            return true_outliers
        
        def reduce_outliers(df, outliers):
            max_loss_percentage = 5
            initial_outliers_count = sum(len(values) for values in outliers.values())
            initial_data_length = len(df)
            max_allowed_loss = initial_data_length * max_loss_percentage / 100.0
            current_outliers_count = initial_outliers_count
            current_data_length = initial_data_length
            print('Initial data length:', initial_data_length)
            print('Initial outliers count:', initial_outliers_count)
            print('Max allowed loss:', max_allowed_loss)
            sorted_outliers = [val for sublist in outliers.values() for val in sublist]
            sorted_outliers.sort()
            trimmed_outliers = sorted_outliers[:current_outliers_count]
            data_loss = 0
            while current_data_length - current_outliers_count > max_allowed_loss:
                if data_loss >= max_allowed_loss:
                    break
                trimmed_outliers = trimmed_outliers[:int(len(trimmed_outliers) * 0.90)]  # Adjust trimming percentage 
                data_loss = len(trimmed_outliers)
                current_outliers_count = len(trimmed_outliers)
                current_data_length = initial_data_length - current_outliers_count
                print('Current data length:', current_data_length)
                print('Current outliers count:', current_outliers_count)
                print('Current data loss:', data_loss)
            # Updated outliers after trimming
            updated_outliers = {}
            for col in outliers.keys():
                updated_outliers[col] = [val for val in outliers[col] if val in trimmed_outliers]
            return updated_outliers
        
        new_df = self.df.select_dtypes(include=['int64', 'float64'])
        for col in new_df.columns:
            drop_cols = []
            if col[-4:] == "skew":
                drop_cols.append(col)
        new_df.drop(columns=drop_cols, inplace=True)
        outlier_values_iqr = iqr_method(new_df)
        outlier_values_zscore = zscore_method(new_df)
        true_outliers = outlier_comparison(outlier_values_iqr, outlier_values_zscore)
        return reduce_outliers(new_df,true_outliers)
    
    def remove_outliers(self, outliers):
        for column in self.df.columns:
            if column in outliers:
                outlier_values = outliers[column]
                self.df = self.df[~self.df[column].isin(outlier_values)]
        return self.df

def create_csv_file(df):
    df.to_csv('local_csv_file.csv')


# test code
cred_dict = read_crednetials()
test = RDSDatabaseConnector(cred_dict)
pd.set_option('display.max_columns', None)
df = test.get_loan_payments_df()
test_transform = DataTransform(df)
test_transform.transform()
test_dateframeinfo = DataFrameInfo(test_transform.df)
test_dataframetransform = DataFrameTransform(test_transform.df)
test_dataframetransform.drop_columns()
test_dataframetransform.impute()
test_dataframetransform.skew_data()
outliers = test_dataframetransform.outliers()
test_dataframetransform.remove_outliers(outliers)
graph3 = Plotter(test_dataframetransform.remove_outliers(outliers))
graph3.df.drop(columns=["id", "loan_amount", "funded_amount_inv","out_prncp_inv", "total_payment_inv","total_rec_prncp"], inplace=True)
print(graph3.df)