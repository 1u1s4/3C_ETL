import mysql.connector
from mysql.connector import Error

def execute_script_from_file(filename, connection):
    cursor = connection.cursor()
    with open(filename, 'r') as file:
        sql_script = file.read()
    sql_commands = sql_script.split(';')
    for command in sql_commands:
        if command.strip():
            try:
                cursor.execute(command)
            except Error as err:
                print(f"Error: '{err}'")
    cursor.close()

def main():
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(
            host='<HOST>',
            database='<DATABASE>',
            user='<USER>',
            password='<PASSWORD>',
            port='<PORT>'
        )

        if connection.is_connected():

            execute_script_from_file('create_tables.sql', connection)
            connection.commit()
    
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
    
    finally:
        if connection.is_connected():
            connection.close()
            print("Base de datos creada con éxito")
