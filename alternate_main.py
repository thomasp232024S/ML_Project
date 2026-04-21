import pandas as pd
from pandas import DataFrame
from alternate_feature_extract import extract_features

if __name__ == "__main__":
    
    df = extract_features("clinical_cases.json")
    #print(df.iloc[:30, :30])
    print(df[["age_at_index", "pack_years_smoked"]])
    print("---------------------------\n\n")
    df.info()

    
