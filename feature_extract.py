from statistics import mean

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
def extract_features(file : str, specimen_file : str) -> DataFrame:
    with open(file, 'r') as f:
        cases = json.load(f) #this converts the json object into python dict
    with open(specimen_file, 'r') as f:
        specimens = json.load(f)
    # list to be converted to DF
    rows = []

    
    
    
    # iterate through cases
    for case in cases:
        row = {}

        this_specimen = None
        for specimen in specimens:
            if specimen.get("case_id") == case.get("case_id"):
                this_specimen = specimen

        # first extract demographic features
        demo = case.get("demographic") or {} # {} is just empty dict in case there is no demographic block
        # extract races
        race = demo.get("race")
        row["is_white"] = (1 if race == "white" else 0) if race and race.lower() != "not reported" else pd.NA
        #row["is_black"] = (1 if race == "black or african american" else 0) if race and race.lower() != "not reported" else pd.NA

        # extract gender
        gender = demo.get("gender")
        row["gender"] = (1 if gender == "male" else 0) if gender and gender.lower() != "not reported" else pd.NA
     
        
        # vital status
        surviving = demo.get("vital_status")
        row["vital_status"] = 0 if surviving and surviving == "Alive" else 1 

        # age at index - REMEMBER TO NORMALIZE AFTER
        age = demo.get("age_at_index")
        #row["age_at_index"] = age

        # Country (remember nominal)
        country = demo.get("country_of_residence_at_enrollment")
        if country:
            #row["is_american"] = 1 if country == "United States" else 0
            #row["is_canadian"] = 1 if country == "Canada" else 0
            row["is_russian"] = 1 if country == "Russia" else 0
            row["is_australian"] = 1 if country == "Australia" else 0
            row["is_german"] = 1 if country == "Germany" else 0


        # latino / ethnicity
        ethnicity = demo.get("ethnicity")
        # if not ethnicity or ethnicity == "not reported":
        #     row["is_latino"] = pd.NA
        # else:
        #     row["is_latino"] = 1 if ethnicity == "hispanic or latino" else 0
        

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
            #row["smoking_status"] = SMOKING_STATUS.get(exposures[0]["tobacco_smoking_status"], pd.NA)
            # pack years smoked (remember to normalize as well)
            pack_years = exposures[0].get("pack_years_smoked", None)
            #row["pack_years_smoked"] = pack_years if pack_years != None else pd.NA


        # initialize treatments to 0
        row["had_chemo"] = 0
        #row["chemo_start"] = 0
        #row["chemo_end"] = 0
        row["had_radiation"] = 0
        #row["radiation_start"] = 0
        row["radiation_end"] = 0
        row["had_surgery"] = 0
        row["surgery_start"] = 0
        #row["surgery_end"] = 0
        row["had_external_beam"] = 0
        #row["beam_start"] = 0
        row["beam_end"] = 0
        row["had_molecular_therapy"] = 0
        #row["molecular_start"] = 0
        #row["molecular_end"] = 0
        row["had_pharma_therapy"] = 0
        #row["pharma_start"] = 0
        #row["pharma_end"] = 0
        

        # define different therapeutic agent names
        CHEMICALS = [
                     #"Gemcitabine",
                     #"Carboplatin",
                     #"Cyclophosphamide",
                     #"Erlotinib",
                     #"Gemcitabine Hydrochloride",
                     #"Vinorelbine",
                     "Vinorelbine Tartrate",
                     #"Cisplatin", //this gave nearly 1% when removed. for the love of god do not put back in
                     "Docetaxel",
                     #"Erlotinib Hydrochloride",
                     #"Pemetrexed",
                     #"Pemetrexed Disodium",
                     #"Paclitaxel",
                     #"Nab-paclitaxel",
                     #"Etoposide",
                     "Bevacizumab",
                     #"Belinostat",
                     #"Irinotecan",
                     #"Irinotecan Hydrochloride",
                     #"Topotecan",
                     #"Vinblastine",
                     #"Anastrozole",
                     #"Gefitinib",
                     #"Letrozole",
                     #"Cyanocobalamin",
                     #"Octreotide Acetate",
                     #"Denosumab",
                     #"Pegfilgrastim",
                     #"Zoledronic Acid",
                     #"Tyrosine Kinase Inhibitor",
                     #"Aurora Kinase/VEGFR2 Inhibitor CYC116",
                     #"Recombinant PRAME Protein Plus AS15 Adjuvant GSK2302025A"
                     ]
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
            #row["ajcc_n"] = pd.NA if not n or n[1] == "X" else int(n[1])

            # laterality (what side of the body the cancer is on)
            l = primary_diagnosis.get("laterality")
            #row["is_left_lateral"] = 0 #init to 0
            row["is_right_lateral"] = 0
            #row["is_bilateral"] = 0
            if l:
                #row["is_left_lateral"] = 1 if l == "Left" else 0
                row["is_right_lateral"] = 1 if l == "Right" else 0
                #row["is_bilateral"] = 1 if l == "Bilateral" else 0


            # now  different treatments and drugs within the primary diagnosis
            treatments = primary_diagnosis.get("treatments")
            
            # treatment iteration for treatment type
            if treatments:
                #row["num_treatments"] = len(treatments)
                for t in treatments:
                    # type of treatment
                    treatment_type = t.get("treatment_type", pd.NA)
                    treatment_end = t.get("days_to_treatment_end")
                    treatment_start = t.get("days_to_treatment_start")
                    if treatment_type == "Chemotherapy":
                        row["had_chemo"] = 1
                        #row["chemo_start"] = treatment_start
                        #row["chemo_end"] = treatment_end
                    if treatment_type == "Radiation Therapy, NOS":
                        row["had_radiation"] = 1
                        #row["radiation_start"] = treatment_start
                        row["radiation_end"] = treatment_end
                    if treatment_type == "Pharmaceutical Therapy, NOS":
                        row["had_pharma_therapy"] = 1
                        #row["pharma_start"] = treatment_start
                        #row["pharma_end"] = treatment_end
                    if treatment_type == "Surgery, NOS":
                        row["had_surgery"] = 1
                        row["surgery_start"] = treatment_start
                        #row["surgery_end"] = treatment_end
                    if treatment_type == "Targeted Molecular Therapy":
                        row["had_molecular_therapy"] = 1
                        #row["molecular_start"] = treatment_start
                        #row["molecular_end"] = treatment_end
                    if treatment_type == "Radiation, External Beam":
                        row["had_external_beam"] = 1
                        #row["beam_start"] = treatment_start
                        row["beam_end"] = treatment_end

                
                # iterate through treatments again
                for t in treatments:
                    agent = t.get("therapeutic_agents")
                    outcome = t.get("treatment_outcome")
                    if (agent and outcome) and (agent in CHEMICALS) and (outcome in RESPONSES):
                        row[agent] = RESPONSES[outcome]

                # prior malignancy
                pm = primary_diagnosis.get("prior_malignancy")
                #row["had_prior_malignancy"] = (1 if pm == "yes" else 0) if pm else pd.NA

                # follow-ups extraction - first do ecog scores
                # find the first follow up with an ecog score
                follow_ups = case.get("follow_ups")
                if follow_ups:
                    for fu in follow_ups:
                        ecog_score = fu.get("ecog_performance_status")
                        if ecog_score and ecog_score != "Unknown":
                            row["ecog_performance"] = int(ecog_score)
                            break

        #row["tumor_cells"] = pd.NA
        row["stromal_cells"] = pd.NA
        row["neutrophil_infiltration"] = pd.NA
        #row["lymphocyte_infiltration"] = pd.NA
        #row["necrosis"] = pd.NA
        row["monocyte_infiltration"] = pd.NA
        row["rna_28s_16s_ratio"] = pd.NA
        row["a260_a280_ratio"] = pd.NA

        if this_specimen is not None:
            tumor_cells = []
            percent_stromal_cells = []
            percent_neutrophil_infiltration = []
            percent_lymphocyte_infiltration = []
            percent_necrosis = []
            percent_monocyte_infiltration = []
            ribosomal_rna_28s_16s_ratio = []
            a260_a280_ratio = []
            for sample in this_specimen.get("samples"):
                for portion in sample.get("portions"):
                    if portion.__contains__("analytes"):
                        for analyte in portion.get("analytes"):
                            if analyte.get("ribosomal_rna_28s_16s_ratio"):
                                ribosomal_rna_28s_16s_ratio.append(analyte.get("ribosomal_rna_28s_16s_ratio"))
                            if analyte.get("a260_a280_ratio"):
                                a260_a280_ratio.append(analyte.get("a260_a280_ratio"))
                    if portion.__contains__("slides"):
                        for slide in portion.get("slides"):
                            if slide.get("percent_stromal_cells"):
                                percent_stromal_cells.append(slide.get("percent_stromal_cells"))
                            if slide.get("percent_neutrophil_infiltration"):
                                percent_neutrophil_infiltration.append(slide.get("percent_neutrophil_infiltration"))
                            if slide.get("percent_lymphocyte_infiltration"):
                                percent_lymphocyte_infiltration.append(slide.get("percent_lymphocyte_infiltration"))
                            if slide.get("percent_monocyte_infiltration"):
                                percent_monocyte_infiltration.append(slide.get("percent_monocyte_infiltration"))
                            if slide.get("percent_necrosis"):
                                percent_necrosis.append(slide.get("percent_necrosis"))
                            if slide.get("percent_tumor_cells"):
                                tumor_cells.append(slide.get("percent_tumor_cells"))
            #row["tumor_cells"] = mean(tumor_cells) if len(tumor_cells) > 0 else pd.NA
            row["stromal_cells"] = mean(percent_stromal_cells) if len(percent_stromal_cells) > 0 else pd.NA
            row["neutrophil_infiltration"] = mean(percent_neutrophil_infiltration) if len(percent_neutrophil_infiltration) > 0 else pd.NA
            #row["lymphocyte_infiltration"] = mean(percent_lymphocyte_infiltration) if len(percent_lymphocyte_infiltration) > 0 else pd.NA
            #row["necrosis"] = mean(percent_necrosis) if len(percent_necrosis) > 0 else pd.NA
            row["monocyte_infiltration"] = mean(percent_monocyte_infiltration) if len(percent_monocyte_infiltration) > 0 else pd.NA
            row["rna_28s_16s_ratio"] = mean(ribosomal_rna_28s_16s_ratio) if len(ribosomal_rna_28s_16s_ratio) > 0 else pd.NA
            row["a260_a280_ratio"] = mean(a260_a280_ratio) if len(a260_a280_ratio) > 0 else pd.NA

        rows.append(row) # row in list represents row of DF
    
    df = pd.DataFrame(data=rows)

    # clean df of all nan rows
    df = df.replace(pd.NA, np.nan)
    
    return df.loc[:, df.notna().any()] # returns new df only with cols that arent ALL nan

