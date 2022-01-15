import pandas as pd
import pickle
import eli5

from flask import current_app as app


def run(df):
    """Modelling pipeline:
        - Load the machine learning model
        - Predict

    Args:
        df (pd.DataFrame): Pre-processed input data

    Returns:
        int: The prediction
            - 1 if fraudulent
            - 0 if non-fraudulent
    """
    model = load_model()
    prediction = predict(model, df)
    explain(model, df)
    return prediction
    
    
def load_model():
    """Loads the machine learning model through pickle

    Returns:
        object: The machine learning model
    """
    return pickle.load(open(app.config["MODEL_RF"], 'rb'))
    
    
def predict(model, data):
    """Predicts whether the pre-processed data is fraudulent or not.
    Uses a probability cut-off.

    Args:
        model (object): The machine learning model
        data (pandas.DataFrame): The pre-processed data

    Returns:
        int: The prediction
            - 1 if fraudulent
            - 0 if non-fraudulent
    """

    raw_probability = model.predict_proba(data[app.config["SIGVARS"]])[0][1]
    prediction = 1 if raw_probability > app.config["PROBA_TRESHOLD"] else 0
    return prediction
    
    
def explain(model, data):
    explanation = eli5.explain_prediction(model, data[app.config["SIGVARS"]], feature_names=app.config["SIGVARS"])
    print(eli5.format_as_text(explanation))