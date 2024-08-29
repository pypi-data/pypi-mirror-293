from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import inspect
from sqlalchemy.sql import text
import pandas as pd
from krazy import utility_functions as uf

'''
PostgresSql wrapper functions
For all functions, pass connected engine
'''

def create_connection(username, host, database, password):
    '''
    Create sqlalchemy connection for postgresql
    '''
    url = URL.create(
    drivername="postgresql",
    username="root",
    host="finance-kartik-poc.cq4isu0u5wom.ap-southeast-1.rds.amazonaws.com",
    database="postgres",
    password=password
)
    return create_engine(url)

def get_schema_names(engine):
    '''
    Takes SQLAlchemy engine and returns schema names as list
    '''
    inspector = inspect(engine)
    return inspector.get_schema_names()

def get_table_names(engine)->dict:
    '''
    Takes SQLAlchemy engine and returns schema wise table names as dictionary
    '''
    inspector = inspect(engine)
    schemas = get_schema_names(engine)
    tables = {}
    for schema in schemas:
        tables[schema] = (inspector.get_table_names(schema=schema))
    return tables

def table_search(table_name: str, engine:create_engine)->list:
    '''
    Searches for given table name in tables on Postgressql Server
    Pass sqlalchemy engine with connection on
    '''

    table_names=get_table_names(engine)
    
    if table_names:
        srch_results = []
        for key in list(table_names.keys()):
            table_names_schema = table_names[key]
            for name in table_names_schema:
                if table_name in name.lower():
                    srch_results.append([key, name])
        return srch_results
    else:
        return None

def table_delete(schema, table_name, engine:create_engine)->None:
    '''
    Deletes given tabe on postgresql server
    '''
    
    table_list = table_search(table_name, engine)
    
    cur = engine.connect()
    cur.execute(text(f'Drop table if exists "{schema}".{table_name};'))
    cur.commit()

def create_table(df:pd.DataFrame, schema, table_name, engine:create_engine)->None:
    '''
    Creates table in Postgresql server based on dataframe supplied
    '''

    df_dtypes = uf.dtype_to_df(df)

    df_dtypes['Data type'] = ''
    
    for ind, row in df_dtypes.iterrows():
        if row['Type'] == 'datetime64[ns]':
            df_dtypes.loc[ind, 'Data type'] = 'date'
        elif row['Type'] == 'float64':
            df_dtypes.loc[ind, 'Data type'] = 'float8'
        elif row['Type'] == 'float':
            df_dtypes.loc[ind, 'Data type'] = 'float8'
        elif row['Type'] == 'int':
            df_dtypes.loc[ind, 'Data type'] = 'int8'
        elif row['Type'] == 'int64':
            df_dtypes.loc[ind, 'Data type'] = 'int8'
        elif df[row['Col']].astype(str).str.len().max() <= 90:
            max_len = df[row['Col']].astype(str).str.len().max()
            df_dtypes.loc[ind, 'Data type'] = f'varchar({max_len+10})'
        else:
            df_dtypes.loc[ind, 'Data type'] = 'text'

    col_string = []
    for ind, row in df_dtypes.iterrows():
        col_string.append(f'''"{row['Col']}" {row['Data type']}''')

    col_string = ', '.join(col_string)

    sql = f'Create table "{schema}".{table_name} ({col_string});'
    
    with engine.begin() as conn:
        conn.execute(text(sql))    
    
    # cur = engine.connect()
    # cur.execute(sql)
    # cur.commit()

def dbase_writer(df: pd.DataFrame, schema, table, engine:create_engine, append=True)->None:
    '''
    writes data to table. Accepts following arguments for append:
    True = append to existing data
    False = deletes all rows and then insert data into existing table
    delete_table = delete table, recreate table and writes data
    '''
    cur = engine.connect()

    if append=='delete_table':
        # delete table
        table_delete(schema=schema, table_name=table, engine=engine)
        print(f'Table: {table} deleted')

        # create table
        create_table(df, schema, table, engine)
        print(f'Table: {table} re-created')

    elif append==False:
        # delete rows
        cur.execute(f'Delete from "{schema}"{table};')
        print(f'Deleted all data from table: {table}')

    else:
        pass

    df.to_sql(table, engine, if_exists='append', index=False, schema=schema)

    print(f'Data written to table {table}')

def build_sql(cols:list, table:str, schema:str, follow_through:str)->str:
    '''
    builds sql string based on table name, schema and follow_through given
    '''
    cols = '","'.join(cols)
    sql = f'select "{cols}" from "{schema}".{table} {follow_through};'
    return sql