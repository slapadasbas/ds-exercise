class Config:
    DEBUG = False
    DB = "input/transactions.csv"
    
    MODEL_RF = "model/rf_baseline20220115.pkl" 
    PROBA_TRESHOLD = 0.25
    
    SIGVARS = [
        'oldbalanceOrig', 
        'newbalanceOrig',
        'oldbalanceDest',
        'newbalanceDest',
        'cumsum',
        'nthTransactionForTheHour'
    ]


class DevConfig(Config):
    DEBUG = True
    
class ProdConfig(Config):
    DEBUG = False