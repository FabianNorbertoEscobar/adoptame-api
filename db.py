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
            genero VARCHAR(255) NOT NULL,
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
            dni VARCHAR(20) NOT NULL,
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

def populate_tables():

    conn = get_db_connection()
    cursor = conn.cursor()

    print("Vaciando tablas...")
    cursor.executescript('''
        DELETE FROM productos;
        DELETE FROM animal_tipo;
        DELETE FROM animal;
        DELETE FROM persona;
        DELETE FROM adopcion;
    ''')
    conn.commit()
    print("Fin de vaciado de tablas")

    print("Insertando registros de ejemplo...")

    print("Insertando en tabla productos...")
    cursor.executescript('''
        INSERT INTO productos (codigo, descripcion, cantidad, precio)
        VALUES
            (1, 'Acondicionador para perros y gatos', 29, 4000.0),
            (2, 'Chapitas', 13, 100.0),
            (3, 'Shampoo para perros', 30, 3500.0),
            (4, 'Correas', 25, 1500.0),
            (5, 'Pipetas para gatos', 25, 850.0),
            (6, 'Collares con cencerro', 25, 1000.0),
            (7, 'Ratitas de goma', 14, 500.0),
            (8, 'Antipulgas para perros', 20, 1200.0),
            (9, 'Juguetes interactivos', 18, 800.0),
            (10, 'Camas para gatos', 12, 2000.0),
            (11, 'Alimento para perros (10 kg)', 40, 2500.0),
            (12, 'Cepillos para gatos', 15, 300.0),
            (13, 'Arnés para perros', 22, 800.0),
            (14, 'Juguetes chirriantes', 10, 350.0),
            (15, 'Cepillos para perros', 27, 400.0),
            (16, 'Alimento para gatos (5 kg)', 35, 1800.0),
            (17, 'Rascadores para gatos', 8, 1500.0),
            (18, 'Juguetes de cuerda', 20, 250.0),
            (19, 'Collares de lujo', 5, 5000.0),
            (20, 'Alimento para perros (2 kg)', 50, 800.0),
            (21, 'Arena para gatos (10 kg)', 15, 600.0),
            (22, 'Snacks para perros', 32, 350.0),
            (23, 'Juguetes masticables', 16, 450.0),
            (24, 'Arena para gatos (5 kg)', 20, 350.0),
            (25, 'Corralitos para cachorros', 7, 2000.0),
            (26, 'Comederos automáticos', 9, 1500.0),
            (27, 'Camas para perros', 23, 1800.0),
            (28, 'Alimento para gatos (1 kg)', 42, 400.0),
            (29, 'Pañales para perros', 18, 500.0),
            (30, 'Juguetes para pájaros', 12, 200.0);
            ''')
    conn.commit()

    print("Insertando en tabla tipo_animal...")
    cursor.executescript('''
        INSERT INTO animal_tipo (descripcion)
        VALUES ('gato');
        INSERT INTO animal_tipo (descripcion)
        VALUES ('perro');
    ''')
    conn.commit()

    print("Insertando en tabla animal...")
    cursor.executescript('''
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('GRISA', 'femenino', 2, null, '1', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/gatos/Grisa.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('ARTURO', 'masculino', 2, null, '1', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/gatos/Arturo.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('FELIPO', 'masculino', 2, null, '1', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/gatos/Felipo.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('LUCKY', 'masculino', 2, null, '1', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/gatos/Lucky.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('GARFIELD', 'masculino', 2, null, '1', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/gatos/Garfield.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('BELLA', 'femenino', 2, null, '1', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/gatos/Bella.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('HAYAKO', 'femenino', 2, null, '1', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/gatos/Hayako.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('REMO', 'no binario', 2, null, '1', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/gatos/Remo.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('FILO', 'masculino', 2, null, '1', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/gatos/Filo.jpg');

        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('ANGUSTIA', 'no binario', 2, null, '1', true, true, true, true, 'https://adoptame-ba.netlify.app/img/gatos/Angustia.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('CARLOS', 'femenino', 2, null, '1', true, true, true, true, 'https://adoptame-ba.netlify.app/img/gatos/Carlos.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('COSITA', 'masculino', 2, null, '1', true, true, true, true, 'https://adoptame-ba.netlify.app/img/gatos/Cosita.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('ROBERTO', 'masculino', 2, null, '1', true, true, true, true, 'https://adoptame-ba.netlify.app/img/gatos/Roberto.jpg');

        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('BLANCA', 'femenino', 2, null, '2', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/perros/Blanca.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('EDÉN', 'masculino', 2, null, '2', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/perros/Ed%C3%A9n.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('FACUNDO', 'masculino', 2, null, '2', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/perros/Facundo.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('LUCERO', 'masculino', 2, null, '2', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/perros/Lucero.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('MALEVO', 'masculino', 2, null, '2', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/perros/Malevo.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('ROLO', 'masculino', 2, null, '2', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/perros/Rolo.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('SILVA', 'femenino', 2, null, '2', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/perros/Silva.jpeg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('TERRA', 'no binario', 2, null, '2', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/perros/Terra.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('PANCHITO', 'masculino', 2, null, '2', false, false, false, false, 'https://adoptame-ba.netlify.app/img/home/tarjetas/perros/Panchito.jpeg');

        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('FRANCISCO', 'masculino', 2, null, '2', true, true, true, true, 'https://adoptame-ba.netlify.app/img/perros/Francisco.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('GAUCHO', 'masculino', 2, null, '2', true, true, true, true, 'https://adoptame-ba.netlify.app/img/perros/Gaucho.jpg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('JOAQUINA', 'femenino', 2, null, '2', true, true, true, true, 'https://adoptame-ba.netlify.app/img/perros/Joaquina.jpeg');
        INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)
        VALUES ('LOBITO', 'masculino', 2, null, '2', true, true, true, true, 'https://adoptame-ba.netlify.app/img/perros/Lobito.jpg');
    ''')
    conn.commit()

    print("Insertando en tabla persona...")
    cursor.executescript('''
        INSERT INTO persona (dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro)
        VALUES ('11111111', 'Juan', 'Perez', '1990-05-15', 'Argentina', 'Calle 123', 'Buenos Aires', '1234', '+54 9 123456789', 'juanperez@example.com', 'Soltero', 'http://ejemplo.com/foto1.jpg', CURRENT_TIMESTAMP);
        INSERT INTO persona (dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro)
        VALUES ('22222222', 'Maria', 'Gomez', '1985-10-20', 'Argentina', 'Avenida 456', 'Córdoba', '5678', '+54 9 987654321', 'mariagomez@example.com', 'Casada', 'http://ejemplo.com/foto2.jpg', CURRENT_TIMESTAMP);
        INSERT INTO persona (dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro)
        VALUES ('33333333', 'Carlos', 'Rodriguez', '1992-02-03', 'Argentina', 'Ruta 789', 'Rosario', '9012', '+54 9 234567890', 'carlosrodriguez@example.com', 'Soltero', 'http://ejemplo.com/foto3.jpg', CURRENT_TIMESTAMP);
        INSERT INTO persona (dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro)
        VALUES ('44444444', 'Laura', 'Lopez', '1988-12-10', 'Argentina', 'Calle 5678', 'Mendoza', '3456', '+54 9 876543210', 'lauralopez@example.com', 'Divorciada', 'http://ejemplo.com/foto4.jpg', CURRENT_TIMESTAMP);
        INSERT INTO persona (dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro)
        VALUES ('55555555', 'Juan', 'Perez', '1990-05-15', 'Argentina', 'Calle 123', 'Buenos Aires', '1234', '555-1234', 'juan@example.com', 'Soltero', 'http://ejemplo.com/juan.jpg', CURRENT_TIMESTAMP);
        INSERT INTO persona (dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro)
        VALUES ('66666666', 'María', 'Gómez', '1985-12-10', 'Argentina', 'Avenida 456', 'Córdoba', '5678', '555-5678', 'maria@example.com', 'Casada', 'http://ejemplo.com/maria.jpg', CURRENT_TIMESTAMP);
        INSERT INTO persona (dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro)
        VALUES ('77777777', 'Carlos', 'Rodríguez', '1992-08-25', 'Argentina', 'Calle 789', 'Rosario', '9012', '555-9012', 'carlos@example.com', 'Soltero', 'http://ejemplo.com/carlos.jpg', CURRENT_TIMESTAMP);
        INSERT INTO persona (dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro)
        VALUES ('88888888', 'Laura', 'López', '1988-03-18', 'Argentina', 'Avenida 987', 'Mendoza', '3456', '555-3456', 'laura@example.com', 'Viuda', 'http://ejemplo.com/laura.jpg', CURRENT_TIMESTAMP);
    ''')
    conn.commit()

    print("Insertando en tabla adopcion...")
    cursor.executescript('''
        INSERT INTO adopcion (id_animal, id_persona, fecha_hora)
        VALUES (10, 1, CURRENT_TIMESTAMP);
        INSERT INTO adopcion (id_animal, id_persona, fecha_hora)
        VALUES (11, 2, CURRENT_TIMESTAMP);
        INSERT INTO adopcion (id_animal, id_persona, fecha_hora)
        VALUES (12, 3, CURRENT_TIMESTAMP);
        INSERT INTO adopcion (id_animal, id_persona, fecha_hora)
        VALUES (13, 4, CURRENT_TIMESTAMP);
        INSERT INTO adopcion (id_animal, id_persona, fecha_hora)
        VALUES (23, 5, CURRENT_TIMESTAMP);
        INSERT INTO adopcion (id_animal, id_persona, fecha_hora)
        VALUES (24, 6, CURRENT_TIMESTAMP);
        INSERT INTO adopcion (id_animal, id_persona, fecha_hora)
        VALUES (24, 7, CURRENT_TIMESTAMP);
        INSERT INTO adopcion (id_animal, id_persona, fecha_hora)
        VALUES (25, 8, CURRENT_TIMESTAMP);
    ''')
    conn.commit()

    print("Fin insercion de registros de ejemplo...")

    cursor.close()
    conn.close()

create_database()

#solo correr esta fn recién creada las tablas si se quiere cargar datos de ejemplo
#populate_tables()
