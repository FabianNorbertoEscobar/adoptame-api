from persona import Persona
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
