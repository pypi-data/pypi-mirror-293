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

def table_delete(schema, table_name, engine:create_engine)->bool:
    '''
    Deletes given tabe on MS SQL Server
    '''
    
    table_list = table_search(table_name, engine)
    if table_name in table_list:
        cur = engine.connect()
        cur.execute(text(f'Drop table if exists "{schema}".{table_name};'))
        cur.commit()
        return True
    else:
        return False

def get_col_types(schema, table, engine:create_engine)->dict:
    '''takes schema, table and engine and returns columns information of the table'''
    cur = engine.connect()
    col_types = cur.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = {schema} AND TABLE_NAME = '{table}';").fetchall()
    col_dict = {}
    for elem in col_types:
        col_dict[elem[0]] = elem[1]
    
    return col_dict

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
    cur = engine.connect()
    cur.execute(sql)
    cur.commit()

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

    # write data
    data = df.values.tolist()
    cols = df.columns.tolist()
    cols2 = []
    for col in cols:
        cols2.append('[' + col + ']')
    cols = cols2.copy()
    del cols2
    cols = '(' + ', '.join(cols) + ')'

    data_str = "?," * len(df.columns.tolist())
    data_str = '(' + data_str[:-1] + ')'
    sql = f'Insert into "{schema}".{table} {cols} values {data_str};'

    with engine.begin() as conn:
        conn.execute(sql, data)

    print(f'Data written to table {table}')