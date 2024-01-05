import pandas as pd
import joblib


def prediction_prob(data):

    model = joblib.load("app/promise_model.joblib")
    return(model.predict_proba(data))


