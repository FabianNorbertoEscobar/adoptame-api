from persona import Persona
from animal import Animal
from adopcion import Adopcion
from db import get_db_connection
from flask import jsonify

class Legajo:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def agregar_persona(self, dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad,
                        codigo_postal, telefono, email, estado_civil, url_foto):
        sql = f'INSERT INTO persona (dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro) VALUES ("{dni}", "{nombre}", "{apellido}", "{fecha_nacimiento}", "{nacionalidad}", "{direccion}", "{ciudad}", "{codigo_postal}", "{telefono}", "{email}", "{estado_civil}", "{url_foto}", CURRENT_TIMESTAMP);'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Persona agregada correctamente.'}), 200

    def consultar_persona(self, id):
        sql = f'SELECT * FROM persona WHERE id = {id};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            id, dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro = row
            return Persona(id, dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro)
        return None

    def modificar_persona(self, id, dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad,
                          codigo_postal, telefono, email, estado_civil, url_foto):
        producto = self.consultar_persona(id)
        if producto:
            sql = f'UPDATE persona SET dni = "{dni}", nombre = "{nombre}", apellido = "{apellido}", fecha_nacimiento = "{fecha_nacimiento}", nacionalidad = "{nacionalidad}", direccion = "{direccion}", ciudad = "{ciudad}", codigo_postal = "{codigo_postal}", telefono = "{telefono}", email = "{email}", estado_civil = "{estado_civil}", url_foto = "{url_foto}" WHERE id = {id};'
            self.cursor.execute(sql)
            self.conexion.commit()
            return jsonify({'message': 'Persona modificada correctamente.'}), 200
        return jsonify({'message': 'Persona no encontrada.'}), 404

    def eliminar_persona(self, id):
        sql = f'DELETE FROM persona WHERE id = {id};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Persona eliminada correctamente.'}), 200
        return jsonify({'message': 'Persona no encontrada.'}), 404

    def listar_personas(self):
        self.cursor.execute("SELECT * FROM persona")
        rows = self.cursor.fetchall()
        personas = []
        for row in rows:
            id, dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto, fecha_registro = row
            persona = {'id': id, 'dni': dni, 'nombre': nombre, 'apellido': apellido, 'fecha_nacimiento': fecha_nacimiento, 'nacionalidad': nacionalidad, 'direccion': direccion,
                       'ciudad': ciudad, 'codigo_postal': codigo_postal, 'telefono': telefono, 'email': email, 'estado_civil': estado_civil, 'url_foto': url_foto, 'fecha_registro': fecha_registro}
            personas.append(persona)
        return jsonify(personas), 200

    def agregar_animal(self, nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen):
        sql = f'INSERT INTO animal (nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen) VALUES ("{nombre}", "{genero}", {edad}, "{raza}", {id_animal_tipo}, {castrado}, {desparasitado}, {vacunado}, {adoptado}, "{url_imagen}");'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Animal agregado correctamente.'}), 200

    def consultar_animal(self, id):
        sql = f'SELECT * FROM animal WHERE id = {id};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            id, nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen = row
            return Animal(id, nombre, genero, edad, raza, id_animal_tipo, bool(castrado), bool(desparasitado), bool(vacunado), bool(adoptado), url_imagen)
        return None

    def modificar_animal(self, id, nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen):
        producto = self.consultar_animal(id)
        if producto:
            sql = f'UPDATE animal SET nombre = "{nombre}", genero = "{genero}", edad = {edad}, raza = "{raza}", id_animal_tipo = {id_animal_tipo}, castrado = {castrado}, desparasitado = {desparasitado}, vacunado = {vacunado}, adoptado = {adoptado}, url_imagen = "{url_imagen}" WHERE id = {id};'
            self.cursor.execute(sql)
            self.conexion.commit()
            return jsonify({'message': 'Animal modificado correctamente.'}), 200
        return jsonify({'message': 'Animal no encontrado.'}), 404

    def eliminar_animal(self, id):
        sql = f'DELETE FROM animal WHERE id = {id};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Animal eliminado correctamente.'}), 200
        return jsonify({'message': 'Animal no encontrado.'}), 404

    def listar_animales(self):
        self.cursor.execute("SELECT * FROM animal")
        rows = self.cursor.fetchall()
        animales = []
        for row in rows:
            id, nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen = row
            animal = {'id': id, 'nombre': nombre, 'genero': genero, 'edad': edad, 'raza': raza, 'id_animal_tipo': id_animal_tipo,
                      'castrado': bool(castrado), 'desparasitado': bool(desparasitado), 'vacunado': bool(vacunado), 'adoptado': bool(adoptado), 'url_imagen': url_imagen}
            animales.append(animal)
        return jsonify(animales), 200

    def agregar_adopcion(self, id_animal, id_persona):
        sql = f'INSERT INTO adopcion (id_animal, id_persona, fecha_hora) VALUES ({id_animal}, {id_persona}, CURRENT_TIMESTAMP);'
        self.cursor.execute(sql)
        sql = f'UPDATE animal SET adoptado = TRUE WHERE id = {id_animal};'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Adopción agregada correctamente.'}), 200

    def consultar_adopcion(self, id):
        sql = f'SELECT * FROM adopcion WHERE id = {id};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            id, id_animal, id_persona, fecha_hora = row
            return Adopcion(id, id_animal, id_persona, fecha_hora)
        return None

    def modificar_adopcion(self, id, id_animal, id_persona):
        adopcion = self.consultar_adopcion(id)
        if adopcion:
            sql = f'UPDATE animal SET adoptado = FALSE WHERE id = {adopcion.id_animal};'
            self.cursor.execute(sql)
            sql = f'UPDATE adopcion SET id_animal = {id_animal}, id_persona = {id_persona} WHERE id = {id};'
            self.cursor.execute(sql)
            sql = f'UPDATE animal SET adoptado = TRUE WHERE id = {id_animal};'
            self.cursor.execute(sql)
            self.conexion.commit()
            return jsonify({'message': 'Adopción modificada correctamente.'}), 200
        return jsonify({'message': 'Adopción no encontrada.'}), 404

    def eliminar_adopcion(self, id):
        adopcion = self.consultar_adopcion(id)
        sql = f'UPDATE animal SET adoptado = FALSE WHERE id = {adopcion.id_animal};'
        self.cursor.execute(sql)
        sql = f'DELETE FROM adopcion WHERE id = {id};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Adopción eliminada correctamente.'}), 200
        return jsonify({'message': 'Adopción no encontrada.'}), 404

    def listar_adopciones(self):
        self.cursor.execute("SELECT * FROM adopcion")
        rows = self.cursor.fetchall()
        adopciones = []
        for row in rows:
            id, id_animal, id_persona, fecha_hora = row
            adopcion = {'id': id, 'id_animal': id_animal, 'id_persona': id_persona, 'fecha_hora': fecha_hora}
            adopciones.append(adopcion)
        return jsonify(adopciones), 200
