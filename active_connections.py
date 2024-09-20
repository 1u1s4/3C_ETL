import mysql.connector
from mysql.connector import Error

def get_active_connections():
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
            cursor.execute("SHOW STATUS LIKE 'Threads_connected';")
            result = cursor.fetchone()

            if result:
                print(f"Conexiones activas: {result[1]}")

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada.")

if __name__ == "__main__":
    get_active_connections()
