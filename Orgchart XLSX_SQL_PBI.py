from sqlalchemy import create_engine, text, MetaData, Table
from pandas import read_csv, DataFrame, to_datetime, notna
import sys
import time
from dotenv import load_dotenv
import os
import urllib

load_dotenv('./env.env')
CSV_PATH = os.environ.get("CSV_PATH")
XLSX_PATH = os.environ.get("XLSX_PATH")
TABLE_NAME = os.environ.get("TABLE_NAME")
DATABASE = os.environ.get("DATABASE")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
DRIVER = os.environ.get("DRIVER")
encoded_password = urllib.parse.quote(PASSWORD)
odbc_conn_str = (
    f"Driver={DRIVER};"
    f"Server={HOST},{PORT};"
    f"Database={DATABASE};"
    f"Uid={USERNAME};"
    f"Pwd={encoded_password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

params = urllib.parse.quote_plus(odbc_conn_str)
CONNECTION_STRING = f"mssql+pyodbc:///?odbc_connect={params}"
def set_types(df:DataFrame)->bool:
        try:
            df = df.astype({
                'Full Name': 'string',
                'Department': 'string',
                'Title': 'string'})
            mask = df['Date'].notnull()
            df.loc[mask, 'Date'] = to_datetime(df.loc[mask, 'Date']).dt.date
            return df
        except Exception as e:
            print(e, "Error setting column types")
            sys.exit(1)

def check_required_data(df:DataFrame):
    for col in df.columns:
        if 'required' in col:
            if df[col].isnull().any() or (df[col].str.strip() == "").any():
                print("Missing required data in column {}. Exiting...".format(col))
                sys.exit(1)

def print_dtypes(df, name):
    print(name.upper() + " ---- ")
    print(df.dtypes, "\n")

def csv_to_df(path:str)->DataFrame:

    try:
        df1 = read_csv(path, delimiter=";")
    except FileNotFoundError as e:
        print(e, "Couldn't find the CSV file at {} Exiting...".format(path))
        sys.exit(1)
    except Exception as e:
        print(e, "Failed to read CSV file. Exiting...")
        sys.exit(1)
    # can't parse columns so we'll pull them out, split it and remove ""
    split_columns = df1.columns[0].replace('"', '').split(";")
    # set df1 to the split rows
    df1 = df1.iloc[:,0].str.split(";", expand=True)
    # set the columns to the list of split columns
    df1.columns = split_columns
    df1 = df1.map(lambda x: x.replace('"', ""))
    try:
        check_required_data(df1)
        
        df1['Full Name'] = df1['First name (required)'] + ' ' + df1['Last name (required)']
        # Split 'Department|||Title' into two columns escape the | character. It's being treated weird, Maybe regex?
        df1[['Department', 'Title']] = df1['Department|||Title'].str.split('\\|\\|\\|', expand=True)
        df2 = df1[['Full Name', 'Department', 'Title', 'Date']]
        #trouble getting NaN dates to be Null in DB something to do with sqlAlchemy sets them to 0001-01-01 
        df2['Date'] = df2['Date'].where(notna(df2['Date']), None)
        df2 = df2.fillna("")
        df2 = set_types(df2)
        print_dtypes(df1, "df1")
        print_dtypes(df2, "df2")
    except KeyError:
        print(e,"\n","parsing failed. The CSV file is missing required columns or has an unhandled edge case. Exiting...")
        sys.exit(1)
    return df2

def delete_table_data(table_name:str, connection, consent=""):
    
    #dangerous function but sometimes you have to run with scissors
    if consent == 'delete it all':
        try:
            connection.execute(text("DELETE FROM {}".format(table_name)))
            return True
        except Exception as e:
            print(e)
            print("Failed to delete table data!")
            raise
    else:
        raise SyntaxError("If you really want to delete all the data in the table please pass 'delete it all' as the consent parameter")
def df_to_sql(df:DataFrame, table_name:str, retries=5, time_between_retries=5)->bool:
    # using a transation to ensure that the table retains data even if the connection fails. Without it the second connection for the insert could
    # fail and leave the table empty. Potentially leading to data loss depending on what happens to the CSV
    
    engine = create_engine(CONNECTION_STRING)
    try:
        with engine.begin() as connection:
            #connection made. Delete table data and insert new data
            try:
                # don't use DataFrame.to_sql with if_exists='replace' as that would delete and recreate the table structure each time. Plus remove indexes and primary keys.
                # when testing it also seemed to overwrite the tables data types. Better to seperate the concerns and let sql define the datamodel.
                delete_table_data(table_name, connection, consent='delete it all')
                metadata = MetaData()
                dict_of_dataframe = df.to_dict('records')
                table_object = Table(table_name, metadata, autoload_with=engine)
                stmt = table_object.insert().values(df.to_dict('records'))
                connection.execute(stmt)
                # commit the tran and close this may be automatic but better to be explicit
                connection.commit()
                connection.close()    
                return True
            except Exception as e:
                print(e)
                print("Connection made but failed to write or delete to SQL table. Rolling back transaction...")
                # roll back and close this may happen automatically but again i'll be explicit
                connection.rollback()
                connection.close()
                return False
    except Exception as e:
        # if connection fails try again. Nieve approach. careful with the retries as its recursive. Change to loop later.
        print(e)
        print("Failed to connect to SQL server. Panicing but holding on to hope. Trying again...")
        if retries > 0:
            time.sleep(time_between_retries)
            df_to_sql(df, table_name, retries-1, time_between_retries)
        else:
            print("Failed to connect to SQL server. ")
            return False


def df_to_xlsx(df:DataFrame, path:str)->None:
    # try to convert to xlsx. If it fails, print the error and continue
    try:
        df.to_excel(path, index=False)
    except Exception as e:
        print(e, "Failed to write to xlsx file. Continuing...")

def main():
    df = csv_to_df(CSV_PATH)
    success = df_to_sql(df, TABLE_NAME)
    if success:
        df_to_xlsx(df, XLSX_PATH)
        print("Success!")
    else:
        print("Failed to write to SQL. Exiting...")
        sys.exit(1)
main()