#def normalize_features(df : DataFrame) -> DataFrame:


        
# # TESTING AND EXECUTION



# temp_df = extract_features('clinical_cases.json')
# #print(temp_df[["pack_years_smoked", "vital_status"]][:50])
# # print(temp_df[temp_df['pack_years_smoked'].notna()][['pack_years_smoked', 'vital_status']][:50])
# # print(temp_df["pack_years_smoked"].max())
# #print(temp_df[:40])

# CHEMICALS = ["Gemcitabine", "Carboplatin", "Cyclophosphamide", "Erlotinib", "Gemcitabine Hydrochloride", "Vinorelbine", "Vinorelbine Tartrate", "Cisplatin", "Docetaxel", "Erlotinib Hydrochloride", "Pemetrexed", "Pemetrexed Disodium", "Paclitaxel", "Nab-paclitaxel", "Etoposide", "Bevacizumab", "Belinostat", "Irinotecan", "Irinotecan Hydrochloride", "Topotecan", "Vinblastine", "Anastrozole", "Gefitinib", "Letrozole", "Cyanocobalamin", "Octreotide Acetate", "Denosumab", "Pegfilgrastim", "Zoledronic Acid", "Tyrosine Kinase Inhibitor", "Aurora Kinase/VEGFR2 Inhibitor CYC116", "Recombinant PRAME Protein Plus AS15 Adjuvant GSK2302025A"]

# print(temp_df.iloc[:20, :-25])

            
            
            
            
