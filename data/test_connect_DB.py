
# USE THIS COMMAND TO MANUALLY CONNECT TO THE DB:
#   tsql -S azuredfserv.database.windows.net -U Demouser
    
# THIS STACKOVERFLOW LINK SOLVED IT
#   https://stackoverflow.com/a/65126815



import pyodbc 
server = 'tcp:azuredfserv.database.windows.net' 
database = 'Azuredf' 
username = 'Demouser' 
password = 'Knxdde#77' 
driver='{ODBC Driver 17 for SQL Server}'

#conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
#cursor = conn.cursor()
#
#cursor.execute("USE azuredf ;")
#
#cursor.commit()
#
#
#cursor.execute("SHOW TABLES;")
#
#cursor.execute("""SELECT *
#               FROM dbo_Objects ;
#               """)
#print(cursor.fetchall())
#
#
#conn.close()




with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT TOP 3 name, collation_name FROM sys.databases")
        row = cursor.fetchone()
        while row:
            print (str(row[0]) + " " + str(row[1]))
            row = cursor.fetchone()
            
            
        print("------\n")
        
        
        cursor.execute("""select schema_name(t.schema_id) as schema_name,
                               t.name as table_name,
                               t.create_date,
                               t.modify_date
                               from sys.tables t""")
        
        
        for row in cursor.fetchall():
            print(row)
            print()

        
        cursor.execute("""select t.name
                               from sys.tables t""")

        
        table_names = cursor.fetchall()
        print(table_names)
        

        for tbl in table_names:
            n = tbl[0]
            cursor.execute(f"""SELECT COLUMN_NAME,* 
                               FROM INFORMATION_SCHEMA.COLUMNS
                               WHERE TABLE_NAME = '{n}' AND TABLE_SCHEMA='dbo'""")
            columns = cursor.fetchall()
            
            
            cursor.execute(f"select TOP 10 * from {n} ;")
            table = cursor.fetchall()
#            print(n, "has entries : ", len(cursor.fetchall()))
            print(n)
            print()
            print(columns)
            print()
            print(table)
            
            print("-"*30, "\n\n")


#
#from os import getenv
#import pymssql
#
#server = 'azuredfserv.database.windows.net'
#port = '1443'
#database = 'Azuredf'
#user = 'Demouser'
#password = 'Knxdde#77'   
#driver='{FreeTDS}' # driver not required with pymssql
#

#url = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+user+';PWD='+ password


 # 'tcp:myserver.database.windows.net,1433',
#conn = pyodbc.connect(server=server, database=database, uid=user, pwd=password)








#conn = pymssql.connect(server=server, user=user, password=password, database=database, port=port)

#con_string = 'mssql+pymssql://{}:{}@{}:{}/{}'.format(user, password, server, port, database)



print(conn)

#cursor = conn.cursor()
#print(cursor.execute("SHOW TABLES;").fetch())
#print(cursor.execute("SELECT * FROM dbo_Objects;"))
#row = cursor.fetchone()
#while row:
#    print(row)
#    row = cursor.fetchone()

conn.close()









#import mysql.connector
#
#mydb = mysql.connector.connect(
#  host=server,
#  user=user,
#  password=password,
#  database=database,
#  port='
#)
#
#print(mydb)
#mydb.close()