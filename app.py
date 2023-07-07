from carrito import Carrito
from inventario import Inventario
from legajo import Legajo
from flask import Flask, jsonify, request, redirect
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='*')

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

carrito = Carrito()
inventario = Inventario()
legajo = Legajo()

SWAGGER_UI = "/apidocs/"


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


class PersonasResource:

    @staticmethod
    @app.route("/personas/<int:id>", methods=["GET"])
    @swag_from(
        {
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "id",
                    "description": "El id de la persona.",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                }
            ],
            "responses": {
                200: {
                    "description": "Datos de la persona.",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "example": 0},
                            "dni": {"type": "string", "example": "string"},
                            "nombre": {"type": "string", "example": "string"},
                            "apellido": {"type": "string", "example": "string"},
                            "fecha_nacimiento": {"type": "string", "example": "string"},
                            "nacionalidad": {"type": "string", "example": "string"},
                            "direccion": {"type": "string", "example": "string"},
                            "ciudad": {"type": "string", "example": "string"},
                            "codigo_postal": {"type": "string", "example": "string"},
                            "telefono": {"type": "string", "example": "string"},
                            "email": {"type": "string", "example": "string"},
                            "estado_civil": {"type": "string", "example": "string"},
                            "url_foto": {"type": "string", "example": "string"},
                            "fecha_registro": {"type": "string", "example": "string"},
                        },
                    },
                },
                404: {"description": "Persona no encontrada."},
            },
        }
    )
    def obtener_persona(id):
        """
        Obtiene los datos de una persona según su id.
        """
        persona = legajo.consultar_persona(id)
        if persona:
            return (
                jsonify(
                    {
                        "id": persona.id,
                        "dni": persona.dni,
                        "nombre": persona.nombre,
                        "apellido": persona.apellido,
                        "fecha_nacimiento": persona.fecha_nacimiento,
                        "nacionalidad": persona.nacionalidad,
                        "direccion": persona.direccion,
                        "ciudad": persona.ciudad,
                        "codigo_postal": persona.codigo_postal,
                        "telefono": persona.telefono,
                        "email": persona.email,
                        "estado_civil": persona.estado_civil,
                        "url_foto": persona.url_foto,
                        "fecha_registro": persona.fecha_registro
                    }
                ),
                200,
            )
        return jsonify({"message": "Persona no encontrada."}), 404

    @staticmethod
    @app.route("/personas", methods=["GET"])
    @swag_from(
        {
            "produces": ["application/json"],
            "responses": {
                200: {
                    "description": "Datos de las personas.",
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 0},
                                "dni": {"type": "string", "example": "string"},
                                "nombre": {"type": "string", "example": "string"},
                                "apellido": {"type": "string", "example": "string"},
                                "fecha_nacimiento": {"type": "string", "example": "string"},
                                "nacionalidad": {"type": "string", "example": "string"},
                                "direccion": {"type": "string", "example": "string"},
                                "ciudad": {"type": "string", "example": "string"},
                                "codigo_postal": {"type": "string", "example": "string"},
                                "telefono": {"type": "string", "example": "string"},
                                "email": {"type": "string", "example": "string"},
                                "estado_civil": {"type": "string", "example": "string"},
                                "url_foto": {"type": "string", "example": "string"},
                                "fecha_registro": {"type": "string", "example": "string"},
                            },
                        },
                    },
                },
            }
        }
    )
    def obtener_personas():
        """
        Obtiene la lista de personas del legajo.
        """
        return legajo.listar_personas()

    @staticmethod
    @app.route("/personas", methods=["POST"])
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
                            "dni": {"type": "string", "example": "string"},
                            "nombre": {"type": "string", "example": "string"},
                            "apellido": {"type": "string", "example": "string"},
                            "fecha_nacimiento": {"type": "string", "example": "string"},
                            "nacionalidad": {"type": "string", "example": "string"},
                            "direccion": {"type": "string", "example": "string"},
                            "ciudad": {"type": "string", "example": "string"},
                            "codigo_postal": {"type": "string", "example": "string"},
                            "telefono": {"type": "string", "example": "string"},
                            "email": {"type": "string", "example": "string"},
                            "estado_civil": {"type": "string", "example": "string"},
                            "url_foto": {"type": "string", "example": "string"},
                        },
                        "required": ["id", "dni", "nombre", "apellido", "fecha_nacimiento", "nacionalidad", "direccion", "ciudad", "codigo_postal", "telefono", "email", "estado_civil", "url_foto"],
                    },
                }
            ],
            "responses": {
                200: {"description": "Persona agregada correctamente."},
            },
        }
    )
    def agregar_persona():
        """
        Agrega una persona al legajo.
        """
        dni = request.json.get("dni")
        nombre = request.json.get("nombre")
        apellido = request.json.get("apellido")
        fecha_nacimiento = request.json.get("fecha_nacimiento")
        nacionalidad = request.json.get("nacionalidad")
        direccion = request.json.get("direccion")
        ciudad = request.json.get("ciudad")
        codigo_postal = request.json.get("codigo_postal")
        telefono = request.json.get("telefono")
        email = request.json.get("email")
        estado_civil = request.json.get("estado_civil")
        url_foto = request.json.get("url_foto")
        return legajo.agregar_persona(dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto)

    @staticmethod
    @app.route("/personas/<int:id>", methods=["PUT"])
    @swag_from(
        {
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "id",
                    "description": "El id de la persona.",
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
                            "dni": {"type": "string", "example": "string"},
                            "nombre": {"type": "string", "example": "string"},
                            "apellido": {"type": "string", "example": "string"},
                            "fecha_nacimiento": {"type": "string", "example": "string"},
                            "nacionalidad": {"type": "string", "example": "string"},
                            "direccion": {"type": "string", "example": "string"},
                            "ciudad": {"type": "string", "example": "string"},
                            "codigo_postal": {"type": "string", "example": "string"},
                            "telefono": {"type": "string", "example": "string"},
                            "email": {"type": "string", "example": "string"},
                            "estado_civil": {"type": "string", "example": "string"},
                            "url_foto": {"type": "string", "example": "string"},
                        },
                        "required": ["id", "dni", "nombre", "apellido", "fecha_nacimiento", "nacionalidad", "direccion", "ciudad", "codigo_postal", "telefono", "email", "estado_civil", "url_foto"],
                    },
                }
            ],
            "responses": {
                200: {"description": "Persona modificada correctamente."},
                400: {"description": "Persona no encontrada."},
            },
        }
    )
    def modificar_persona(id):
        """
        Modifica una persona del legajo.
        """
        dni = request.json.get("dni")
        nombre = request.json.get("nombre")
        apellido = request.json.get("apellido")
        fecha_nacimiento = request.json.get("fecha_nacimiento")
        nacionalidad = request.json.get("nacionalidad")
        direccion = request.json.get("direccion")
        ciudad = request.json.get("ciudad")
        codigo_postal = request.json.get("codigo_postal")
        telefono = request.json.get("telefono")
        email = request.json.get("email")
        estado_civil = request.json.get("estado_civil")
        url_foto = request.json.get("url_foto")
        return legajo.modificar_persona(id, dni, nombre, apellido, fecha_nacimiento, nacionalidad, direccion, ciudad, codigo_postal, telefono, email, estado_civil, url_foto)

    @staticmethod
    @app.route("/personas/<int:id>", methods=["DELETE"])
    @swag_from(
        {
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "id",
                    "description": "El id de la persona a eliminar.",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                }
            ],
            "responses": {
                200: {"description": "Persona eliminada correctamente."},
                400: {"description": "Persona no encontrada."},
            },
        }
    )
    def eliminar_persona(id):
        """
        Elimina una persona del legajo.
        """
        return legajo.eliminar_persona(id)


