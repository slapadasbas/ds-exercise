# Code Challenge - DS ML Engineer

You are provided a synthetic dataset for a mobile payments application. In this dataset, you are provided the sender and recipient of a transaction as well as whether transactions are tagged as fraud or not fraud. Your task is to build a fraud detection API that can be called to predict whether or not a transaction is fraudulent.

Access the API:
```curl -XPOST https://exercise-jcb.herokuapp.com/is-fraud -H 'Content-Type:application/json' \
-d {
    "step":1,
    "type":"PAYMENT",
    "amount":9839.64,
    "nameOrig":"C1231006815",
    "oldbalanceOrig":170136.0,
    "newbalanceOrig":160296.36,
    "nameDest":"M1979787155",
    "oldbalanceDest":0.0,
    "newbalanceDest":0.0
}
```