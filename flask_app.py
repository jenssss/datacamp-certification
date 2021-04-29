# Based on https://towardsdatascience.com/deploying-a-machine-learning-model-as-a-rest-api-4a03b865c166
import json

from flask import Flask
from flask import send_file
from flask import request, make_response
from flask_restful import reqparse, Api, Resource
from pickle import load
import numpy as np

from multi_models import eval_model, pretty_print_prediction, load_models


app = Flask(__name__)
api = Api(app)

models = load_models()
    
# argument parsing
parser = reqparse.RequestParser()
parser.add_argument("query", required=True)


class PredictPrice(Resource):
    def post(self):
        # print(self.body)
        # use parser and find the user's query

        args = parser.parse_args()
        user_query = args["query"]
        user_query = json.loads(user_query)

        prediction = eval_model(models, **user_query)

        # create JSON object
        output = pretty_print_prediction(prediction)
        response = make_response(output)

        # This block is necessary due to cors
        if 'HTTP_ORIGIN' in request.environ and request.environ['HTTP_ORIGIN'] is not None:
            origin = request.environ['HTTP_ORIGIN']
            response.headers.add("access-control-allow-origin", origin)
        return response


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictPrice, "/")


@app.route('/bmw_front')
def serve_frontend():
    return send_file("predict_price.html")

@app.route('/bmw_fetcher.js')
def send_js():
    return send_file("bmw_fetcher.js")



if __name__ == "__main__":
    from os import environ
    app.run(host="0.0.0.0", port=environ.get("PORT", 5000))
