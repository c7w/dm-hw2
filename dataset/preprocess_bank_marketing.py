# [SRC] bank-full.csv
# "age";"job";"marital";"education";"default";"balance";"housing";"loan";"contact";"day";"month";"duration";"campaign";"pdays";"previous";"poutcome";"y"
# 58;"management";"married";"tertiary";"no";2143;"yes";"no";"unknown";5;"may";261;1;-1;0;"unknown";"no"
# 44;"technician";"single";"secondary";"no";29;"yes";"no";"unknown";5;"may";151;1;-1;0;"unknown";"no"
# 33;"entrepreneur";"married";"secondary";"no";2;"yes";"yes";"unknown";5;"may";76;1;-1;0;"unknown";"no"
# 47;"blue-collar";"married";"unknown";"no";1506;"yes";"no";"unknown";5;"may";92;1;-1;0;"unknown";"no"
# 33;"unknown";"single";"unknown";"no";1;"no";"no";"unknown";5;"may";198;1;-1;0;"unknown";"no"
# 35;"management";"married";"tertiary";"no";231;"yes";"no";"unknown";5;"may";139;1;-1;0;"unknown";"no"
# 28;"management";"single";"tertiary";"no";447;"yes";"yes";"unknown";5;"may";217;1;-1;0;"unknown";"no"
# 42;"entrepreneur";"divorced";"tertiary";"yes";2;"yes";"no";"unknown";5;"may";380;1;-1;0;"unknown";"no"

# [Target file 1] bank-marketing.data
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

# [Target file 2] bank-marketing.info
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

# Read from the bank-full.csv file and preprocess the data.
import pandas as pd

# Read the CSV file
df = pd.read_csv('bank-full.csv', sep=';')

column_names = df.columns

# Convert the data into the specified format for bank-marketing.data
with open('bank-marketing.data', 'w') as data_file:
    for index, row in df.iterrows():
        # Convert row to list of strings
        row_list = row.astype(str).tolist()
        # Join the list into a comma-separated string
        data_line = ",".join(row_list)
        # Write the line to the file
        data_file.write(data_line + "\n")

# Create the bank-marketing.info file
with open('bank-marketing.info', 'w') as info_file:
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
