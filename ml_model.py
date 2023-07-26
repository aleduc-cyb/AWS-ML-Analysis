from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib
import os
import config

config_object = config.config_object

def main(df, train_model=False):   
    # Format data
    X = df.values

    # Preprocess and get/train model
    if train_model:
        X = preprocess_fit(X)
        clf = model_fit(X)
    else:
        X = preprocess_transform(X)
        clf = model_get_from_file()

    # Predict results
    scores_pred, anomalies_pred = predict_score(clf, X)

    # Get threshold
    threshold = get_threshold(scores_pred)

    # Get anomalies
    anomalies = get_anomalies(df, scores_pred, threshold)
    
    return scores_pred, anomalies_pred, anomalies

def preprocess_fit(X):
    # Preprocess the data by standardizing it
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    joblib.dump(scaler, os.path.join('Out', 'Model', 'scaler.joblib'))
    return X

def preprocess_transform(X):
    scaler = joblib.load(os.path.join('Out', 'Model', 'scaler.joblib'))
    X = scaler.transform(X)
    return X

def model_fit(X):
    # Apply the Isolation Forest algorithm
    clf = IsolationForest(n_estimators=100, max_samples='auto', contamination=float(0.1), random_state=np.random.RandomState(42))
    clf.fit(X)
    joblib.dump(clf, os.path.join('Out', 'Model', 'clf.joblib'))
    return clf

def model_get_from_file():
    clf = joblib.load(os.path.join('Out', 'Model', 'clf.joblib'))
    return clf

def predict_score(clf, X):
    # Predict the anomaly scores for each sample
    scores_pred = clf.decision_function(X)
    anomalies_pred = clf.predict(X)
    return scores_pred, anomalies_pred

def get_threshold(scores_pred):
    #threshold = np.percentile(scores_pred, 1)  # top 1% of lowest scores
    #threshold = np.min(scores_pred)
    k = int(config_object['ML']['topanomalies'])
    threshold = np.partition(scores_pred, k - 1)[k - 1]
    return threshold

def get_anomalies(df, scores_pred, threshold):
    # Identify the anomalies
    anomalies = df[scores_pred <= threshold]
    anomalies.to_csv(os.path.join('Out', 'Data', 'anomalies.csv'))
    return anomalies