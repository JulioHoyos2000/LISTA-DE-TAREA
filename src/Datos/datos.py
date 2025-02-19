import mysql.connector
from mysql.connector import Error
import bcrypt
import re

# Función para crear la conexión a la base de datos
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Dirección del servidor
            user='Julio_Hoyos',  # Usuario de MySQL
            password='12345678',  # Contraseña de MySQL
            database='listtarea'  # Nombre de la base de datos
        )

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

# Clase Usuario con integración a la base de datos
class Usuario:
    def __init__(self, id: str, name: str, email: str, password_hash: str, created_at=None):
        self._id = id
        self._name = name
        self._email = email
        self._password_hash = password_hash
        self._created_at = created_at  # La fecha de registro

    # Getters
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def get_password_hash(self):
        return self._password_hash

    def get_created_at(self):
        return self._created_at

    # Setters
    def set_id(self, id: str):
        self._id = id

    def set_name(self, name: str):
        self._name = name

    def set_email(self, email: str):
        self._email = email

    def set_password_hash(self, password_hash: str):
        self._password_hash = password_hash

    def set_created_at(self, created_at):
        self._created_at = created_at

    # Método para insertar usuario en la base de datos
    def save_to_db(self, connection):
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (name, email, password_hash, created_at) VALUES (%s, %s, %s, %s)"
            values = (self._name, self._email, self._password_hash, self._created_at)
            cursor.execute(query, values)
            connection.commit()
            print("Usuario guardado exitosamente.")
        except Error as e:
            print(f"Error al guardar usuario: {e}")
        finally:
            cursor.close()

    # Método para verificar si el correo ya está registrado
    @staticmethod
    def email_exists(connection, email):
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            return result is not None  # Retorna True si el correo existe
        except Error as e:
            print(f"Error al verificar correo: {e}")
            return False
        finally:
            cursor.close()

    # Método para verificar la contraseña
    @staticmethod
    def verify_password(connection, email, password):
        try:
            cursor = connection.cursor()
            query = "SELECT password_hash FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            if result:
                stored_hash = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    return True
                else:
                    return False
            return False
        except Error as e:
            print(f"Error al verificar la contraseña: {e}")
            return False
        finally:
            cursor.close()

    # Método para actualizar el correo de un usuario
    def update_email(self, connection, new_email):
        try:
            cursor = connection.cursor()
            query = "UPDATE users SET email = %s WHERE id = %s"
            cursor.execute(query, (new_email, self._id))
            connection.commit()
            self.set_email(new_email)  # Actualizar el atributo localmente también
            print(f"Email del usuario actualizado a {new_email}")
        except Error as e:
            print(f"Error al actualizar email: {e}")
        finally:
            cursor.close()

    def __str__(self):
        return f"Usuario(id='{self._id}', name='{self._name}', email='{self._email}', created_at='{self._created_at}')"


# Ejemplo de uso
if __name__ == "__main__":
    # Crear la conexión
    conn = create_connection()

    if conn:
        # Crear un nuevo usuario
        name = "Jose Carlos"
        email = "Jose_Carlos@example.com"
        password = "87654321"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Hashear la contraseña
        created_at = None  # Dejar que la base de datos maneje la fecha de registro

        # Verificar si el correo ya está registrado
        if Usuario.email_exists(conn, email):
            print("El correo electrónico ya está registrado.")
        else:
            usuario = Usuario(None, name, email, password_hash, created_at)
            usuario.save_to_db(conn)

        # Intentar inicio de sesión (verificar la contraseña)
        email_to_verify = "Jose_Carlos@example.com"
        password_to_verify = "87654321"
        if Usuario.verify_password(conn, email_to_verify, password_to_verify):
            print("Inicio de sesión exitoso.")
        else:
            print("Correo electrónico o contraseña incorrectos.")

        # Actualizar el email del usuario
        usuario.update_email(conn, "new.email@example.com")
        print(f"Nuevo email: {usuario.get_email()}")

        # Cerrar la conexión
        close_connection(conn)
