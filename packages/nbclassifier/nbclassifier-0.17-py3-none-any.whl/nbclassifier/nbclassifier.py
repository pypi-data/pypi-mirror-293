import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics

def run_nbclassifier(confusion_matrix=None):
    if confusion_matrix is None:
        from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:\n", cm)

    wine = datasets.load_wine()

    print("Features: ", wine.feature_names)
    print("Labels: ", wine.target_names)

    X = pd.DataFrame(wine['data'])

    print(X.head())
    print(wine.data.shape)

    y = wine.target
    print(y)

    X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.30, random_state=109)

    gnb = GaussianNB()

    gnb.fit(X_train, y_train)

    y_pred = gnb.predict(X_test)
    print(y_pred)

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:\n", cm)

if __name__ == "__main__":
    run_nbclassifier()