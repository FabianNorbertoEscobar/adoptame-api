from carrito import Carrito
from inventario import Inventario
from flask import Flask, jsonify, request, redirect
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.json_encoder = LazyJSONEncoder

template = dict(
    info={
        'title': LazyString(lambda: 'API de Adoptame'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'API REST del sitio web Adoptame'),
    },
    host=LazyString(lambda: request.host),
    schemes=[LazyString(lambda: 'https' if request.is_secure else 'http')],
    foo=LazyString(lambda: "Bar")
)
Swagger(app, template=template)

carrito = Carrito()  # Instanciamos un carrito
inventario = Inventario()  # Instanciamos un inventario

SWAGGER_UI = "/apidocs/"

# Ruta para obtener index
# Redirigir a swagger-ui
@app.route("/")
def index():
    """
    Ruta principal de la API que redirige al Swagger-UI.
    """
    return redirect(SWAGGER_UI)

class ProductosResource:

    @staticmethod
    @app.route("/productos/<int:codigo>", methods=["GET"])
    @swag_from(
        {
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "codigo",
                    "description": "El código del producto.",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                }
            ],
            "responses": {
                200: {
                    "description": "Datos del producto.",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "cantidad": {"type": "integer", "example": 0},
                            "codigo": {"type": "integer", "example": 0},
                            "descripcion": {"type": "string", "example": "string"},
                            "precio": {"type": "integer", "example": 0},
                        },
                    },
                },
                404: {"description": "Producto no encontrado."},
            },
        }
    )
    def obtener_producto(codigo):
        """
        Obtiene los datos de un producto según su código.
        """
        producto = inventario.consultar_producto(codigo)
        if producto:
            return (
                jsonify(
                    {
                        "codigo": producto.codigo,
                        "descripcion": producto.descripcion,
                        "cantidad": producto.cantidad,
                        "precio": producto.precio,
                    }
                ),
                200,
            )
        return jsonify({"message": "Producto no encontrado."}), 404

    @staticmethod
    @app.route("/productos", methods=["GET"])
    @swag_from(
        {
            "produces": ["application/json"],
            "responses": {
                200: {
                "description": "Datos de los productos.",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "cantidad": {"type": "integer", "example": 0},
                            "codigo": {"type": "integer", "example": 0},
                            "descripcion": {"type": "string", "example": "string"},
                            "precio": {"type": "integer", "example": 0},
                        },
                    },
                },
            },
            }
        }
    )
    def obtener_productos():
        """
        Obtiene la lista de productos del inventario.
        """
        return inventario.listar_productos()

    @staticmethod
    @app.route("/productos", methods=["POST"])
    @swag_from(
        {
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "cantidad": {"type": "integer"},
                            "codigo": {"type": "integer"},
                            "descripcion": {"type": "string"},
                            "precio": {"type": "number"},
                        },
                        "required": ["cantidad", "codigo", "descripcion", "precio"],
                    },
                }
            ],
            "responses": {
                200: {"description": "Producto agregado correctamente."},
                400: {"description": "Ya existe un producto con ese código."},
            },
        }
    )
    def agregar_producto():
        """
        Agrega un producto al inventario.
        """
        codigo = request.json.get("codigo")
        descripcion = request.json.get("descripcion")
        cantidad = request.json.get("cantidad")
        precio = request.json.get("precio")
        return inventario.agregar_producto(codigo, descripcion, cantidad, precio)

    @staticmethod
    @app.route("/productos/<int:codigo>", methods=["PUT"])
    @swag_from(
        {
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "codigo",
                    "description": "El código del producto.",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                },
                {
                    "name": "body",
                    "in": "body",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "cantidad": {"type": "integer"},
                            "descripcion": {"type": "string"},
                            "precio": {"type": "number"},
                        },
                        "required": ["cantidad", "descripcion", "precio"],
                    },
                }
            ],
            "responses": {
                200: {"description": "Producto modificado correctamente."},
                400: {"description": "Producto no encontrado."},
            },
        }
    )
    def modificar_producto(codigo):
        """
        Modifica un producto del inventario.
        """
        nueva_descripcion = request.json.get("descripcion")
        nueva_cantidad = request.json.get("cantidad")
        nuevo_precio = request.json.get("precio")
        return inventario.modificar_producto(
            codigo, nueva_descripcion, nueva_cantidad, nuevo_precio
        )

    @staticmethod
    @app.route("/productos/<int:codigo>", methods=["DELETE"])
    @swag_from(
        {
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "codigo",
                    "description": "El código del producto a eliminar.",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                }
            ],
            "responses": {
                200: {"description": "Producto eliminado correctamente."},
                400: {"description": "Producto no encontrado."},
            },
        }
    )
    def eliminar_producto(codigo):
        """
        Elimina un producto del inventario.
        """
        return inventario.eliminar_producto(codigo)

