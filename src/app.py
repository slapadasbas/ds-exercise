from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from jsonschema import validate

import os
import sys
sys.path.append('src/')
import dataproc 
import modelling

app = Flask(__name__)
api = Api(app)

env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object('config.ProdConfig')
else:
    app.config.from_object('config.DevConfig')

class IsFraud(Resource):
    def post(self):
        
        schema = {
            "type": "object",
            "properties": {
                "step": {"type":"number"},
                "type": {"type":"string"},
                "amount": {"type": "number"},
                "nameOrig": {"type":"string"},
                "oldbalanceOrig": {"type": "number"},
                "newbalanceOrig": {"type": "number"},
                "nameDest": {"type": "string"},
                "oldbalanceDest": {"type": "number"},
                "newbalanceDest": {"type": "number"}
            },
            "required": [
                "step",
                "type",
                "amount",
                "nameOrig",
                "oldbalanceOrig",
                "newbalanceOrig",
                "nameDest",
                "oldbalanceDest",
                "newbalanceDest"
            ]
        }
        
        try:
            json_data = request.get_json(force=True)
            if json_data["type"] in ["CASH_IN", "DEBIT", "PAYMENT"]:
                return jsonify(isFraud=False)
            
            validate(
                instance=json_data,
                schema = schema
            )
            
        except Exception as e:
            return {"error": str(e).split('\n')[0]}
        
        data = dataproc.run(json_data)
        prediction = modelling.run(data)
        return jsonify(isFraud=bool(prediction))

api.add_resource(IsFraud, '/is-fraud')
