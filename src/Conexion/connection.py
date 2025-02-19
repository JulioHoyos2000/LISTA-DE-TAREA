import mysql.connector
from mysql.connector import Error


# Función para crear la conexión
def create_connection():
    try:
        # Configuración de la conexión
        connection = mysql.connector.connect(
            host='localhost',  # Dirección del servidor, puede ser 'localhost' o una IP
            user='Julio_Hoyos',  # Tu usuario de MySQL
            password='12345678',  # La contraseña del usuario
            database='listtarea'  # El nombre de la base de datos
        )

        # Verificar si la conexión fue exitosa
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None


# Función para cerrar la conexión
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Conexión cerrada")


# Prueba de conexión
if __name__ == "__main__":
    conn = create_connection()  # Crear la conexión
    if conn:
        close_connection(conn)  # Cerrar la conexión después de probarla
