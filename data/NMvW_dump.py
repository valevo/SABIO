## Server Manual

#  - this server is a Microsoft Azure Data Factory  
#    `ssh` not supported, directly make SQL queries via TPC (/UDP) 
#  - use this command to manually connect to the DB (`tqsl` uses the TDS protocol to do interaction between Linux and Microsoft SQL servers):  
#    `tsql -S azuredfserv.database.windows.net -U Demouser` 
#  - this [stackoverflow](https://stackoverflow.com/a/65126815) post solved getting pyodbc (Python tie-in of ODBC, an API for DBMSes) to work with the server
 
# ### Install

#  - unixODBC (`pacman -Syu unixodbc`)
#  - freeTDS (`pacman -Syu freetds`)
#  - msodbcsql (from https://aur.archlinux.org/packages/msodbcsql/; install from arch AUR for install instruction)
 
#  check `odbcinst -j` or `pyodbc.drivers()`



from time import time
from datetime import datetime
import glob
from tqdm import tqdm
import os

import pandas as pd
import numpy as np

import pyodbc


server = 'tcp:azuredfserv.database.windows.net' 
database = 'Azuredf' 
username = 'Demouser' 
password = 'Knxdde#77' 
driver='{ODBC Driver 17 for SQL Server}'


def table_to_DataFrame(connection, table_name, keys=None, until=None, random_n=None):
    
    keys = "*" if not keys else ",".join(keys)
    if not until:
        until = ""
    until = f"TOP {until}" if until else ""
    sample = f"TABLESAMPLE ({random_n} ROWS)" if random_n else ""
    query = f"SELECT {until} {keys} FROM {table_name} {sample};"
    print(query)
    df = pd.read_sql(query, connection)
    return df


def connect_to_DB():
    return pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)


t0 = time()

with connect_to_DB() as conn:
    q  = "SELECT t.name, t.modify_date FROM sys.tables t"
    tables = pd.read_sql(q, conn)
    tables = tables[tables.name != "Person"]

table_names = list(tables.name)


print("found tables:" + "\n\t".join(table_names) + "\n\n")

to_ignore = ["Objects"]

print("ignoring tables:" + "\n\t".join(to_ignore) + "\n\n")

to_download = [n for n in table_names if not n in to_ignore]

to_download = ["Objects"]

keys_of = {
    "Objects": ['DepartmentID', 'ClassificationID',
                 'ObjectName', 'Medium', 'Provenance','Exhibitions',
                 'BeginISODate', 'EndISODate', 'Dated', 'Title',
                 'Description', 'Notes', 'CuratorialRemarks', 'RelatedWorks',
                 'HistAttributions'
               ]
}


timestamp = datetime.now().strftime("%d_%m_%Y-%H_%M_%S")
cur_folder = f"NMvW_tables_{timestamp}"
os.mkdir(cur_folder)

with connect_to_DB() as conn:
    for tbl_name in tqdm(to_download):
        cur_tbl = table_to_DataFrame(conn, tbl_name, 
                                     keys=keys_of["Objects"], until=None, random_n=5000)
        cur_tbl.to_csv(f"{cur_folder}/{tbl_name}.csv.gz", index=False)