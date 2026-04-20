from math import isnan

import pandas as pd
from pandas import DataFrame


def convert_smart(df_complex : DataFrame) -> DataFrame:
    dfs = []
    for index, row in df_complex.iterrows():
        df = {}
        rowlist = row.dropna().to_list()
        #rowstr = str(rowlist)
        if rowlist.__contains__("not hispanic or latino"):
            df["latino"] = 1
        else:
            df["latino"] = 0
        if rowlist.__contains__("female"):
            df["gender"] = 1
        else:
            df["gender"] = 0
        if rowlist.__contains__("white"):
            df["race"] = 1
        elif rowlist.__contains__("black"):
            df["race"] = 2
        else:
            df["race"] = 0
        if rowlist.__contains__("Alive"):
            df["Surviving"] = 1
        else:
            df["Surviving"] = 0
        if rowlist.__contains__("Chemotherapy"):
            df["Chemotherapy"] = 1
        else:
            df["Chemotherapy"] = 0
        if rowlist.__contains__("Gemcitabine"):
            if rowlist[rowlist.index("Gemcitabine") - 2] == "Complete Response":
                df["Gemcitabine"] = 2
            else:
                df["Gemcitabine"] = 1
        else:
            df["Gemcitabine"] = 0
        if rowlist.__contains__("Vinorelbine"):
            if rowlist[rowlist.index("Vinorelbine") - 2] == "Complete Response":
                df["Vinorelbine"] = 2
            else:
                df["Vinorelbine"] = 1
        else:
            df["Vinorelbine"] = 0
        if rowlist.__contains__("Cisplatin"):
            if rowlist[rowlist.index("Cisplatin") - 2] == "Complete Response":
                df["Cisplatin"] = 2
            else:
                df["Cisplatin"] = 1
        else:
            df["Cisplatin"] = 0
        if rowlist.__contains__("Docetaxel"):
            if rowlist[rowlist.index("Docetaxel") - 2] == "Complete Response":
                df["Docetaxel"] = 2
            else:
                df["Docetaxel"] = 1
        else:
            df["Docetaxel"] = 0
        if rowlist.__contains__("Carboplatin"):
            if rowlist[rowlist.index("Carboplatin") - 2] == "Complete Response":
                df["Carboplatin"] = 2
            else:
                df["Carboplatin"] = 1
        else:
            df["Carboplatin"] = 0
        if rowlist.__contains__("Erlotinib Hydrochloride"):
            if rowlist[rowlist.index("Erlotinib Hydrochloride") - 2] == "Complete Response":
                df["Erlotinib Hydrochloride"] = 2
            else:
                df["Erlotinib Hydrochloride"] = 1
        else:
            df["Erlotinib Hydrochloride"] = 0
        if rowlist.__contains__("Pemetrexed"):
            if rowlist[rowlist.index("Pemetrexed") - 2] == "Complete Response":
                df["Pemetrexed"] = 2
            else:
                df["Pemetrexed"] = 1
        else:
            df["Pemetrexed"] = 0
        if rowlist.__contains__("Pemetrexed Disodium"):
            if rowlist[rowlist.index("Pemetrexed Disodium") - 2] == "Complete Response":
                df["Pemetrexed Disodium"] = 2
            else:
                df["Pemetrexed Disodium"] = 1
        else:
            df["Pemetrexed Disodium"] = 0
        if rowlist.__contains__("Paclitaxel"):
            if rowlist[rowlist.index("Paclitaxel") - 2] == "Complete Response":
                df["Paclitaxel"] = 2
            else:
                df["Paclitaxel"] = 1
        else:
            df["Paclitaxel"] = 0
        if rowlist.__contains__("Etoposide"):
            if rowlist[rowlist.index("Etoposide") - 2] == "Complete Response":
                df["Etoposide"] = 2
            else:
                df["Etoposide"] = 1
        else:
            df["Etoposide"] = 0
        if rowlist.__contains__("Cyclophosphamide"):
            if rowlist[rowlist.index("Cyclophosphamide") - 2] == "Complete Response":
                df["Cyclophosphamide"] = 2
            else:
                df["Cyclophosphamide"] = 1
        else:
            df["Cyclophosphamide"] = 0
        if rowlist.__contains__("Erlotinib"):
            if rowlist[rowlist.index("Erlotinib") - 2] == "Complete Response":
                df["Erlotinib"] = 2
            else:
                df["Erlotinib"] = 1
        else:
            df["Erlotinib"] = 0
        if rowlist.__contains__("Vinorelbine Tartrate"):
            if rowlist[rowlist.index("Vinorelbine Tartrate") - 2] == "Complete Response":
                df["Vinorelbine Tartrate"] = 2
            else:
                df["Vinorelbine Tartrate"] = 1
        else:
            df["Vinorelbine Tartrate"] = 0
        if rowlist.__contains__("Gemcitabine Hydrochloride"):
            if rowlist[rowlist.index("Gemcitabine Hydrochloride") - 2] == "Complete Response":
                df["Gemcitabine Hydrochloride"] = 2
            else:
                df["Gemcitabine Hydrochloride"] = 1
        else:
            df["Gemcitabine Hydrochloride"] = 0
        if rowlist.__contains__("Bevacizumab"):
            if rowlist[rowlist.index("Bevacizumab") - 2] == "Complete Response":
                df["Bevacizumab"] = 2
            else:
                df["Bevacizumab"] = 1
        else:
            df["Bevacizumab"] = 0
        if rowlist.__contains__("Belinostat"):
            if rowlist[rowlist.index("Belinostat") - 2] == "Complete Response":
                df["Belinostat"] = 2
            else:
                df["Belinostat"] = 1
        else:
            df["Belinostat"] = 0
        if rowlist.__contains__("Recombinant PRAME Protein Plus AS15 Adjuvant GSK2302025A"):
            if rowlist[rowlist.index("Recombinant PRAME Protein Plus AS15 Adjuvant GSK2302025A") - 2] == "Complete Response":
                df["Recombinant PRAME Protein Plus AS15 Adjuvant GSK2302025A"] = 2
            else:
                df["Recombinant PRAME Protein Plus AS15 Adjuvant GSK2302025A"] = 1
        else:
            df["Recombinant PRAME Protein Plus AS15 Adjuvant GSK2302025A"] = 0
        if rowlist.__contains__("Vinblastine"):
            if rowlist[rowlist.index("Vinblastine") - 2] == "Complete Response":
                df["Vinblastine"] = 2
            else:
                df["Vinblastine"] = 1
        else:
            df["Vinblastine"] = 0
        if rowlist.__contains__("Anastrozole"):
            if rowlist[rowlist.index("Anastrozole") - 2] == "Complete Response":
                df["Anastrozole"] = 2
            else:
                df["Anastrozole"] = 1
        else:
            df["Anastrozole"] = 0
        if rowlist.__contains__("Gefitinib"):
            if rowlist[rowlist.index("Gefitinib") - 2] == "Complete Response":
                df["Gefitinib"] = 2
            else:
                df["Gefitinib"] = 1
        else:
            df["Gefitinib"] = 0
        if rowlist.__contains__("Tyrosine Kinase Inhibitor"):
            if rowlist[rowlist.index("Tyrosine Kinase Inhibitor") - 2] == "Complete Response":
                df["Tyrosine Kinase Inhibitor"] = 2
            else:
                df["Tyrosine Kinase Inhibitor"] = 1
        else:
            df["Tyrosine Kinase Inhibitor"] = 0
        if rowlist.__contains__("Zoledronic Acid"):
            if rowlist[rowlist.index("Zoledronic Acid") - 2] == "Complete Response":
                df["Zoledronic Acid"] = 2
            else:
                df["Zoledronic Acid"] = 1
        else:
            df["Zoledronic Acid"] = 0
        if rowlist.__contains__("Clinical Trial"):
            if rowlist[rowlist.index("Clinical Trial") - 2] == "Complete Response":
                df["Clinical Trial"] = 2
            else:
                df["Clinical Trial"] = 1
        else:
            df["Clinical Trial"] = 0
        if rowlist.__contains__("Letrozole"):
            if rowlist[rowlist.index("Letrozole") - 2] == "Complete Response":
                df["Letrozole"] = 2
            else:
                df["Letrozole"] = 1
        else:
            df["Letrozole"] = 0
        if rowlist.__contains__("Cyanocobalamin"):
            if rowlist[rowlist.index("Cyanocobalamin") - 2] == "Complete Response":
                df["Cyanocobalamin"] = 2
            else:
                df["Cyanocobalamin"] = 1
        else:
            df["Cyanocobalamin"] = 0
        if rowlist.__contains__("Octreotide Acetate"):
            if rowlist[rowlist.index("Octreotide Acetate") - 2] == "Complete Response":
                df["Octreotide Acetate"] = 2
            else:
                df["Octreotide Acetate"] = 1
        else:
            df["Octreotide Acetate"] = 0
        if rowlist.__contains__("Denosumab"):
            if rowlist[rowlist.index("Denosumab") - 2] == "Complete Response":
                df["Denosumab"] = 2
            else:
                df["Denosumab"] = 1
        else:
            df["Denosumab"] = 0
        if rowlist.__contains__("Pegfilgrastim"):
            if rowlist[rowlist.index("Pegfilgrastim") - 2] == "Complete Response":
                df["Pegfilgrastim"] = 2
            else:
                df["Pegfilgrastim"] = 1
        else:
            df["Pegfilgrastim"] = 0
        if rowlist.__contains__("Topotecan"):
            if rowlist[rowlist.index("Topotecan") - 2] == "Complete Response":
                df["Topotecan"] = 2
            else:
                df["Topotecan"] = 1
        else:
            df["Topotecan"] = 0
        if rowlist.__contains__("Irinotecan Hydrochloride"):
            if rowlist[rowlist.index("Irinotecan Hydrochloride") - 2] == "Complete Response":
                df["Irinotecan Hydrochloride"] = 2
            else:
                df["Irinotecan Hydrochloride"] = 1
        else:
            df["Irinotecan Hydrochloride"] = 0
        if rowlist.__contains__("Nab-paclitaxel"):
            if rowlist[rowlist.index("Nab-paclitaxel") - 2] == "Complete Response":
                df["Nab-paclitaxel"] = 2
            else:
                df["Nab-paclitaxel"] = 1
        else:
            df["Nab-paclitaxel"] = 0
        if rowlist.__contains__("Irinotecan"):
            if rowlist[rowlist.index("Irinotecan") - 2] == "Complete Response":
                df["Irinotecan"] = 2
            else:
                df["Irinotecan"] = 1
        else:
            df["Irinotecan"] = 0
        if rowlist.__contains__("Aurora Kinase/VEGFR2 Inhibitor CYC116"):
            if rowlist[rowlist.index("Aurora Kinase/VEGFR2 Inhibitor CYC116") - 2] == "Complete Response":
                df["Aurora Kinase/VEGFR2 Inhibitor CYC116"] = 2
            else:
                df["Aurora Kinase/VEGFR2 Inhibitor CYC116"] = 1
        else:
            df["Aurora Kinase/VEGFR2 Inhibitor CYC116"] = 0
        if rowlist.__contains__("Germany"):
            df["Country"] = 1
        elif rowlist.__contains__("United States"):
            df["Country"] = 2
        elif rowlist.__contains__("Australia"):
            df["Country"] = 3
        elif rowlist.__contains__("Ukraine"):
            df["Country"] = 4
        elif rowlist.__contains__("Russia"):
            df["Country"] = 5
        elif rowlist.__contains__("Canada"):
            df["Country"] = 6
        elif rowlist.__contains__("Vietnam"):
            df["Country"] = 7
        elif rowlist.__contains__("Romania"):
            df["Country"] = 8
        else:
            df["Country"] = 0
        if rowlist.__contains__("Peripheral Lung"):
            df["Primary_Site"] = 1
        elif rowlist.__contains__("Central Lung"):
            df["Primary_Site"] = 2
        elif rowlist.__contains__("Lung, NOS"):
            df["Primary_Site"] = 3
        elif rowlist.__contains__("Bronchus and lung"):
            df["Primary_Site"] = 4
        elif rowlist.__contains__("Body, total"):
            df["Primary_Site"] = 5
        elif rowlist.__contains__("Primary Tumor Field"):
            df["Primary_Site"] = 6
        elif rowlist.__contains__("Distant Site"):
            df["Primary_Site"] = 7
        elif rowlist.__contains__("Locoregional Site"):
            df["Primary_Site"] = 8
        elif rowlist.__contains__("Regional Site"):
            df["Primary_Site"] = 9
        elif rowlist.__contains__("Thyroid"):
            df["Primary_Site"] = 10
        elif rowlist.__contains__("Skin"):
            df["Primary_Site"] = 11
        elif rowlist.__contains__("Lung"):
            df["Primary_Site"] = 12
        elif rowlist.__contains__("Breast"):
            df["Primary_Site"] = 13
        elif rowlist.__contains__("Colon"):
            df["Primary_Site"] = 14
        elif rowlist.__contains__("Vulva"):
            df["Primary_Site"] = 15
        elif rowlist.__contains__("Floor of Mouth"):
            df["Primary_Site"] = 16
        elif rowlist.__contains__("Vagina"):
            df["Primary_Site"] = 17
        elif rowlist.__contains__("Tongue"):
            df["Primary_Site"] = 18
        else:
            df["Primary_Site"] = 0
        if rowlist.__contains__("Lifelong Non-Smoker"):
            df["Smoking"] = 1
        elif rowlist.__contains__("Current Reformed Smoker for > 15 yrs"):
            df["Smoking"] = 2
        elif rowlist.__contains__("Current Reformed Smoker for < or = 15 yrs"):
            df["Smoking"] = 3
        elif rowlist.__contains__("Current Reformed Smoker, Duration Not Specified"):
            df["Smoking"] = 4
        elif rowlist.__contains__("Current Smoker"):
            df["Smoking"] = 5
        else:
            df["Smoking"] = 0

        df["case_id"] = row["case_id"]
        df["age_at_diagnosis"] = row["demographic_age_at_index"]
        #if we don't even have age data, this should probably indicate the data
        #for this case is so incomplete as to be useless
        if isnan(df["age_at_diagnosis"]):
            continue
        
        dfs.append(df)
    df_full = []
    for f in dfs:
        df_full.append(DataFrame(f, index=[0]))
    df = pd.concat(df_full, ignore_index=True)
    return df

