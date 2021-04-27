from itertools import chain, combinations

import numpy as np
import pandas as pd
from scipy.stats import t


def calc_prediction_delta(y, y_pred, alpha=0.90, print_ratio_captured=False):
    n = len(y)
    resid = y - y_pred
    mean_resid = np.mean(y - y_pred)
    sN2 = 1 / (n - 1) * sum((resid - mean_resid) ** 2)
    dy = t.ppf((1 + alpha) / 2, n - 1) * np.sqrt(sN2) * (1 + 1 / n)
    if print_ratio_captured:
        print("Ratio in prediction interval", np.mean(np.abs(resid + mean_resid) < dy))
    return dy


def powerset(iterable, start=0):
    """ "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    This function comes from the python documentation at https://docs.python.org/3/library/itertools.html"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(start, len(s) + 1))


def train_set_of_models(features, bmw, dependent="log price"):
    models = {}
    for feature_set in powerset(features, start=1):
        linreg_local = Pipeline(
            (("one_hot", make_cat_ohe()), ("regressor", LinearRegression()))
        )
        X = bmw[list(feature_set)]
        y = bmw[dependent]
        linreg_local.fit(X, y)
        dy = calc_prediction_delta(y, linreg_local.predict(X), alpha=0.90)
        models[feature_set] = {"model": linreg_local, "dy_90": dy}
    return models


def find_longest_element(keys):
    return keys[np.argmax(list(map(len, keys)))]


def scalar_to_list(x):
    if np.isscalar(x):
        return [x]
    else:
        return x


def eval_model(models, **kwargs):
    features = find_longest_element(list(models.keys()))
    # print(features)
    for key in kwargs:
        if key not in features:
            raise ValueError(f"{key} not found in {features}")
    chosen_features = tuple(feature for feature in features if feature in kwargs)
    model_holder = models[chosen_features]
    model = model_holder["model"]
    dy = model_holder["dy_90"]

    values = (scalar_to_list(kwargs[feature]) for feature in chosen_features)
    X = pd.DataFrame(
        dict(
            zip(
                chosen_features,
                values,
            )
        )
    )
    price = np.power(10, model.predict(X))
    lower_90 = np.power(10, model.predict(X) - dy)
    upper_90 = np.power(10, model.predict(X) + dy)
    price_w_interval = pd.DataFrame(
        {"price": price, "90% lower bound": lower_90, "90% upper bound": upper_90}
    )

    return price_w_interval


def pretty_print_prediction(prediction):
    print(prediction)
    price = float(prediction["price"])
    low_bound = float(prediction["90% lower bound"])
    upper_bound = float(prediction["90% upper bound"])
    return f"Price: {price:.0f}$, 90% of prices between {low_bound:.0f}$ and {upper_bound:.0f}$"
