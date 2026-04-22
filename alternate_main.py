import pandas as pd
from pandas import DataFrame
from alternate_feature_extract import extract_features
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import numpy as np

#initialize scaler and imputer
scaler = StandardScaler()
imputer = SimpleImputer(strategy="median")



if __name__ == "__main__":
    
    df = extract_features("clinical_cases.json")

    # logistic regression model
    y = df["vital_status"]
    X = df.drop(columns=["vital_status", "case_id"])

   
    # now define datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # impute all nan for logistic regression based on median of training data
    imputer.fit(X_train)
    X_train = imputer.transform(X_train)
    X_test = imputer.transform(X_test)


    # now do the same but with scaling
    X_train_std = scaler.fit_transform(X_train)
    X_test_std = scaler.transform(X_test)

    # fit model and make predictions
    model = LogisticRegression()
    model.fit(X_train_std, y_train)

    prediction = model.predict(X_test_std)

    accuracy = accuracy_score(y_test, prediction)
    report = classification_report(y_test, prediction)
    cm = confusion_matrix(y_test, prediction)
    ConfusionMatrixDisplay(cm).plot()
    plt.show()

    print(f"Accuracy: {accuracy}")
    print(f"Classification Report: {report}")

"""TO-DO -
- create model pipeline as showed in class example
- improve model accuracy by feature manipulation
- remove scaling on already binary features
"""

    
