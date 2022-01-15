import pandas as pd
import csv

from flask import current_app as app

def run(json_data):
    """Data Processing pipeline:
        - Convert json payload to pandas Dataframe
        - Get previous transaction based on `nameDest` 
        - Insert new data to data storage

    Args:
        json_data (dict): The input json payload

    Returns:
        pandas.DataFrame: The preprocessed input data
    """
    raw_df = json_to_df(json_data)
    hist_df = get_historical_data(raw_df.loc[0,'nameDest'])
    
    # Ideally this will be handled by SQL 
    raw_id = hist_df.shape[0] + 1
    raw_df['id'] = raw_id
    
    df = pd.concat([raw_df, hist_df])
    df_fe = feature_engineer(df)
    insert_to_db(raw_df)
    return df_fe.query('id == @raw_id')
    

def json_to_df(json_data):
    """Converts the json payload to a pandas dataframe

    Args:
        json_data (dict): The json input from the API

    Returns:
        pandas.DataFrame: The json input converted into a pandas dataframe
    """
    for k,v in json_data.items():
        json_data.update({k:[v]})
        
    raw_df = pd.DataFrame.from_dict(json_data, orient='columns')
    return raw_df


def get_historical_data(name):
    """Loads all the previous transaction of 
    the provided destination account

    Args:
        name (str): recipient ID of the transaction
    
    Returns:
        pandas.DataFrame: All the previous transaction 
            of the provided destination account
    """
    #Ideally, use a database for this process
    old = pd.read_csv(app.config["DB"])
    hist = old.query("nameDest == @name")
    return hist
    
    
def feature_engineer(df):
    """Feature engineering pipeline:
        - Add `nthTransactionForTheHour` column
        - Compute cumulative amount for the hour

    Args:
        df (pandas.DataFrame): A raw dataframe input

    Returns:
        pandas.DataFrame: The feature engineered dataframe
    """
    df = df.sort_values('id')
    
    df["nthTransactionForTheHour"] = df.groupby(["nameDest", "step"])['step'].rank(method='first')
    df['cumsum'] = df.groupby(['nameDest', 'step'])['amount'].transform('cumsum')
    return df


def insert_to_db(df):
    """Inserts the input data to the data storage

    Args:
        df (pandas.DataFrame): The input data
    """
    
    DB_COLS = ["id",
               "step",
               "type",
               "amount",
               "nameOrig",
               "oldbalanceOrig",
               "newbalanceOrig",
               "nameDest",
               "oldbalanceDest",
               "newbalanceDest"]
    
    with open(app.config["DB"], 'a', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(df.loc[0, DB_COLS].tolist())
    
    