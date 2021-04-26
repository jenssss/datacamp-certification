# Based on https://towardsdatascience.com/deploying-a-machine-learning-model-as-a-rest-api-4a03b865c166
import json

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from pickle import load
import numpy as np

from multi_models import eval_model


app = Flask(__name__)
api = Api(app)


model_dump_file = "bmw_linreg_model.pckl"
with open(model_dump_file, "rb") as file_:
    models = load(file_)

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument("query")


class PredictSentiment(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args["query"]

        user_query = json.loads(user_query)
        # vectorize the user's query and make a prediction
        print("user_query", user_query)
        prediction = eval_model(models, **user_query)

        # create JSON object
        output = {"prediction": str(prediction)}

        return output


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictSentiment, "/")


if __name__ == "__main__":
    app.run(debug=True)
