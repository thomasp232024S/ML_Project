import pandas as pd
from pandas import DataFrame
import json
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import numpy as np

scaler = StandardScaler()
imputer = SimpleImputer()


""" temporary function to feature extract ajcc tumor stages
final dataframes will be merged together

* REMINDER TO SELF - NORMALIZE CONTINUOUS FEATURES AFTER INITIAL
DF ENCODING

"""
def extract_features(file : str) -> DataFrame:
    with open(file, 'r') as f:
        cases = json.load(f) #this converts the json object into python dict
    
    # list to be converted to DF
    rows = []

    
    
    
    # iterate through cases
    for case in cases:
        row = {}
        
        # first extract demographic features
        demo = case.get("demographic") or {} # {} is just empty dict in case there is no demographic block
        # extract races
        race = demo.get("race")
        row["is_white"] = (1 if race == "white" else 0) if race and race.lower() != "not reported" else pd.NA
        row["is_black"] = (1 if race == "black or african american" else 0) if race and race.lower() != "not reported" else pd.NA

        # extract gender
        gender = demo.get("gender")
        row["gender"] = (1 if gender == "male" else 0) if gender and gender.lower() != "not reported" else pd.NA
        
        # days to death (normalize this as well)
        days_death = demo.get("days_to_death", pd.NA)
        row["days_to_death"] = days_death
        
        
        # vital status
        surviving = demo.get("vital_status")
        row["vital_status"] = 0 if surviving and surviving == "Alive" else 1 

        # age at index - REMEMBER TO NORMALIZE AFTER
        age = demo.get("age_at_index")
        row["age_at_index"] = age

        # Country (remember nominal)
        country = demo.get("country_of_residence_at_enrollment")
        if not country:
            row["country"] = pd.NA

        row["is_american"] = 1 if country == "United States" else 0
        row["is_canadian"] = 1 if country == "Canada" else 0
        row["is_russian"] = 1 if country == "Russia" else 0
        row["is_australian"] = 1 if country == "Australia" else 0
        row["is_german"] = 1 if country == "Germany" else 0


        # latino / ethnicity
        ethnicity = demo.get("ethnicity")
        if not ethnicity or ethnicity == "not reported":
            row["is_latino"] = pd.NA
        else:
            row["is_latino"] = 1 if ethnicity == "hispanic or latino" else 0
        

        # case_id
        id = case.get("case_id")
        if not id:
            row["case_id"] = pd.NA
        else:
            row["case_id"] = id


        
        # next do exposure features
        exposures = case.get("exposures") # this will refer to the initial exposure
        if exposures is not None:
            
            # smoking status
            SMOKING_STATUS = {
                "Lifelong Non-Smoker" : 0,
                "Current Reformed Smoker for > 15 yrs" : 1,
                "Current Reformed Smoker for < or = 15 yrs" : 2,
                "Current Smoker" : 3,
                "Not Reported" : pd.NA


            }
            row["smoking_status"] = SMOKING_STATUS.get(exposures[0]["tobacco_smoking_status"], pd.NA)
            # pack years smoked (remember to normalize as well)
            pack_years = exposures[0].get("pack_years_smoked", None)
            row["pack_years_smoked"] = pack_years if pack_years != None else pd.NA


        # initialize treatments to 0
        row["had_chemo"] = 0
        row["had_radiation"] = 0
        row["had_surgery"] = 0
        row["had_external_beam"] = 0
        row["had_molecular_therapy"] = 0
        row["had_pharma_therapy"] = 0
        

        # define different therapeutic agent names
        CHEMICALS = ["Gemcitabine", "Carboplatin", "Cyclophosphamide", "Erlotinib", "Gemcitabine Hydrochloride", "Vinorelbine", "Vinorelbine Tartrate", "Cisplatin", "Docetaxel", "Erlotinib Hydrochloride", "Pemetrexed", "Pemetrexed Disodium", "Paclitaxel", "Nab-paclitaxel", "Etoposide", "Bevacizumab", "Belinostat", "Irinotecan", "Irinotecan Hydrochloride", "Topotecan", "Vinblastine", "Anastrozole", "Gefitinib", "Letrozole", "Cyanocobalamin", "Octreotide Acetate", "Denosumab", "Pegfilgrastim", "Zoledronic Acid", "Tyrosine Kinase Inhibitor", "Aurora Kinase/VEGFR2 Inhibitor CYC116", "Recombinant PRAME Protein Plus AS15 Adjuvant GSK2302025A"]
        for chemical in CHEMICALS:
            row[chemical] = pd.NA # initialize to None at first
            

        # chemical response scoring
        RESPONSES = {
            "Complete Response" : 0,
            "Partial Response" : 1,
            "Stable Disease" : 2,
            "Progressive Disease" : 3,
            "Treatment Ongoing" : pd.NA
            }

        # diagnosis information
        if case.get("diagnoses"):
            primary_diagnosis = case.get("diagnoses")[0]
            # now different ajcc stages - also normalize these
            STAGE_ORDER = {"Stage I" : 0, "Stage IA" : 1,
                        "Stage IB" : 2, "Stage IC" : 3,
                        "Stage II" : 4, "Stage IIA" : 5,
                        "Stage IIB" : 6, "Stage III" : 7,
                        "Stage IIIA" : 8, "Stage IIIB" : 9,
                        "Stage IV" : 10}
            row["ajcc_stage"] = STAGE_ORDER.get(primary_diagnosis.get("ajcc_pathologic_stage"), pd.NA)

            # also account for tumor, metastasis and lymph nodes
            m = primary_diagnosis.get("ajcc_pathologic_m")
            row["ajcc_m"] = pd.NA if not m or m[1] == "X" else int(m[1]) # parsing number portion of these
            t = primary_diagnosis.get("ajcc_pathologic_t")
            row["ajcc_t"] = pd.NA if not t or t[1] == "X" else int(t[1])
            n = primary_diagnosis.get("ajcc_pathologic_n")
            row["ajcc_n"] = pd.NA if not n or n[1] == "X" else int(n[1])

            # laterality (what side of the body the cancer is on)
            l = primary_diagnosis.get("laterality")
            row["is_left_lateral"] = 0 #init to 0
            row["is_right_lateral"] = 0
            row["is_bilateral"] = 0
            if l:
                row["is_left_lateral"] = 1 if l == "Left" else 0
                row["is_right_lateral"] = 1 if l == "Right" else 0
                row["is_bilateral"] = 1 if l == "Bilateral" else 0


            # now  different treatments and drugs within the primary diagnosis
            treatments = primary_diagnosis.get("treatments")
            
            # treatment iteration for treatment type
            if treatments:
                row["num_treatments"] = len(treatments)
                for t in treatments:
                    # type of treatment
                    treatment_type = t.get("treatment_type", pd.NA)
                    if treatment_type == "Chemotherapy": row["had_chemo"] = 1
                    if treatment_type == "Radiation Therapy, NOS": row["had_radiation"] = 1
                    if treatment_type == "Pharmaceutical Therapy, NOS": row["had_pharma_therapy"] = 1
                    if treatment_type == "Surgery, NOS": row["had_surgery"] = 1
                    if treatment_type == "Targeted Molecular Therapy": row["had_molecular_therapy"] = 1
                    if treatment_type == "Radiation, External Beam": row["had_external_beam"] = 1

                
                # iterate through treatments again
                for t in treatments:
                    agent = t.get("therapeutic_agents")
                    outcome = t.get("treatment_outcome")
                    if (agent and outcome) and (agent in CHEMICALS) and (outcome in RESPONSES):
                        row[agent] = RESPONSES[outcome]

                # prior malignancy
                pm = primary_diagnosis.get("prior_malignancy")
                row["had_prior_malignancy"] = (1 if pm == "yes" else 0) if pm else pd.NA

                # follow-ups extraction - first do ecog scores
                # find the first follow up with an ecog score
                follow_ups = case.get("follow_ups")
                if follow_ups:
                    for fu in follow_ups:
                        ecog_score = fu.get("ecog_performance_status")
                        if ecog_score and ecog_score != "Unknown":
                            row["ecog_performance"] = int(ecog_score)
                            break

        rows.append(row) # row in list represents row of DF
    
    df = pd.DataFrame(data=rows)
    # normalize continuous / ordinarl cols to not skew log reg training
    
    """SCALING - maybe remove this part because of model leakage
    """
    continuous_cols = ["age_at_index", "pack_years_smoked","num_treatments", "ajcc_stage", "ajcc_t", "ajcc_n", "ajcc_m", "smoking_status", "ecog_performance", "Gemcitabine", "Carboplatin", "Cyclophosphamide", "Erlotinib", "Gemcitabine Hydrochloride", "Vinorelbine", "Vinorelbine Tartrate", "Cisplatin", "Docetaxel", "Erlotinib Hydrochloride", "Pemetrexed", "Pemetrexed Disodium", "Paclitaxel", "Nab-paclitaxel", "Etoposide", "Bevacizumab", "Belinostat", "Irinotecan", "Irinotecan Hydrochloride", "Topotecan", "Vinblastine", "Anastrozole", "Gefitinib", "Letrozole", "Cyanocobalamin", "Octreotide Acetate", "Denosumab", "Pegfilgrastim", "Zoledronic Acid", "Tyrosine Kinase Inhibitor", "Aurora Kinase/VEGFR2 Inhibitor CYC116", "Recombinant PRAME Protein Plus AS15 Adjuvant GSK2302025A"]
    existing_cols = [c for c in continuous_cols if c in df.columns and df[c].notna().any()]
    df = df.replace(pd.NA, np.nan)
    df[existing_cols] = imputer.fit_transform(df[existing_cols]) # this fills in all NaN with the mean of the col
    df[existing_cols] = scaler.fit_transform(df[existing_cols]) #normalization
    
    return df


        
