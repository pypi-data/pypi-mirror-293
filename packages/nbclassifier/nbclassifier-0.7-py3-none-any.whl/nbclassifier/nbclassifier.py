import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.metrics import confusion_matrix

def run_nbclassifier():
    cm = metrics.confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:\n", cm)
    wine = datasets.load_wine()
    X = pd.DataFrame(wine['data'])
    y = wine.target

    X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.30, random_state=109)

    gnb = GaussianNB()
    gnb.fit(X_train, y_train)
    y_pred = gnb.predict(X_test)

    print("Features: ", wine.feature_names)
    print("Labels: ", wine.target_names)
    print(X.head())
    print(wine.data.shape)
    print("Predicted Labels: ", y_pred)
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

if __name__ == "__main__":
    run_nbclassifier()