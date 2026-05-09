import pandas as pd
from pandas import DataFrame
from feature_extract import extract_features
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, confusion_matrix, \
    roc_auc_score
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, IterativeImputer, KNNImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.compose import ColumnTransformer
import matplotlib.pyplot as plt
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

#initialize scaler and imputer
scaler = StandardScaler()
imputer = KNNImputer(n_neighbors=5, weights="uniform")



if __name__ == "__main__":
    
    df = extract_features("clinical.project-tcga-luad.2026-03-30.json", "biospecimen.project-tcga-luad.2026-03-30.json")

    y = df["vital_status"]
    X = df.drop(columns=["vital_status", "case_id"])

    # impute on everything before splitting
    #imputer.fit(X)
    X = imputer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=12)

    # fit scaler
    X_train_std = scaler.fit_transform(X_train)
    X_test_std = scaler.fit_transform(X_test)

    pipe_lr = Pipeline([("model", LogisticRegression())])
    pipe_svm = Pipeline([("model", SVC(probability=True))])
    pipe_knn = Pipeline([("model", KNeighborsClassifier())])
    pipe_dt = Pipeline([("model", DecisionTreeClassifier(max_depth=2))])
    pipe_rf = Pipeline([("model", RandomForestClassifier(n_estimators=300))])

    def evaluate(pipe, name, X_tr, X_te):
        pipe.fit(X_tr, y_train)
        predictions = pipe.predict(X_te)
        accuracy = accuracy_score(y_test, predictions)
        auroc = roc_auc_score(y_test, pipe.predict_proba(X_te)[:,1])

        print(f"\n==============")
        print(f"{name}")
        print(f"==============")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"AUROC: {auroc:.4f}")
        print(classification_report(y_test,predictions))


        cm = confusion_matrix(y_test, predictions)
        ConfusionMatrixDisplay(cm).plot()
        plt.title(name)
        plt.show()

    # scaled models
    evaluate(pipe_lr, "Logistic Regression", X_train_std, X_test_std)
    evaluate(pipe_svm, "SVM", X_train_std, X_test_std)
    evaluate(pipe_knn, "KNN", X_train_std, X_test_std)

    # tree models don't need scaling
    evaluate(pipe_dt, "Decision Tree", X_train, X_test)
    evaluate(pipe_rf, "Random Forest", X_train, X_test)