from flask import Flask
from controllers.HomeControllers import blueprint_home
def create_app():
    app = Flask(__name__)
    app.register_blueprint_home(blueprint_home)
    @app.route('/')
    def home():
        return {'mesaje': 'hola mundo'},400

    return app
    
if __name__=='__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)