import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Task 1
nri_data= r"C:\Users\aserilevi\code\PRGS-Intro-to-Machine-Learning\data\raw\National Risk Index (NRI) County Level Data\NRI_Table_Counties.csv"
nri_df=pd.read_csv(nri_data)
nri_df['STCOFIPS'] = nri_df['STCOFIPS'].astype(str)
stcofips_column = 'STCOFIPS'


# Filter columns that end with '_AFREQ' or '_RISKR'
filtered_nri = nri_df.filter(regex='(_AFREQ|_RISKR)$').columns

# Include the STCOFIPS column
filtered_nri = [stcofips_column] + list(filtered_nri)

# Subset the DataFrame with only columns of interest
subset_nri = nri_df[filtered_nri]

# Restrict to rows where STCOFIPS has exactly 5 digits
subset_nri = subset_nri[subset_nri[stcofips_column].astype(str).str.match(r'^\d{5}$')]

#Identifying which columns ends with _AFREQ and _RISKR and assigning each to a variable
afreq_columns = [col for col in subset_nri.columns if col.endswith('_AFREQ')]
riskr_columns = [col for col in subset_nri.columns if col.endswith('_RISKR')]

# Impute zero in '_AFREQ' columns where the corresponding '_RISKR'columns are 'Not Applicable'
for riskr_columns, afreq_columns in zip(riskr_columns, afreq_columns):
    subset_nri.loc[subset_nri[riskr_columns] == 'Not Applicable', afreq_columns] = 0


#importing SVI Data
svi_data= r"C:\Users\aserilevi\code\PRGS-Intro-to-Machine-Learning\data\raw\Social Vulnerability Index (SVI) County Level Data\SVI_2022_US_county.csv"
svi_df=pd.read_csv(svi_data)
svi_df['FIPS'] = svi_df['FIPS'].astype(str)
#identifying the columns I'm going to filter by
svi_columns = columns_to_select = [
    'ST', 'STATE', 'ST_ABBR', 'STCNTY', 'COUNTY', 'FIPS', 'LOCATION', 'AREA_SQMI',
    'E_TOTPOP', 'EP_POV150', 'EP_UNEMP', 'EP_HBURD', 'EP_NOHSDP', 'EP_UNINSUR', 'EP_AGE65', 
    'EP_AGE17', 'EP_DISABL', 'EP_SNGPNT', 'EP_LIMENG', 'EP_MINRTY', 'EP_MUNIT', 'EP_MOBILE', 
    'EP_CROWD', 'EP_NOVEH', 'EP_GROUPQ', 'EP_NOINT', 'EP_AFAM', 'EP_HISP', 'EP_ASIAN', 
    'EP_AIAN', 'EP_NHPI', 'EP_TWOMORE', 'EP_OTHERRACE'
]

#filtering the columns in the svi table 
filtered_svi=svi_df[svi_columns]
##merging the subsetted and filtered dataframes on the FIPS and STCOFIPS keys?
merged_nri_svi=pd.merge(subset_nri, filtered_svi, how='outer', left_on='STCOFIPS', right_on='FIPS')

merged_nri_svi.to_csv('data/processed/merged_dataset.csv', index=False)