class CarritoResource:

    @staticmethod
    @app.route("/carrito", methods=["POST"])
    @swag_from(
        {
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "cantidad": {"type": "integer"},
                            "codigo": {"type": "integer"},
                        },
                        "required": ["cantidad", "codigo"],
                    },
                }
            ],
            "responses": {
                200: {"description": "Producto agregado al carrito correctamente."},
                404: {"description": "Producto no encontrado."},
            },
        }
    )
    def agregar_carrito():
        """
        Agrega un producto al carrito.
        """
        codigo = request.json.get("codigo")
        cantidad = request.json.get("cantidad")
        inventario = Inventario()
        return carrito.agregar(codigo, cantidad, inventario)

    @staticmethod
    @app.route("/carrito", methods=["GET"])
    @swag_from(
        {
            "produces": ["application/json"],
            "responses": {
                200: {
                "description": "Contenido del carrito.",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "cantidad": {"type": "integer", "example": 0},
                            "codigo": {"type": "integer", "example": 0},
                            "descripcion": {"type": "string", "example": "string"},
                            "precio": {"type": "integer", "example": 0},
                        },
                    },
                },
            },
            }
        }
    )
    def obtener_carrito():
        """
        Obtiene el contenido del carrito.
        """
        return carrito.mostrar()

    @staticmethod
    @app.route("/carrito", methods=["DELETE"])
    @swag_from(
        {
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "body",
                    "in": "body",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "cantidad": {"type": "integer"},
                            "codigo": {"type": "integer"},
                        },
                        "required": ["cantidad", "codigo"],
                    },
                }
            ],
            "responses": {
                200: {"description": "Producto quitado del carrito correctamente."},
                404: {"description": "El producto no se encuentra en el carrito."},
            },
        }
    )
    def eliminar_carrito():
        """
        Elimina un producto del carrito.
        """
        codigo = request.json.get("codigo")
        cantidad = request.json.get("cantidad")
        return carrito.quitar(codigo, cantidad)

# Registrar los recursos en la aplicación
app.add_url_rule(
    "/productos/<int:codigo>",
    view_func=ProductosResource.obtener_producto,
    methods=["GET"],
)
app.add_url_rule(
    "/productos",
    view_func=ProductosResource.obtener_productos,
    methods=["GET"],
)
app.add_url_rule(
    "/productos",
    view_func=ProductosResource.agregar_producto,
    methods=["POST"],
)
app.add_url_rule(
    "/productos/<int:codigo>",
    view_func=ProductosResource.modificar_producto,
    methods=["PUT"],
)
app.add_url_rule(
    "/productos/<int:codigo>",
    view_func=ProductosResource.eliminar_producto,
    methods=["DELETE"],
)
app.add_url_rule(
    "/carrito",
    view_func=CarritoResource.agregar_carrito,
    methods=["POST"],
)
app.add_url_rule(
    "/carrito",
    view_func=CarritoResource.obtener_carrito,
    methods=["GET"],
)
app.add_url_rule(
    "/carrito",
    view_func=CarritoResource.eliminar_carrito,
    methods=["DELETE"],
)

if __name__ == "__main__":
    app.run()
#    with app.app_context():
#        app.run(debug=True)
