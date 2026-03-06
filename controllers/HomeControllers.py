from flask import Blueprint, jsonify

blueprint_home = Blueprint('home', __name__)

@blueprint_home.route('/', methods=['GET'])
def home():
    return jsonify({
        "mensaje": "Hola mundo",
        "status": "API funcionando correctamente"
    })
