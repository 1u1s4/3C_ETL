import mysql.connector
from mysql.connector import Error

def kill_all_connections():
    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='<HOST>',
            database='<DATABASE>',
            user='<USER>',
            password='<PASSWORD>',
            port='<PORT>'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SHOW PROCESSLIST;")
            processes = cursor.fetchall()

            for process in processes:
                process_id = process[0]
                # Evitar cerrar la conexión actual
                if process_id != connection.connection_id:
                    kill_query = f"KILL {process_id};"
                    cursor.execute(kill_query)

            print("Todas las conexiones activas han sido cerradas.")

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada.")

if __name__ == "__main__":
    kill_all_connections()
