import numpy as np
import pandas as pd

file_list = {"11700intel": "general_template_11700_intelfullDESKTOP-JS3OJ8L.csv",
             # "11700intel2": "general_template_11700intel_full2DESKTOP-JS3OJ8L.csv",
             # "11700intelOC": "general_template_11700intel_full_ocDESKTOP-JS3OJ8L.csv",
             "11700openblas": "general_template_11700openblasfullDESKTOP-JS3OJ8L.csv",
             "amd4500Uopenblas": "general_template_amd_fullcolin-pn50.csv",
             "10700intel": "general_templateDESKTOP-JS3OJ8L.csv",
             "10700openblas": "general_template_openblasDESKTOP-JS3OJ8L.csv",
             "1135g7openblas": "general_template_1135g7_openblascolin-1135.csv",
             "1135g7intel_cold": "general_template_1135g7_intel_coldcolin-1135.csv",
             "1135g7intel": "general_template_1135g7intel_fullcolin-1135.csv",
             }
count = 0
for key, value in file_list.items():
    df = pd.read_csv(value, index_col=0)
    df['TotalRuntimeException'] = np.where(df['Exceptions'].isna(), df['TotalRuntime'], pd.NA)
    df = df[df['ValidationRound'] == 0]
    df_slice = df[['ID', 'Model','ModelParameters', 'TotalRuntimeException']]
    df_slice.columns = ["ID", "Model",'ModelParameters', key]
    if count == 0:
        results = df_slice
    else:
        results = results.merge(df_slice, on=["ID", "Model", 'ModelParameters'])
    count += 1

results['reg_mod'] = results['ModelParameters'].str.extract('{"regression_model": {"model": "(.*?)"')
results['reg_mod'] = np.where(results['reg_mod'].isna(), results['Model'], results['reg_mod'])
results.drop(columns=['ModelParameters'], inplace=True)

df_cleaned = results.dropna(how='any')
agg = df_cleaned.groupby("Model").sum().drop(columns=["ID", "reg_mod"])
agg_full = df_cleaned.groupby("reg_mod").sum().drop(columns=["ID", "Model"])
agg_full.idxmin(axis=1)


