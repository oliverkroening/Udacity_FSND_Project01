from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import os
from models import setup_db, Plant

def create_app(test_config=None):
    ## create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    # )
    # CORS(app)
    cors = CORS(app, resources={r"*/api/*": {"origins": "*"}})

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)

    # @app.route("/")
    # @cross_origin()
    # def get_greeting():
    #     return jsonify({'message':'Hello, World!'})

    @app.route('/hello', methods=['GET', 'POST'])
    def greeting():
        if request.method == 'POST':
            return create_greeting()
        else:
            return send_greeting()


    @app.route('/entrees/<int:entree_id>')
    def retrieve_entree(entree_id):
        return 'Entree %d' % entree_id


    # Pagination
    @app.route('/entrees', methods=['GET']) 
    def get_entrees(): 
        page = request.args.get('page', 1, type=int)


    # CORS Headers 
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    
    @app.route('/messages')
    @cross_origin()
    def get_messages():
        return 'GETTING MESSAGES'