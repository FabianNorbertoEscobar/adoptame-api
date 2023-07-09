from producto import Producto
from db import get_db_connection
from flask import jsonify

class Inventario:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    def agregar_producto(self, codigo, descripcion, cantidad, precio):
        producto_existente = self.consultar_producto(codigo)
        if producto_existente:
            return jsonify({'message': 'Ya existe un producto con ese código.'}), 400
        sql = f'INSERT INTO productos VALUES ({codigo}, "{descripcion}", {cantidad}, {precio});'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Producto agregado correctamente.'}), 200

    def consultar_producto(self, codigo):
        sql = f'SELECT * FROM productos WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            codigo, descripcion, cantidad, precio = row
            return Producto(codigo, descripcion, cantidad, precio)
        return None

    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio):
        producto = self.consultar_producto(codigo)
        if producto:
            sql = f'UPDATE productos SET descripcion = "{nueva_descripcion}", cantidad = {nueva_cantidad}, precio = {nuevo_precio} WHERE codigo = {codigo};' 
            self.cursor.execute(sql)
            self.conexion.commit()
            return jsonify({'message': 'Producto modificado correctamente.'}), 200
        return jsonify({'message': 'Producto no encontrado.'}), 404

    def eliminar_producto(self, codigo):
        sql = f'DELETE FROM productos WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            self.conexion.commit()
            return jsonify({'message': 'Producto eliminado correctamente.'}), 200
        return jsonify({'message': 'Producto no encontrado.'}), 404

    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        rows = self.cursor.fetchall()
        productos = []
        for row in rows:
            codigo, descripcion, cantidad, precio = row
            producto = {'codigo': codigo, 'descripcion': descripcion, 'cantidad': cantidad, 'precio': precio}
            productos.append(producto)
        return jsonify(productos), 200