# # TESTING AND EXECUTION



# temp_df = extract_features('clinical_cases.json')
# #print(temp_df[["pack_years_smoked", "vital_status"]][:50])
# # print(temp_df[temp_df['pack_years_smoked'].notna()][['pack_years_smoked', 'vital_status']][:50])
# # print(temp_df["pack_years_smoked"].max())
# #print(temp_df[:40])

# CHEMICALS = ["Gemcitabine", "Carboplatin", "Cyclophosphamide", "Erlotinib", "Gemcitabine Hydrochloride", "Vinorelbine", "Vinorelbine Tartrate", "Cisplatin", "Docetaxel", "Erlotinib Hydrochloride", "Pemetrexed", "Pemetrexed Disodium", "Paclitaxel", "Nab-paclitaxel", "Etoposide", "Bevacizumab", "Belinostat", "Irinotecan", "Irinotecan Hydrochloride", "Topotecan", "Vinblastine", "Anastrozole", "Gefitinib", "Letrozole", "Cyanocobalamin", "Octreotide Acetate", "Denosumab", "Pegfilgrastim", "Zoledronic Acid", "Tyrosine Kinase Inhibitor", "Aurora Kinase/VEGFR2 Inhibitor CYC116", "Recombinant PRAME Protein Plus AS15 Adjuvant GSK2302025A"]

# print(temp_df.iloc[:20, :-25])

            
            
            
            
