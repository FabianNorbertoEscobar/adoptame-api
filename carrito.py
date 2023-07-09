from producto import Producto
from inventario import Inventario
from db import get_db_connection
from flask import jsonify

class Carrito:
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()
        self.items = []

    def agregar(self, codigo, cantidad, inventario):
        producto = inventario.consultar_producto(codigo)
        if producto is None:
            return jsonify({'message': 'El producto no existe.'}), 404
        if producto.cantidad < cantidad:
            return jsonify({'message': 'Cantidad en stock insuficiente.'}), 400

        for item in self.items:
            if item.codigo == codigo:
                item.cantidad += cantidad
                sql = f'UPDATE productos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return jsonify({'message': 'Producto agregado al carrito correctamente.'}), 200

        nuevo_item = Producto(codigo, producto.descripcion, cantidad, producto.precio)
        self.items.append(nuevo_item)
        sql = f'UPDATE productos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Producto agregado al carrito correctamente.'}), 200

    def quitar(self, codigo, cantidad):
        for item in self.items:
            if item.codigo == codigo:
                if cantidad > item.cantidad:
                    return jsonify({'message': 'Cantidad a quitar mayor a la cantidad en el carrito.'}), 400
                item.cantidad -= cantidad
                if item.cantidad == 0:
                    self.items.remove(item)
                sql = f'UPDATE productos SET cantidad = cantidad + {cantidad} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return jsonify({'message': 'Producto quitado del carrito correctamente.'}), 200
        return jsonify({'message': 'El producto no se encuentra en el carrito.'}), 404

    def vaciar(self):
        for item in self.items:
            sql = f'UPDATE productos SET cantidad = cantidad + {item.cantidad} WHERE codigo = {item.codigo};'
            self.cursor.execute(sql)
            self.conexion.commit()
        self.items = []
        return jsonify({'message': 'Carrito vaciado correctamente.'}), 200

    def mostrar(self):
        productos_carrito = []
        for item in self.items:
            producto = {'codigo': item.codigo, 'descripcion': item.descripcion, 'cantidad': item.cantidad, 'precio': item.precio}
            productos_carrito.append(producto)
        return jsonify(productos_carrito), 200
