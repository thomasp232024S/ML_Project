import pandas as pd
from pandas import DataFrame
from feature_extract import extract_features
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, confusion_matrix
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

df = extract_features(
    "clinical.project-tcga-luad.2026-03-30.json",
    "biospecimen.project-tcga-luad.2026-03-30.json"
)

if __name__ == "__main__":
    
    y = df["vital_status"]
    X = df.drop(columns=["vital_status", "case_id"])

    binary_cols = [col for col in X.columns if X[col].dropna().nunique() == 2]
    numeric_cols = [col for col in X.columns if col not in binary_cols]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.25,
        random_state=12,
        stratify=y
    )

    preprocessor = ColumnTransformer([("numeric", Pipeline([
        ("imputer", KNNImputer(n_neighbors=5)),
        ("scaler", StandardScaler())]), numeric_cols),

    ("binary", Pipeline([
        ("imputer", KNNImputer(n_neighbors=5))
    ]), binary_cols)
])

    

   

   


    models = {
        "Logistic Regression" : LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        ),

        "Decision Tree" : DecisionTreeClassifier(
            max_depth=5,
            random_state=12
        ),
        
        "Random Forest" : RandomForestClassifier(
            n_estimators=100,
            random_state=12
        ),

        "SVM" : SVC(kernel='rbf',probability = True),

        "KNN" : KNeighborsClassifier(n_neighbors=5)
    }

    for name, model in models.items():


        pipeline = Pipeline([("preprocessor", preprocessor),("model", model)])
        


        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)

        print("\n==============")
        print(name)
        print("\n==============")
        print(f"Accuracy: {accuracy:.4f}")
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

    
