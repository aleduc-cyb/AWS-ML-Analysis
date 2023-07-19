from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import features_extractor as fe
import joblib
import pandas as pd

def main():
    # Get the data (select one)
    #df = get_data_online()
    df = get_data_from_file()
    
    # Format data
    excluded_users = fe.users_exclusion_list()
    df = df[~df['username'].isin(excluded_users)]
    df = df.drop('username', axis=1)

    X = df.values

    # Preprocessing data (select one)
    #X = preprocess_fit(X)
    X = preprocess_transform(X)

    # Model data (select one)
    #clf = model_fit(X)
    clf = model_get_from_file()

    # Predict results
    scores_pred = predict_score(clf, X)

    # Get threshold
    threshold = get_threshold(scores_pred)

    # Get anomalies
    anomalies = get_anomalies(df, scores_pred, threshold)
    anomalies = anomalies

def get_data_online():
    df = fe.main()
    df.to_csv('Save\data.csv')
    return df

def get_data_from_file():
    df = pd.read_csv('Save\data.csv', index_col=0)
    return df

def preprocess_fit(X):
    # Preprocess the data by standardizing it
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    joblib.dump(scaler, 'Save\scaler.joblib')
    return X

def preprocess_transform(X):
    scaler = joblib.load('Save\scaler.joblib')
    X = scaler.transform(X)
    return X

def model_fit(X):
    # Apply the Isolation Forest algorithm
    clf = IsolationForest(n_estimators=100, max_samples='auto', contamination=float(0.1), random_state=np.random.RandomState(42))
    clf.fit(X)
    joblib.dump(clf, 'Save\clf.joblib')
    return clf

def model_get_from_file():
    clf = joblib.load('Save\clf.joblib')
    return clf

def predict_score(clf, X):
    # Predict the anomaly scores for each sample
    scores_pred = clf.decision_function(X)
    return scores_pred

def get_threshold(scores_pred):
    threshold = np.percentile(scores_pred, 1)  # top 1% of lowest scores
    threshold = np.min(scores_pred)
    k = 100
    threshold = np.partition(scores_pred, k - 1)[k - 1]
    return threshold

def get_anomalies(df, scores_pred, threshold):
    # Identify the anomalies
    anomalies = df[scores_pred <= threshold]
    anomalies.to_csv('anomalies.csv')
    return anomalies

if __name__ == "__main__":
    main()