class AnimalesResource:

    @staticmethod
    @app.route("/animales/<int:id>", methods=["GET"])
    @swag_from(
        {
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "id",
                    "description": "El id del animal.",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                }
            ],
            "responses": {
                200: {
                    "description": "Datos del animal.",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "example": 0},
                            "nombre": {"type": "string", "example": "string"},
                            "genero": {"type": "string", "example": "string"},
                            "edad": {"type": "integer", "example": 0},
                            "raza": {"type": "string", "example": "string"},
                            "id_animal_tipo": {"type": "integer", "example": 0},
                            "castrado": {"type": "bool", "example": True},
                            "desparasitado": {"type": "string", "example": True},
                            "vacunado": {"type": "string", "example": True},
                            "adoptado": {"type": "string", "example": True},
                            "url_imagen": {"type": "string", "example": "string"},
                        },
                    },
                },
                404: {"description": "Animal no encontrado."},
            },
        }
    )
    def obtener_animal(id):
        """
        Obtiene los datos de un animal según su id.
        """
        animal = legajo.consultar_animal(id)
        if animal:
            return (
                jsonify(
                    {
                        "id": animal.id,
                        "nombre": animal.nombre,
                        "genero": animal.genero,
                        "edad": animal.edad,
                        "raza": animal.raza,
                        "id_animal_tipo": animal.id_animal_tipo,
                        "castrado": animal.castrado,
                        "desparasitado": animal.desparasitado,
                        "vacunado": animal.vacunado,
                        "adoptado": animal.adoptado,
                        "url_foto": animal.url_imagen,
                    }
                ),
                200,
            )
        return jsonify({"message": "Animal no encontrado."}), 404

    @staticmethod
    @app.route("/animales", methods=["GET"])
    @swag_from(
        {
            "produces": ["application/json"],
            "responses": {
                200: {
                    "description": "Datos de los animales.",
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "example": 0},
                                "nombre": {"type": "string", "example": "string"},
                                "genero": {"type": "string", "example": "string"},
                                "edad": {"type": "integer", "example": 0},
                                "raza": {"type": "string", "example": "string"},
                                "id_animal_tipo": {"type": "integer", "example": 0},
                                "castrado": {"type": "bool", "example": True},
                                "desparasitado": {"type": "string", "example": True},
                                "vacunado": {"type": "string", "example": True},
                                "adoptado": {"type": "string", "example": True},
                                "url_imagen": {"type": "string", "example": "string"},
                            },
                        },
                    },
                },
            }
        }
    )
    def obtener_animales():
        """
        Obtiene la lista de animales del legajo.
        """
        return legajo.listar_animales()

    @staticmethod
    @app.route("/animales", methods=["POST"])
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
                            "nombre": {"type": "string", "example": "string"},
                            "genero": {"type": "string", "example": "string"},
                            "edad": {"type": "integer", "example": 0},
                            "raza": {"type": "string", "example": "string"},
                            "id_animal_tipo": {"type": "integer", "example": 0},
                            "castrado": {"type": "bool", "example": True},
                            "desparasitado": {"type": "string", "example": True},
                            "vacunado": {"type": "string", "example": True},
                            "adoptado": {"type": "string", "example": True},
                            "url_imagen": {"type": "string", "example": "string"},
                        },
                        "required": ["nombre", "genero", "edad", "raza", "id_animal_tipo", "castrado", "desparasitado", "vacunado", "adoptado", "url_imagen"],
                    },
                }
            ],
            "responses": {
                200: {"description": "Animal agregado correctamente."},
            },
        }
    )
    def agregar_animal():
        """
        Agrega un animal al legajo.
        """
        nombre = request.json.get("nombre")
        genero = request.json.get("genero")
        edad = request.json.get("edad")
        raza = request.json.get("raza")
        id_animal_tipo = request.json.get("id_animal_tipo")
        castrado = request.json.get("castrado")
        desparasitado = request.json.get("desparasitado")
        vacunado = request.json.get("vacunado")
        adoptado = request.json.get("adoptado")
        url_imagen = request.json.get("url_imagen")
        print(nombre)
        print(castrado)
        return legajo.agregar_animal(nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)

    @staticmethod
    @app.route("/animales/<int:id>", methods=["PUT"])
    @swag_from(
        {
            "consumes": ["application/json"],
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "id",
                    "description": "El id del animal.",
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
                            "nombre": {"type": "string", "example": "string"},
                            "genero": {"type": "string", "example": "string"},
                            "edad": {"type": "integer", "example": 0},
                            "raza": {"type": "string", "example": "string"},
                            "id_animal_tipo": {"type": "integer", "example": 0},
                            "castrado": {"type": "bool", "example": True},
                            "desparasitado": {"type": "string", "example": True},
                            "vacunado": {"type": "string", "example": True},
                            "adoptado": {"type": "string", "example": True},
                            "url_imagen": {"type": "string", "example": "string"},
                        },
                        "required": ["nombre", "genero", "edad", "raza", "id_animal_tipo", "castrado", "desparasitado", "vacunado", "adoptado", "url_imagen"],
                    },
                }
            ],
            "responses": {
                200: {"description": "Animal modificado correctamente."},
                400: {"description": "Animal n|o encontrado."},
            },
        }
    )
    def modificar_animal(id):
        """
        Modifica un animal del legajo.
        """
        nombre = request.json.get("nombre")
        genero = request.json.get("genero")
        edad = request.json.get("edad")
        raza = request.json.get("raza")
        id_animal_tipo = request.json.get("id_animal_tipo")
        castrado = request.json.get("castrado")
        desparasitado = request.json.get("desparasitado")
        vacunado = request.json.get("vacunado")
        adoptado = request.json.get("adoptado")
        url_imagen = request.json.get("url_imagen")
        return legajo.modificar_animal(id, nombre, genero, edad, raza, id_animal_tipo, castrado, desparasitado, vacunado, adoptado, url_imagen)

    @staticmethod
    @app.route("/animales/<int:id>", methods=["DELETE"])
    @swag_from(
        {
            "produces": ["application/json"],
            "parameters": [
                {
                    "name": "id",
                    "description": "El id del animal a eliminar.",
                    "in": "path",
                    "type": "integer",
                    "required": True,
                }
            ],
            "responses": {
                200: {"description": "Animal eliminado correctamente."},
                400: {"description": "Animal no encontrado."},
            },
        }
    )
    def eliminar_animal(id):
        """
        Elimina un animal del legajo.
        """
        return legajo.eliminar_animal(id)


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
app.add_url_rule(
    "/personas/<int:id>",
    view_func=PersonasResource.obtener_persona,
    methods=["GET"],
)
app.add_url_rule(
    "/personas",
    view_func=PersonasResource.obtener_personas,
    methods=["GET"],
)
app.add_url_rule(
    "/personas",
    view_func=PersonasResource.agregar_persona,
    methods=["POST"],
)
app.add_url_rule(
    "/personas/<int:id>",
    view_func=PersonasResource.modificar_persona,
    methods=["PUT"],
)
app.add_url_rule(
    "/personas/<int:id>",
    view_func=PersonasResource.eliminar_persona,
    methods=["DELETE"],
)
app.add_url_rule(
    "/animales/<int:id>",
    view_func=AnimalesResource.obtener_animal,
    methods=["GET"],
)
app.add_url_rule(
    "/animales",
    view_func=AnimalesResource.obtener_animales,
    methods=["GET"],
)
app.add_url_rule(
    "/animales",
    view_func=AnimalesResource.agregar_animal,
    methods=["POST"],
)
app.add_url_rule(
    "/animales/<int:id>",
    view_func=AnimalesResource.modificar_animal,
    methods=["PUT"],
)
app.add_url_rule(
    "/animales/<int:id>",
    view_func=AnimalesResource.eliminar_animal,
    methods=["DELETE"],
)

if __name__ == "__main__":
    app.run()
#    with app.app_context():
#        app.run(debug=True)
