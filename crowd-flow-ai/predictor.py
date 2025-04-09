# predictor.py
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def predict_crowd(history, future_steps=5, degree=2):
    if len(history) < 2:
        return [history[-1]] * future_steps
    
    X = np.arange(len(history)).reshape(-1, 1)
    y = np.array(history)
    
    poly = PolynomialFeatures(degree)
    X_poly = poly.fit_transform(X)
    
    model = LinearRegression().fit(X_poly, y)
    
    future_X = np.arange(len(history), len(history) + future_steps).reshape(-1, 1)
    future_X_poly = poly.transform(future_X)
    predictions = model.predict(future_X_poly)
    
    return predictions.round(2).tolist()
