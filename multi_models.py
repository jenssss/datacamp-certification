from itertools import chain, combinations
import json
from pickle import dump, load

import numpy as np
import pandas as pd
from scipy.stats import t

from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def make_cat_ohe(drop="first"):
    """Make a one hot encoder that only acts on categorical columns"""
    cat_transformer_tuple = (
        OneHotEncoder(drop=drop),
        make_column_selector(dtype_include="category"),
    )
    ohe = make_column_transformer(cat_transformer_tuple, remainder="passthrough")
    return ohe


def calc_prediction_delta(y, y_pred, alpha=0.90, print_ratio_captured=False):
    """Calculates the half width of the prediction interval, in which the
    the fraction of values that fall within this interval is expected to
    be `alpha`.

    If `print_ratio_captured` is true, the ratio of values actually in the
    prediction interval is printed. This should be close to `alpha`.

    """
    n = len(y)
    resid = y - y_pred
    mean_resid = np.mean(y - y_pred)
    sN2 = 1 / (n - 1) * sum((resid - mean_resid) ** 2)
    dy = t.ppf((1 + alpha) / 2, n - 1) * np.sqrt(sN2) * (1 + 1 / n)
    if print_ratio_captured:
        print(
            "Ratio of values inside prediction interval:"
            + " {:.2f}, mean residual {:.2g}".format(
                np.mean(np.abs(resid + mean_resid) < dy), mean_resid
            )
        )
    return dy


def eval_price_with_pred_interval(X, linreg, dy):
    y_predict = linreg.predict(X)
    y_pred_w_interval = pd.DataFrame(
        {"y": y_predict, "y-dy": y_predict - dy, "y+dy": y_predict + dy}
    )
    price = np.power(10, y_pred_w_interval).rename(
        {"y": "price", "y-dy": "lower", "y+dy": "upper"}, axis="columns"
    )
    return price


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
    price = float(prediction["price"])
    low_bound = float(prediction["90% lower bound"])
    upper_bound = float(prediction["90% upper bound"])
    return f"Price: ${price:.0f}, 90% of prices between ${low_bound:.0f} and ${upper_bound:.0f}$"


def extract_feature_ranges(df):
    features_ranges = {}
    for col in df.select_dtypes(include=np.number):
        series = df[col]
        summary = {
            "type": "numeric",
            "range": (float(series.min()), float(series.max())),
        }
        features_ranges[col] = summary
    for col in df.select_dtypes(include="category"):
        series = df[col]
        summary = {"type": "category", "values": list(series.cat.categories)}
        features_ranges[col] = summary
    return features_ranges


def dump_feature_ranges_to_json_file(df, filename="feature_ranges.json"):
    feature_ranges = extract_feature_ranges(df)
    with open(filename, "w") as fil:
        json.dump(feature_ranges, fil)
    return filename


def dump_models(models, model_dump_file="bmw_linreg_model.pckl"):
    with open(model_dump_file, "wb") as file_:
        dump(models, file_)
    return model_dump_file


def load_models(model_dump_file="bmw_linreg_model.pckl"):
    with open(model_dump_file, "rb") as file_:
        models = load(file_)
    return models
