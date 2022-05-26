# import libraries
import pandas as pd
import numpy as np

import pickle
import random

from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# read the data from the csv
data = pd.read_csv('data.csv', error_bad_lines=False)
data.dropna(inplace=True)

# randomly shuffle
password_tuple = np.array(data)
random.shuffle(password_tuple)

# get the x and y values
x = [labels[0] for labels in password_tuple]
y = [labels[1] for labels in password_tuple]

# tokenizer
def tokenization(word):
    tokens = []
    for ch in word:
        tokens.append(ch)
    return tokens

# vectorize the data
vectorizer = TfidfVectorizer(tokenizer=tokenization)
X = vectorizer.fit_transform(x)

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# fit the model
rfc = RandomForestClassifier(criterion='entropy', random_state=123)
rfc.fit(X_train, y_train)

# predict with the model
y_pred = rfc.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_pred)
print("accuracy: " + str(round(accuracy * 100, 2)) + '%')

# test prediction
predict_data = np.array(['hellothere!'])
prediction = vectorizer.transform(predict_data)
rfc.predict(prediction)

# pickle the models
file = 'vectorizer.pkl'
pickle.dump(vectorizer, open(file, 'wb'))
file = 'rfc.pkl'
pickle.dump(rfc, open(file, 'wb'))