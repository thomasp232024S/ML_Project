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
    df = extract_features(
        "clinical.project-tcga-luad.2026-03-30.json",
        "biospecimen.project-tcga-luad.2026-03-30.json"
    )
    y = df["vital_status"]
    X = df.drop(columns=["vital_status", "case_id"])

    X = imputer.fit_transform(X)

    # binary_cols = [col for col in X.columns if X[col].dropna().nunique() == 2]
    # numeric_cols = [col for col in X.columns if col not in binary_cols]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.25,
        random_state=12
    )

#     preprocessor = ColumnTransformer([("numeric", Pipeline([
#         ("imputer", KNNImputer(n_neighbors=5)),
#         ("scaler", StandardScaler())]), numeric_cols),
#
#     ("binary", Pipeline([
#         ("imputer", KNNImputer(n_neighbors=5))
#     ]), binary_cols)
# ])

    

   

   


    models = {
        "Logistic Regression" : LogisticRegression(
            max_iter=100000
        ),

        "Decision Tree" : DecisionTreeClassifier(
            max_depth=2,
            random_state=12
        ),
        
        "Random Forest" : RandomForestClassifier(
            n_estimators=300,
            random_state=12
        ),

        "SVM" : SVC(kernel='rbf'),

        "KNN" : KNeighborsClassifier(n_neighbors=5)
    }
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.fit_transform(X_test)


    for name, model in models.items():

        if name == "Decision Tree" or name == "Random Forest":
            use_x_train = X_train
            use_x_test = X_test
        else:
            use_x_train = X_train_scaled
            use_x_test = X_test_scaled

        model.fit(use_x_train, y_train)

        predictions = model.predict(use_x_test)

        accuracy = accuracy_score(y_test, predictions)
        try:
            auroc = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
        except:
            print("error")

        print("\n==============")
        print(name)
        print("\n==============")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"AUROC: {auroc:.4f}")
        print(classification_report(y_test,predictions))


        cm = confusion_matrix(y_test, predictions)
        ConfusionMatrixDisplay(cm).plot()
        plt.title(name)
        plt.show()


              


"""TO-DO -
- create model pipeline as showed in class example
- improve model accuracy by feature manipulation
- remove scaling on already binary features
"""

    
