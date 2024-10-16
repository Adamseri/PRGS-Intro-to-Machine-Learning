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

#  Creating a function that counts missing values for each column in a dataFrame
def count_missing(df):
    return df.isna().sum()
#using the function to count missing in our subsetted dataframe
count_missing_subset_nri=count_missing(subset_nri)
#dropping the STCOFIPS column
count_missing_subset_nri = count_missing_subset_nri.drop('STCOFIPS')
#converting to dataframe
count_missing_subset_nri= pd.DataFrame(count_missing_subset_nri)

nri_df['AVLN_FREQ_MISSING'] = np.where(nri_df['AVLN_AFREQ'].isna(),'Missing', 'Exists')
print(nri_df['AVLN_FREQ_MISSING'])

'''
#cross tabulating, but it doesn't make sense because AFREQ is a numerical variable, and to cross tabulate you need two categorical variables

crosstab_df=pd.crosstab(
    subset_nri['AVLN_AFREQ'],
    subset_nri['AVLN_RISKR'],
    dropna=False
)
#Identifying which columns ends with _AFREQ and _RISKR and assigning each to a variable
afreq_columns = [col for col in subset_nri.columns if col.endswith('_AFREQ')]
riskr_columns = [col for col in subset_nri.columns if col.endswith('_RISKR')]

# Impute zero in '_AFREQ' columns where the corresponding '_RISKR'columns are 'Not Applicable'
for riskr_columns, afreq_columns in zip(riskr_columns, afreq_columns):
    subset_nri.loc[subset_nri[riskr_columns] == 'Not Applicable', afreq_columns] = 0

#checking that it worked
'''
print(subset_nri)
'''



#### Task 2
#Question 1
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


#question 2
#using the function made in the previous task
svi_missing=count_missing(filtered_svi)
#turning it into a dataframe
svi_missing_df=pd.DataFrame(svi_missing)
print(svi_missing_df)


#Task 3
#Question 1
#The NRI dataset has 3 FIPS columns, one for state, one for county, and one for a combination of both, called state county (STCO). The SVI data has one column named FIPS and another column named STCNTY (State County) which can be interpreted in the same way as the STCOFIPS column from the NRI data and we should keep this in mind moving forward as we can use this as a key to merge our datasets


##merging the subsetted and filtered dataframes on the FIPS and STCOFIPS keys?
merged_nri_svi=pd.merge(subset_nri, filtered_svi, how='outer', left_on='STCOFIPS', right_on='FIPS')
#using count_missing function to county how many missing values there are in merged dataframe
missing_merged=count_missing(merged_nri_svi)
missing_merged_df=pd.DataFrame(missing_merged)


#Task 4
def plot_histogram(data, bins=10, title='Histogram', xlabel='Values', ylabel='Frequency'):
    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=bins, edgecolor='black')
    
    # Add title and axis labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # Show the plot
    plt.show()
#checking to see if it worked
hist_test= plot_histogram(merged_nri_svi['EP_MINRTY'])
#assigning a variable that is only the numerical variables in the merged dataset
selecting_numerical_variables= merged_nri_svi.select_dtypes(include=['number'])
#applying the plot_Histogram function to all the numerical variables in the merged dataset
apply_hist=selecting_numerical_variables.apply(plot_histogram)
'''