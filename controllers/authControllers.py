import yaml
from flask import Blueprint, request, jsonify, Response
from services.authService import AuthService
from flasgger import swag_from

auth_bp = Blueprint("auth", __name__)


# =========================
# FUNCION RESPUESTA YAML
# =========================
def to_yaml(data):
    return Response(
        yaml.dump(data, allow_unicode=True),
        mimetype="application/x-yaml"
    )


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
@swag_from({
    "tags": ["Auth"],
    "summary": "Registrar usuario",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "username": "alex",
                    "email": "alex@mail.com",
                    "password": "123456"
                }
            }
        }
    },
    "responses": {
        201: {"description": "Usuario registrado"},
        409: {"description": "Usuario ya existe"}
    }
})
def register():

    if request.method == "GET":
        html_form = """
        <h2>Registro de Usuario</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required><br><br>
            <input name="email" placeholder="Email" required><br><br>
            <input name="password" type="password" placeholder="Password" required><br><br>
            <button type="submit">Registrar</button>
        </form>
        """

        if "application/x-yaml" in request.headers.get("Accept", ""):
            return to_yaml({
                "message": "Endpoint de registro activo",
                "info": "Envía POST con username, email y password"
            })

        return html_form

    # POST
    if request.form:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
    else:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Debe enviar datos"}), 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    user = AuthService.register(username, email, password)

    if not user:
        return jsonify({"error": "El usuario ya existe"}), 409

    response_data = {
        "message": "Usuario registrado correctamente",
        "user": user.to_dict()
    }

    if "application/x-yaml" in request.headers.get("Accept", ""):
        return to_yaml(response_data)

    return jsonify(response_data), 201


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["POST"])
@swag_from({
    "tags": ["Auth"],
    "summary": "Login de usuario",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "username": "alex",
                    "password": "123456"
                }
            }
        }
    },
    "responses": {
        200: {"description": "Login exitoso"},
        401: {"description": "Credenciales inválidas"}
    }
})
def login():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Debe enviar JSON"}), 400

    if not all(k in data for k in ("username", "password")):
        return jsonify({"error": "Faltan datos"}), 400

    user = AuthService.login(data["username"], data["password"])

    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 401

    response_data = {
        "message": "Login exitoso",
        "user": user.to_dict()
    }

    if "application/x-yaml" in request.headers.get("Accept", ""):
        return to_yaml(response_data)

    return jsonify(response_data), 200


# =========================
# GET USERS
# =========================
@auth_bp.route("/users", methods=["GET"])
@swag_from({
    "tags": ["Users"],
    "summary": "Obtener lista de usuarios",
    "responses": {
        200: {
            "description": "Lista de usuarios",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "username": "alex"},
                        {"id": 2, "username": "juan"}
                    ]
                }
            }
        }
    }
})
def get_users():

    users = AuthService.get_all_users()
    response_data = [user.to_dict() for user in users]

    if "application/x-yaml" in request.headers.get("Accept", ""):
        return to_yaml(response_data)

    return jsonify(response_data), 200


# =========================
# GET USER BY ID
# =========================
@auth_bp.route("/users/<int:user_id>", methods=["GET"])
@swag_from({
    "tags": ["Users"],
    "summary": "Obtener usuario por ID",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "required": True,
            "schema": {
                "type": "integer"
            }
        }
    ],
    "responses": {
        200: {"description": "Usuario encontrado"},
        404: {"description": "Usuario no encontrado"}
    }
})
def get_user(user_id):

    user = AuthService.find_by_id(user_id)

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    response_data = user.to_dict()

    if "application/x-yaml" in request.headers.get("Accept", ""):
        return to_yaml(response_data)

    return jsonify(response_data), 200


# =========================
# UPDATE USER
# =========================
@auth_bp.route("/users/<int:user_id>", methods=["PUT"])
@swag_from({
    "tags": ["Users"],
    "summary": "Actualizar usuario",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"}
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {
                    "username": "nuevo",
                    "email": "nuevo@mail.com",
                    "password": "123456"
                }
            }
        }
    },
    "responses": {
        200: {"description": "Usuario actualizado"},
        404: {"description": "Usuario no encontrado"}
    }
})
def update_user(user_id):

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Debe enviar JSON"}), 400

    user = AuthService.update_user(
        user_id,
        username=data.get("username"),
        email=data.get("email"),
        password=data.get("password")
    )

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    response_data = {
        "message": "Usuario actualizado correctamente",
        "user": user.to_dict()
    }

    if "application/x-yaml" in request.headers.get("Accept", ""):
        return to_yaml(response_data)

    return jsonify(response_data), 200


# =========================
# DELETE USER
# =========================
@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
@swag_from({
    "tags": ["Users"],
    "summary": "Eliminar usuario",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"}
        }
    ],
    "responses": {
        200: {"description": "Usuario eliminado"},
        404: {"description": "Usuario no encontrado"}
    }
})
def delete_user(user_id):

    success = AuthService.delete_user(user_id)

    if not success:
        return jsonify({"error": "Usuario no encontrado"}), 404

    response_data = {"message": "Usuario eliminado correctamente"}

    if "application/x-yaml" in request.headers.get("Accept", ""):
        return to_yaml(response_data)

    return jsonify(response_data), 200