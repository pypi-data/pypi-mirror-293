import numpy as np
import pandas as pd
from sklearn import datasets

wine = datasets.load_wine()

print("Features: ", wine.feature_names)
print("Labels: ", wine.target_names)

X = pd.DataFrame(wine['data'])

print(X.head())
print(wine.data.shape)

y = wine.target
print(y)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.30, random_state=109)

from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()

gnb.fit(X_train, y_train)

y_pred = gnb.predict(X_test)
print(y_pred)

from sklearn import metrics

print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

from sklearn.metrics import confusion_matrix

cm = np.array(confusion_matrix(y_test, y_pred))
print("Confusion Matrix:\n", cm)