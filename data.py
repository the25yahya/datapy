import mysql.connector
import sqlite3


###########################funtcions#################################
#function to perform CREATE operations 
def create_operation(cursor, table_name, values):
    """Inserts a row of values into the specified table.

    Args:
        cursor: A MySQL Connector/Python cursor object.
        table_name: The name of the table to insert into.
        values: A tuple of values to insert.

    Returns:
        None
    """

    query = f"INSERT INTO {table_name} VALUES ({','.join(['%s'] * len(values))})"
    cursor.execute(query, values)


#function to perform READ operations
def read_operation(cursor, table_name):
    cursor.execute( f"SELECT * FROM {table_name}")
    return cursor.fetchall()

#function to perform UPDATE operations
def update_operation(cursor, table_name, column, new_value, condition_value, condition_column):
    query = f"UPDATE {table_name} SET {column} = %s WHERE {condition_column} = %s"
    cursor.execute((query), (new_value, condition_value))
    
#function to perform DELETE operations 
def delete_operation(cursor, table_name, column, value): 
    query= f"DELETE FROM {table_name} WHERE {column} = %s"
    cursor.execute(query,(value,))
    
    
    #############user prompt##################
db_type = input("ENTER the the type of database (mysql/sqlite): ").lower()
if db_type == "mysql":
    host = input("ENTER mysql host: ")
    user = input("ENTER mysql username: ")
    password = input("ENTER mysql password: ")
    database = input("ENTER mysql database name: ")

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Connected to MySQL database")
    except mysql.connector.Error as err:
        print("Error connecting to MySQL database:", err)

elif db_type == "sqlite":
    database = input("ENTER sqlite database name: ")

    try:
        sqlite_conn = sqlite3.connect(database)
        print("Connected to SQLite database")
    except sqlite3.Error as err:
        print("Error connecting to SQLite database:", err) 
          
          
#create cursor object
cursor = conn.cursor()

#prompt user for CRUD operation deails
crud_operation = input("Enter the CRUD operation you want to perform (create/read/update/delete): ").lower()


#perform the selected CRUD operation
if crud_operation == "create":
    table_name = input("Enter table name: ")
    values = input("Enter values separated by comma: ").split(",")
    create_operation(cursor,table_name,values)
    conn.commit()
    print("Data inserted successfully.")
elif crud_operation ==  "read":
    table_name = input("Enter table name:")
    data = read_operation(cursor,table_name)
    print("Data retrieved")
    for row in data:
        print(row)
elif crud_operation == "update":
    table_name = input("Enter table name: ")
    column = input("Enter column to update: ")
    new_value = input("Enter new value: ")
    condition_column = input("Enter condition column: ")
    condition_value = input("Enter condition value: ")
    update_operation(cursor,table_name, column, new_value, condition_column, condition_value)
    conn.commit()
    print("Date updated successfully.")
elif crud_operation == "delete":
    table_name = input("Enter table name: ")
    column = input("Enter column to update: ")  
    value = input("Enter value to delete: ")      
    delete_operation(table_name, column, value)
    conn.commit()
    print("Data deleted successfully.")
else:
    print("INVALID CRUD OPERATION!!")
    
#close cursor and connection
cursor.close()
conn.close()    