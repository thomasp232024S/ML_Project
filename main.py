import pandas

import import_clinical
from import_clinical import convert_smart

if __name__ == '__main__':
    #df = import_clinical.convert('/home/terif/Downloads/clinical.project-tcga-luad.2026-03-30.json')
    #print(df)
    #df.to_parquet("clinical_full.parquet")
    df = pandas.read_parquet("clinical_full.parquet")

    strs = []
    for column in df.columns.values:
        if column.__contains__("smoking"):
            for row in df[column]:
                if str(row) not in strs:
                    strs.append(str(row))
    #print(strs)
    df = convert_smart(df)
    df.to_parquet("clinical_filtered.parquet")
    df.info()