# Import pandas so we can load, clean, and save tabular data.
import pandas as pd

# Import numpy so we can handle missing values and numerical calculations.
import numpy as np

# Import Path so file paths work properly on Windows, Mac, and Linux.
from pathlib import Path


# Create the path to the raw dataset file.
RAW_FILE = Path("data") / "raw_travel_expenses.csv"

# Create the folder path where cleaned data will be saved.
OUTPUT_FOLDER = Path("outputs")

# Create the outputs folder if it does not already exist.
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Create the path for the cleaned dataset file.
CLEAN_FILE = OUTPUT_FOLDER / "cleaned_travel_expenses.csv"


# Print a message so we know the script has started.
print("Starting data cleaning process...")


# Load the raw CSV file into a pandas DataFrame.
df = pd.read_csv(RAW_FILE)

# Print the shape of the raw dataset.
print("Raw dataset shape:", df.shape)

# Print the first five rows of the raw dataset.
print("\nFirst 5 rows of raw data:")
print(df.head())


# Print missing values in each column before cleaning.
print("\nMissing values before cleaning:")
print(df.isnull().sum())


# Count duplicate rows before removing them.
duplicate_count = df.duplicated().sum()

# Print the number of duplicate rows.
print("\nDuplicate rows before cleaning:", duplicate_count)


# Remove duplicate rows from the dataset.
df = df.drop_duplicates()

# Print the shape after removing duplicates.
print("Shape after removing duplicates:", df.shape)


# Convert the Date column from text into a real datetime column.
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Convert Duration_Days into numeric values.
df["Duration_Days"] = pd.to_numeric(df["Duration_Days"], errors="coerce")

# Convert Amount_LKR into numeric values.
df["Amount_LKR"] = pd.to_numeric(df["Amount_LKR"], errors="coerce")

# Convert Rating into numeric values.
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")


# Print missing values after data type conversion.
print("\nMissing values after data type conversion:")
print(df.isnull().sum())


# Fill missing Rating values using the median rating.
df["Rating"] = df["Rating"].fillna(df["Rating"].median())

# Fill missing Duration_Days values using the median duration.
df["Duration_Days"] = df["Duration_Days"].fillna(df["Duration_Days"].median())

# Fill missing Amount_LKR values using the median amount.
df["Amount_LKR"] = df["Amount_LKR"].fillna(df["Amount_LKR"].median())


# Remove rows where Date is missing because date is important for monthly trend analysis.
df = df.dropna(subset=["Date"])


# Convert Duration_Days into integers.
df["Duration_Days"] = df["Duration_Days"].astype(int)

# Convert Amount_LKR into integers.
df["Amount_LKR"] = df["Amount_LKR"].astype(int)


# Fix unrealistic trip durations below 1 day.
df.loc[df["Duration_Days"] < 1, "Duration_Days"] = 1

# Fix unrealistic trip durations above 14 days.
df.loc[df["Duration_Days"] > 14, "Duration_Days"] = 14


# Fix ratings below 1.
df.loc[df["Rating"] < 1, "Rating"] = 1

# Fix ratings above 5.
df.loc[df["Rating"] > 5, "Rating"] = 5


# Calculate the 25th percentile of Amount_LKR.
q1 = df["Amount_LKR"].quantile(0.25)

# Calculate the 75th percentile of Amount_LKR.
q3 = df["Amount_LKR"].quantile(0.75)

# Calculate the interquartile range.
iqr = q3 - q1

# Calculate the upper limit for realistic expense values.
upper_limit = q3 + 1.5 * iqr

# Print the calculated upper limit.
print("\nCalculated upper limit for Amount_LKR:", round(upper_limit, 2))


# Count how many rows have unrealistic high expense amounts.
unrealistic_count = (df["Amount_LKR"] > upper_limit).sum()

# Print the number of unrealistic expense rows.
print("Unrealistic high Amount_LKR rows found:", unrealistic_count)


# Define a function to replace unrealistic amounts.
def fix_unrealistic_amount(row):
    # Check whether this row has an amount higher than the upper limit.
    if row["Amount_LKR"] > upper_limit:

        # Filter the dataset to find similar rows with the same destination and category.
        similar_rows = df[
            (df["Destination"] == row["Destination"])
            & (df["Category"] == row["Category"])
            & (df["Amount_LKR"] <= upper_limit)
        ]

        # Check whether similar rows exist.
        if len(similar_rows) > 0:

            # Return the median amount from similar rows.
            return int(similar_rows["Amount_LKR"].median())

        # If no similar rows exist, return the overall median amount.
        return int(df[df["Amount_LKR"] <= upper_limit]["Amount_LKR"].median())

    # If the amount is realistic, return the original amount.
    return row["Amount_LKR"]


# Apply the unrealistic amount fixing function to every row.
df["Amount_LKR"] = df.apply(fix_unrealistic_amount, axis=1)


# Remove rows where Amount_LKR is zero or negative.
df = df[df["Amount_LKR"] > 0]


# Create a new column for year and month.
df["Month"] = df["Date"].dt.to_period("M").astype(str)


# Calculate cost per day for each expense row.
df["Cost_Per_Day"] = df["Amount_LKR"] / df["Duration_Days"]

# Round Cost_Per_Day to 2 decimal places.
df["Cost_Per_Day"] = df["Cost_Per_Day"].round(2)


# Sort the dataset by Date.
df = df.sort_values(by="Date")

# Reset the row index after sorting.
df = df.reset_index(drop=True)


# Print missing values after cleaning.
print("\nMissing values after cleaning:")
print(df.isnull().sum())


# Print final dataset shape.
print("\nCleaned dataset shape:", df.shape)


# Print first five rows of cleaned data.
print("\nFirst 5 rows of cleaned data:")
print(df.head())


# Save the cleaned dataset as a CSV file.
df.to_csv(CLEAN_FILE, index=False)


# Print the saved file location.
print("\nCleaned dataset saved successfully!")

# Print the cleaned file path.
print("File saved at:", CLEAN_FILE)