def convert(file : str):
    df_bad = convert_stupid(file)
    dfs = []
    #this is probably a really inefficient way to do this
    for index, row in df_bad.iterrows():
        df = DataFrame(row).transpose()
        df_sub = []
        if "project" in df.columns and df["project"].first_valid_index() is not None:
            df_project = DataFrame(df["project"][df["project"].first_valid_index()], index=[0])
            df_project.columns = df_project.columns.to_series().apply(prefix_str_project)
            df_sub.append(df_project)
            df = df.drop(columns=["project"])
        if "demographic" in df.columns and df["demographic"].first_valid_index() is not None:
            df_demographic = DataFrame(df["demographic"][df["demographic"].first_valid_index()], index=[0])
            df_demographic.columns = df_demographic.columns.to_series().apply(prefix_str_project)
            df_demographic.columns = df_demographic.columns.str.replace("project_", "demographic_")
            df_sub.append(df_demographic)
            df = df.drop(columns=["demographic"])
        if "diagnoses" in df.columns and df["diagnoses"].first_valid_index() is not None:
            i=0
            for diagnosis in row["diagnoses"]:
                #df_diagnosis = DataFrame(diagnosis)
                df_diagnosis_sub = []
                df_diagnosis_drop = []
                if "treatments" in diagnosis:
                    j = 0
                    for treatment in list(diagnosis["treatments"]):
                        if "treatment_anatomic_sites" in treatment and isinstance(treatment["treatment_anatomic_sites"], list) and treatment["treatment_anatomic_sites"].__len__() > 1:
                            k = 0
                            df_sites = {}
                            for site in list(treatment["treatment_anatomic_sites"]):
                                df_sites[f"treatment_{j}_treatment_anatomic_sites_{k}"] = site
                                k += 1
                            df_sites = DataFrame(df_sites, index=[0])
                            df_diagnosis_sub.append(df_sites)
                            treatment.pop("treatment_anatomic_sites")
                        df_treatment = DataFrame(dict(treatment), index=[0])
                        df_treatment.columns = df_treatment.columns.to_series().apply(prefix_str_project)
                        df_treatment.columns = df_treatment.columns.str.replace("project_", f"treatment_{j}_")
                        df_diagnosis_sub.append(df_treatment)
                        j+=1
                    df_diagnosis_drop.append("treatments")
                if diagnosis.__contains__("pathology_details"):
                    j = 0
                    for pathology in list(diagnosis["pathology_details"]):
                        df_pathology = DataFrame(dict(pathology), index=[0])
                        df_pathology.columns = df_pathology.columns.to_series().apply(prefix_str_project)
                        df_pathology.columns = df_pathology.columns.str.replace("project_", f"pathology_{j}_")
                        df_diagnosis_sub.append(df_pathology)
                        j+=1
                    df_diagnosis_drop.append("pathology_details")
                if diagnosis.__contains__("sites_of_involvement"):
                    j=0
                    df_site = {}
                    for site in list(diagnosis["sites_of_involvement"]):
                        df_site[f"site_{j}_of_involvement"] = site
                        j+=1
                    df_site = DataFrame(df_site, index=[0])
                    df_diagnosis_drop.append("sites_of_involvement")
                    df_diagnosis_sub.append(df_site)
                for key in df_diagnosis_drop:
                    diagnosis.pop(key)
                df_diagnosis = DataFrame(diagnosis, index=[0])
                df_diagnosis_sub.append(df_diagnosis)
                df_diagnosis = pd.concat(df_diagnosis_sub, axis=1)
                df_diagnosis.columns = df_diagnosis.columns.to_series().apply(prefix_str_project)
                df_diagnosis.columns = df_diagnosis.columns.str.replace("project_", f"diagnosis_{i}_")
                df_sub.append(df_diagnosis)
                i += 1
            df = df.drop(columns=["diagnoses"])
        if "exposures" in df.columns and df["exposures"].first_valid_index() is not None:
            i = 0
            for exposure in df["exposures"][df["exposures"].first_valid_index()]:
                df_exposure = DataFrame(exposure, index=[0])
                df_exposure.columns = df_exposure.columns.to_series().apply(prefix_str_project)
                df_exposure.columns = df_exposure.columns.str.replace("project_", f"exposure_{i}_")
                df_sub.append(df_exposure)
                i+=1
            df = df.drop(columns=["exposures"])
        if "follow_ups" in df.columns and df["follow_ups"].first_valid_index() is not None:
            i = 0
            for follow_up in list(df["follow_ups"][df["follow_ups"].first_valid_index()]):
                df_follow_up = DataFrame(dict(follow_up), index=[0])
                df_follow_up.columns = df_follow_up.columns.to_series().apply(prefix_str_project)
                df_follow_up.columns = df_follow_up.columns.str.replace("project_", f"follow_up_{i}_")
                df_sub.append(df_follow_up)
                i+=1
            df = df.drop(columns=["follow_ups"])
        df_sub.append(df)
        df_final = {}
        for dframe in df_sub:
            df_final = df_final | dframe.to_dict(orient="list")
        dfs.append(DataFrame(df_final, index=[0]))
    return pd.concat(dfs, ignore_index=True)

def prefix_str_project(x):
    return "project_" + x


def convert_stupid(file : str):
    return pd.read_json(file)