import sqlite3

DATABASE = 'inventario.db'

def get_db_connection():
    print("Obteniendo conexion a la base de datos...")
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():

    print("Creando tablas si no existen...")

    conn = get_db_connection()
    cursor = conn.cursor()

    print("Creando tabla productos si no existe...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            codigo INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        );
    ''')
    conn.commit()

    print("Creando tabla animal_tipo si no existe...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animal_tipo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion VARCHAR(255) NOT NULL
        );
    ''')
    conn.commit()

    print("Creando tabla animal si no existe...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(50) NOT NULL,
            descripcion VARCHAR(255) NULL,
            edad INTEGER NULL,
            raza VARCHAR(50) NULL,
            id_animal_tipo INTEGER NOT NULL,
            castrado BOOLEAN NOT NULL,
            desparasitado BOOLEAN NOT NULL,
            vacunado BOOLEAN NOT NULL,
            adoptado BOOLEAN NOT NULL,
            url_imagen VARCHAR(255) NULL,
            FOREIGN KEY (id_animal_tipo) REFERENCES animal_tipo (id)
        );
    ''')
    conn.commit()

    print("Creando tabla persona si no existe...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS persona (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(50) NOT NULL,
            apellido VARCHAR(50) NOT NULL,
            fecha_nacimiento DATE NOT NULL,
            nacionalidad VARCHAR(50) NOT NULL,
            direccion VARCHAR(100) NOT NULL,
            ciudad VARCHAR(50) NOT NULL,
            codigo_postal VARCHAR(10) NULL,
            telefono VARCHAR(20) NOT NULL,
            email VARCHAR(100) NOT NULL,
            estado_civil VARCHAR(20) NOT NULL,
            url_foto VARCHAR(255) NULL,
            fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()

    print("Creando tabla adopcion si no existe...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS adopcion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_animal INT NOT NULL,
            id_persona INT NOT NULL,
            fecha_hora DATETIME NOT NULL,
            FOREIGN KEY (id_animal) REFERENCES animal (id),
            FOREIGN KEY (id_persona) REFERENCES persona (id)
        );
    ''')
    conn.commit()

    print("Fin creacion de tablas...")

    cursor.close()
    conn.close()

def create_database():
    print("Creando la base de datos si no existe...")
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.close()
    print("Fin creacion de la base de datos...")
    create_tables()

create_database()
