import os
from flask import Flask, request, jsonify, abort
from flask.wrappers import Response
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

# ROUTES
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    formatted_drinks = [drink.short() for drink in drinks]

    if len(drinks) == 0:
        abort(404)

    return jsonify({
        'success': True,
        "drinks": formatted_drinks
    })


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()
    formatted_drinks = [drink.long() for drink in drinks]

    if len(drinks) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': formatted_drinks
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    try:
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        formatted_drink = drink.long()

        return jsonify({
            'success': True,
            'drinks': [formatted_drink]
        })
    except:
        abort(422)


@app.route('/drinks/<drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    body = request.get_json()

    try:
        drink = Drink.query.get(drink_id)

        drink.title = body.get('title', None)
        recipe = body.get('recipe', None)
        drink.recipe = json.dumps(recipe)

        drink.update()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        abort(404)


@app.route('/drinks/<drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):

    try:
        drink = Drink.query.get(drink_id)
        drink.delete()

        return jsonify({
            'success': True,
            'delete': drink_id
        })
    except:
        abort(404)


# Error Handling
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'unauthorized'
    }), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'not found'
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

