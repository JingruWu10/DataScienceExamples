#import statements
import numpy as np
import pandas as pd

#I am going to use the same dateset as assignment 3
adults = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data", header=None)

#print the first 5 rows of the dataset

print(adult_df.head())



#lets' add some column headers to make it easier to work with this data

adult_columns = ["age", "workclass", "fnlwgt", "education", "education-num","marital-status", "occupation", "relationship", "race", "sex","capital-gain", "capital-loss", "hours-per-week", "native-country","income"]


# and now we can apply that list of names to our dataframe

adult_df.columns = adult_columns



#print the first 5 rows of the dataset

print(adult_df.head())


#check the distribution of age column
plt.hist(adults.loc[:,"age"])

def clean_column(column): #define functions to find outlier and replace with median values
    LimitHi = np.mean(column) + 2 * np.std(column)  # set high bar
    LimitLo = np.mean(column) - 2 * np.std(column)  # set low bar
    FlagGood = (column >= LimitLo) & (column <= LimitHi)
    FlagBad = ~FlagGood  # flag bad equals to not Flaggood
    column[FlagBad] = np.median(column[FlagGood])  # replace outliers with median values

def replace_missing_data(column): #define functions to replace the missing data with most frequent value
    FlagGood = (column != ' ?') & (column != " ")
    FlagBad = ~FlagGood
    column[FlagBad] = max(set(column), key=column.tolist().count)  # fill in missing value with the most frequent value


#I am going to create a loop to clean the data and fill in missing data,
# if the column contains integer, i am going to identify the outlier and fill it with mean
# if the column contains string, i am going to fill the missing data with the most frequent value
for colunm in adults:
    if adults[colunm].dtype in ["int64", "float64"]:
        clean_column(adults[colunm])
    else:
        replace_missing_data(adults[colunm])

adults.to_csv(path_or_buf="C:/Users/shcui/Desktop/results_1.csv") #write to csv file

