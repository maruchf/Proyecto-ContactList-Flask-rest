"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os,json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Contact
#desde el archivo models se importan las clases 
#aqui están los endpoints y se configura

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
    
#configuración de endpoint para traer todos los contactos
@app.route('/contacts', methods=['GET'])
def handle_contacts():
    contacts= Contact.query.all()
    response_body=[]
    for contact in contacts:
        response_body.append(contact.serialize())
    return jsonify(response_body), 200

@app.route('/contacts', methods=['POST'])
def contact_create():
    body = request.get_json()
    if isinstance (body, dict):
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'full_name' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'address' not in body:
            raise APIException('You need to specify the address', status_code=400)
        if 'phone' not in body:
            raise APIException('You need to specify the phone', status_code=400)
    else: return "no es un diccionario"
    # at this point, all data has been validated, we can proceed to inster into the bd
    contact1 = Contact(full_name=body['full_name'], email=body['email'], address=body['address'], phone=body['phone'])
    db.session.add(contact1)
    db.session.commit()
    return "ok", 200

@app.route('/contacts/<int:position>',methods=['DELETE'])
def delete_contact(position):
    db.session.delete(Contact.query.get(position))
    db.session.commit()
    return '', 204

@app.route('/contacts/<int:position>', methods=['GET'])
def handle_contact_for_id(position):
    contact= Contact.query.get(position)
    if contact is None:
        return "This contact not exist", 400
    else:
        return jsonify(contact.serialize()),200

@app.route('/contacts/<int:position>', methods=['PUT'])
def update_allcontact(position):
    body = request.get_json()
    contact= Contact.query.get(position)
    if isinstance (body, dict):
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if contact is None:
            raise APIException("Contact is not in the list", status_code=400)
        if 'full_name' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'address' not in body:
            raise APIException('You need to specify the address', status_code=400)
        if 'phone' not in body:
            raise APIException('You need to specify the phone', status_code=400)
    else: return "no es un diccionario"
    # at this point, all data has been validated, we can proceed to inster into the bd
    Contact.query.filter(Contact.id==position).update({
        "email": body['email'],
        "full_name": body['full_name'],
        "address": body['address'],
        "phone": body['phone']
        })
    db.session.commit()
    return "ok", 200

@app.route('/contacts/<int:position>', methods=['PATCH'])
def upgrade_contact(position):
    body = request.get_json()
    contact_to_upgrade = Contact.query.get(position)
    if isinstance (body, dict):
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if contact_to_upgrade is None:
            raise APIException("Contact is not in the list", status_code=400)
        if 'full_name' != None:
            new_full_name = body['full_name']
            contact_to_upgrade.full_name = new_full_name
        if 'email' != None:
            new_email = body['email']
            contact_to_upgrade.email = new_email
        if 'address' != None:
            new_address = body['address']
            contact_to_upgrade.address = new_address
        if 'phone' != None:
            new_phone = body['phone']
            contact_to_upgrade.phone = new_phone
    db.session.commit()
    return 'Contact update',200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
