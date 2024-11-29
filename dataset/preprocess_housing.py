# :Number of Instances: 506 

# :Number of Attributes: 13 numeric/categorical predictive. Median Value (attribute 14) is usually the target.

# :Attribute Information (in order):
#     - CRIM     per capita crime rate by town
#     - ZN       proportion of residential land zoned for lots over 25,000 sq.ft.
#     - INDUS    proportion of non-retail business acres per town
#     - CHAS     Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
#     - NOX      nitric oxides concentration (parts per 10 million)
#     - RM       average number of rooms per dwelling
#     - AGE      proportion of owner-occupied units built prior to 1940
#     - DIS      weighted distances to five Boston employment centres
#     - RAD      index of accessibility to radial highways
#     - TAX      full-value property-tax rate per $10,000
# - PTRATIO  pupil-teacher ratio by town
# - B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
# - LSTAT    % lower status of the population
# - MEDV     Median value of owner-occupied homes in $1000's


# [SRC] HousingData.csv
# CRIM,ZN,INDUS,CHAS,NOX,RM,AGE,DIS,RAD,TAX,PTRATIO,B,LSTAT,MEDV
# 0.00632,18,2.31,0,0.538,6.575,65.2,4.09,1,296,15.3,396.9,4.98,24
# 0.02731,0,7.07,0,0.469,6.421,78.9,4.9671,2,242,17.8,396.9,9.14,21.6
# 0.02729,0,7.07,0,0.469,7.185,61.1,4.9671,2,242,17.8,392.83,4.03,34.7
# 0.03237,0,2.18,0,0.458,6.998,45.8,6.0622,3,222,18.7,394.63,2.94,33.4
# 0.06905,0,2.18,0,0.458,7.147,54.2,6.0622,3,222,18.7,396.9,NA,36.2
# 0.02985,0,2.18,0,0.458,6.43,58.7,6.0622,3,222,18.7,394.12,5.21,28.7
# 0.08829,12.5,7.87,NA,0.524,6.012,66.6,5.5605,5,311,15.2,395.6,12.43,22.9

# [Target file 1] housing.data
# [example] tic-tac-toe.data
# x,x,x,x,o,o,x,o,o,positive
# x,x,x,x,o,o,o,x,o,positive
# x,x,x,x,o,o,o,o,x,positive
# x,x,x,x,o,o,o,b,b,positive
# x,x,x,x,o,o,b,o,b,positive
# x,x,x,x,o,o,b,b,o,positive
# x,x,x,x,o,b,o,o,b,positive
# x,x,x,x,o,b,o,b,o,positive
# x,x,x,x,o,b,b,o,o,positive
# x,x,x,x,b,o,o,o,b,positive
# x,x,x,x,b,o,o,b,o,positive

# [Target file 2] housing.info
# [example] tic-tac-toe.info. contains the column name and the type of the column (discrete or continuous). and the label position.
# 1 discrete
# 2 discrete
# 3 discrete
# 4 discrete
# 5 discrete
# 6 discrete
# 7 discrete
# 8 discrete
# 9 discrete
# class discrete
# LABEL_POS -1

import pandas as pd

# Read the CSV file
df = pd.read_csv('HousingData.csv', sep=',')

column_names = df.columns

# Convert the data into the specified format for housing.data
with open('housing.data', 'w') as data_file:
    for index, row in df.iterrows():
        # Convert row to list of strings
        row_list = row.astype(str).tolist()
        # Join the list into a comma-separated string
        data_line = ",".join(row_list)
        # Write the line to the file
        data_file.write(data_line + "\n")


# Create the housing.info file
with open('housing.info', 'w') as info_file:
    for i, column in enumerate(df.columns):
        # Determine if the column is discrete or continuous
        if df[column].dtype == 'object':
            column_type = 'discrete'
        else:
            column_type = 'continuous'
        # Write the column name and type to the file
        info_file.write(f"{column} {column_type}\n")
    # Write the label position
    info_file.write("LABEL_POS -1\n")
