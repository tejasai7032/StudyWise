import pandas as pd

# Read the dataset
data = pd.read_csv("data/study_data.csv")

# Display the dataset
print(data)

# Display the column names
print("\nColumns:")
print(data.columns)

# Display number of rows and columns
print("\nDataset shape:")
print(data.shape)