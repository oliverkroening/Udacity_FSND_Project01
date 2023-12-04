import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import sys

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
#### Done ####
with app.app_context():
    db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} 
        where drinks is the list of drinks or appropriate status code 
        indicating reason for failure
'''
#### Done ####
@app.route('/drinks', methods=['GET'])
def get_drinks():
    '''
    API endpoint that contains the data.short() data representation 
    of all drinks in the list of drinks.

    Allowed HTTP methods:
        - GET - obtain all drinks with their data representation (data.short())

    Authorized user roles:
        - Public (no restrictions)

    Requested Parameters: 
        - NONE
    Returned Parameters:
        - "success": boolean - information, if request was successful
        - "drinks": list - list of data representations of all drinks
    '''
    # query all drinks that are stored in the database
    drinks_all = Drink.query.all()
    
    # return 404 - Not found, in case there are no drinks in the database
    if drinks_all is None:
        abort(404)

    # perform drinks.short() to obtain the data representation on all drinks
    drinks = [drink.short() for drink in drinks_all]

    # return json with data representions
    return jsonify({
        "success": True,
        "drinks": drinks
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drinks} 
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
#### Done ####
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    '''
    API endpoint that contains the data.long() data representation 
    of all drinks in the list of drinks.

    Allowed HTTP methods:
        - GET - obtain all drinks with their data representation (data.long())

    Authorized user roles:
        - Barista
        - Manager
        - required permission: get:drinks-detail

    Requested Parameters: 
        - NONE
    Returned Parameters:
        - "success": boolean - information, if request was successful
        - "drinks": list - list of data representations of all drinks
    '''
    # query all drinks that are stored in the database
    drinks_all = Drink.query.all()
    
    # return 404 - Not found, in case there are no drinks in the database
    if drinks_all is None:
        abort(404)

    # perform drinks.long() to obtain the data representation on all drinks
    drinks = [drink.long() for drink in drinks_all]

    # return json with data representions
    return jsonify({
        "success": True,
        "drinks": drinks
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink} 
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
#### Done ####
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    '''
    API endpoint that allows authorized users to create a new row in
    the drinks table.

    Allowed HTTP methods:
        - POST - create new drink in the database

    Authorized user roles:
        - Manager
        - required permission: post:drinks

    Requested Parameters: 
        - jwt - token to check for permissions
    Returned Parameters:
        - "success": boolean - information, if request was successful
        - "drinks": list - list containing the created drink representation
    '''
    # get json from request
    data = request.get_json()

    # raise 422 error in case there is no data that could be extracted
    # from the request
    if data is None:
        abort(422)
    
    # extract title and recipe from request data
    title = data.get('title', None)
    recipe = data.get('recipe', None)

    # raise 422 error in case there is no title or recipe data in the request
    if (title is None) or (recipe is None):
        abort(422)
    
    # create new Drink object from extracted data
    # use json.dumps() to serialize recipe object to a JSON formatted string
    # source: https://reqbin.com/code/python/pbokf3iz/python-json-dumps-example
    try:
        drink = Drink(
            title = title,
            recipe = json.dumps(recipe)
        )
        # insert drink into Drink database
        drink.insert()

        # return json with data representions (drink.long())
        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    
    except:
        # raise 400 error in case of bad request during the
        # database operation
        # print error information
        print(sys.exc_info())
        abort(400)
    
    

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
        returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
#### Done ####
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    '''
    API endpoint that allows authorized users to update an existing row in
    the drinks table identified by the corresponding id in the URL.

    Allowed HTTP methods:
        - PATCH - update an existing drink in the database

    Authorized user roles:
        - Manager
        - required permission: patch:drinks

    Requested Parameters: 
        - jwt - token to check for permissions
        - id - ID of drink in the database
    Returned Parameters:
        - "success": boolean - information, if request was successful
        - "drinks": list - list containing the updated drink representation
    '''
    # get json from request
    data = request.get_json()

    # raise 422 error in case there is no data that could be extracted
    # from the request
    if data is None:
        abort(422)
    
    try:
        # get Drink object from database by id
        drink = Drink.query.get(id)

        # raise 404 error if <id> is not found
        if drink is None:
            abort(404)
        
        # extract title and recipe from request data and 
        # assign extracted data to database entry
        if "title" in data:
            title = data.get('title', None)
            drink.title = title
        
        if "recipe" in data:
            recipe = data.get('recipe', None)
            drink.recipe = recipe if type(recipe) == str else json.dumps(recipe)

        # return json with data representions (drink.long())
        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })

    except:
        # raise 400 error in case of bad request during the
        # database operation
        # print error information
        print(sys.exc_info())
        abort(400)
    
    

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
        returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
#### Done ####
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    '''
    API endpoint that allows authorized users to delete an existing row in
    the drinks table identified by the corresponding id in the URL.

    Allowed HTTP methods:
        - DELETE - delete an existing drink in the database

    Authorized user roles:
        - Manager
        - required permission: delete:drinks

    Requested Parameters: 
        - jwt - token to check for permissions
        - id - ID of drink in the database
    Returned Parameters:
        - "success": boolean - information, if request was successful
        - "delete": int - id of deleted drink
    '''
    try:
        # get drink with specific ID from URL via database query
        drink = Drink.query.get(id)
        
        # create HTTP 404 error (not found) in case id is not in the database
        if drink is None:
            abort(404)
      
        # delete drink
        drink.delete()
        # return json with data representions (drink.long())
        return jsonify({
            "success": True,
            "delete": id
        })
    
    except:
        # raise 400 error in case of bad request during the
        # database operation
        # print error information
        print(sys.exc_info())
        abort(400)

# Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(422)
def unprocessable(error):
    '''
    Error handling function for error 422 "unprocessable"
    '''
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
#### Done ####
@app.errorhandler(404)
def not_found(error):
    '''
    Error handling function for error 404 "Not Found"
    '''
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
#### Done ####
@app.errorhandler(AuthError)
def auth_error(error):
    '''
    Error handling function for authorization error (AuthError)
    '''
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

if __name__ == "__main__":
    app.debug = True
    app.run()
