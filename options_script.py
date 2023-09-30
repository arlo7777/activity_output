import pandas as pd
import os

file_or_dir_name = "account_activity.csv"

# STEP 1 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * GET THE PATH * * * * * * * * * * * * * *

#Get the full path to the file or directory within the current directory 
full_path = os.path.join(os.getcwd(), file_or_dir_name)

#print("Full Path:", full_path)

# Read a CSV file
df = pd.read_csv('/Users/ak/Desktop/robinhood/account_activity.csv')

# Display the contents of the DataFrame
#print(df.head(10))

# STEP 2 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * CLEAN DATA * * * * * * * * * * * * * * * *

df.drop(df.columns[[1,2,3,4,7,8,10,11]], axis=1,inplace=True)
df = df[df['Trans Code'].str.contains('OASGN')==False]
df = df[df['Trans Code'].str.contains('Buy')==False]
df = df[df['Trans Code'].str.contains('ACH')==False]
df = df[df['Trans Code'].str.contains('OEXCS')==False]
df = df[df['Trans Code'].str.contains('OEXP')==False]
df = df[df['Trans Code'].str.contains('Sell')==False]
df = df[df['Trans Code'].str.contains('REC')==False]
df = df[df['Trans Code'].str.contains('OCA')==False]
df = df[df['Trans Code'].str.contains('BCXL')==False]
df = df[df['Trans Code'].str.contains('OAREV')==False]
df.drop(df.columns[[2]], axis=1,inplace=True)

# Replace parentheses with a negative sign
df['Amount'] = df['Amount'].str.replace(r'\(([^)]+)\)', r'-\1')

# Remove the dollar sign from the column values
df['Amount'] = df['Amount'].str.replace('$', '')

# Convert the column to float
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce', downcast='float')

# STEP 3 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * OUTPUT FILE 1 * * * * * * * * * * * * * * 

df.to_csv('Activity_Output.csv', index=False)

# STEP 4 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * WEEKLY NUMBERS * * * * * * * * * * * * * 

# Sum the values in the "Column_Name" column
total_sum = df['Amount'].sum()

# Print the total sum
print("Total Sum = $", total_sum)

# Convert the 'Date' column to datetime
df['Activity Date'] = pd.to_datetime(df['Activity Date'])

# Set 'Date' as the DataFrame's index
df.set_index('Activity Date', inplace=True)

# Resample data by week and calculate the sum for each week
weekly_sum = df.resample('W').sum()

# Reset the index to have 'Date' as a column (optional)
weekly_sum.reset_index(inplace=True)

# Print the result
print(weekly_sum)

print(df.head(30))

# STEP 5 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * OUTPUT FILE 2 * * * * * * * * * * * * * *

# Step 1: Open the file in write mode
output_file = open('weekly_sum.txt', 'w')

# Step 2: Use print statements to write text to the file
print("Total Sum = $", total_sum, "\n\n", weekly_sum, file=output_file)

# Step 3: Close the file to save changes
output_file.close()



