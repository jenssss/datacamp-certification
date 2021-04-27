# Based on https://towardsdatascience.com/deploying-a-machine-learning-model-as-a-rest-api-4a03b865c166
import json

from flask import Flask
from flask import render_template, send_from_directory, send_file
from flask import request, make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from pickle import load
import numpy as np

from multi_models import eval_model


app = Flask(__name__)
api = Api(app)


model_dump_file = "bmw_linreg_model.pckl"
with open(model_dump_file, "rb") as file_:
    models = load(file_)

# @app.route("/", methods=["POST"])
# def create_entry():

#     req = request.get_json()

#     print(req)

#     res = make_response(jsonify(req), 200)

#     return res

    
# argument parsing
parser = reqparse.RequestParser()
parser.add_argument("query", required=True)


def pretty_print_prediction(prediction):
    print(prediction)
    price = float(prediction["price"])
    low_bound = float(prediction["95% lower bound"])
    upper_bound = float(prediction["95% upper bound"])
    return f"Price: {price:.0f}$, 95% of prices between {low_bound:.0f}$ and {upper_bound:.0f}$"


class PredictPrice(Resource):
    def post(self):
        # print(self.body)
        # use parser and find the user's query

        args = parser.parse_args()
        # print("args", args)
        user_query = args["query"]
        # print(user_query)
        user_query = json.loads(user_query)
        # vectorize the user's query and make a prediction
        # print("user_query", user_query)
        prediction = eval_model(models, **user_query)

        # create JSON object
        # output = {"prediction": pretty_print_prediction(prediction)}
        output = pretty_print_prediction(prediction)
        response = make_response(output)
        if 'HTTP_ORIGIN' in request.environ and request.environ['HTTP_ORIGIN'] is not None:
            origin = request.environ['HTTP_ORIGIN']
            print("origin", origin)
            response.headers.add("access-control-allow-origin", origin) # "http://127.0.0.1:5000/")
        return response


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictPrice, "/")


# @app.route('/bmw_pricer')
# def send_price():
#     return send_file("predict_price.html")

# @app.route('/bmw_fetcher.js')
# def send_js():
#     return send_file("bmw_fetcher.js")

# @app.route("/bmw_price")
# def guestbook():
#     return render_template("./predict_price.html")


if __name__ == "__main__":
    # app.run(debug=True)
    from os import environ
    app.run(host="0.0.0.0", port=environ.get("PORT", 5000))
