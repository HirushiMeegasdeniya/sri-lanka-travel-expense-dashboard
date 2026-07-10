# Import pandas so we can load, group, summarize, and analyze the dataset.
import pandas as pd

# Import Path so file paths work properly on Windows, Mac, and Linux.
from pathlib import Path


# Create the path to the cleaned dataset.
CLEAN_FILE = Path("outputs") / "cleaned_travel_expenses.csv"

# Create the folder where EDA result files will be saved.
OUTPUT_FOLDER = Path("outputs")

# Create the output folder if it does not already exist.
OUTPUT_FOLDER.mkdir(exist_ok=True)


# Print a starting message.
print("Starting Exploratory Data Analysis...")


# Load the cleaned dataset into a pandas DataFrame.
df = pd.read_csv(CLEAN_FILE)

# Convert the Date column into a proper datetime format.
df["Date"] = pd.to_datetime(df["Date"])

# Print the shape of the dataset.
print("\nDataset shape:")
print(df.shape)

# Print the column names.
print("\nDataset columns:")
print(df.columns.tolist())

# Print the first five rows.
print("\nFirst 5 rows:")
print(df.head())


# Create a trip-level summary.
trip_summary = df.groupby(
    ["Trip_ID", "Date", "Destination", "Duration_Days", "Traveler_Type", "Season"],
    as_index=False
)["Amount_LKR"].sum()

# Rename the Amount_LKR column to Total_Trip_Cost_LKR.
trip_summary = trip_summary.rename(columns={"Amount_LKR": "Total_Trip_Cost_LKR"})

# Calculate cost per day for each trip.
trip_summary["Cost_Per_Day_LKR"] = (
    trip_summary["Total_Trip_Cost_LKR"] / trip_summary["Duration_Days"]
).round(2)


# Print a preview of the trip-level summary.
print("\nTrip-level summary preview:")
print(trip_summary.head())


# Question 1: Which destination is most expensive?
destination_cost = trip_summary.groupby("Destination", as_index=False).agg(
    Average_Trip_Cost_LKR=("Total_Trip_Cost_LKR", "mean"),
    Median_Trip_Cost_LKR=("Total_Trip_Cost_LKR", "median"),
    Total_Trip_Cost_LKR=("Total_Trip_Cost_LKR", "sum"),
    Number_Of_Trips=("Trip_ID", "count")
)

# Sort destinations from most expensive to least expensive by average trip cost.
destination_cost = destination_cost.sort_values(
    by="Average_Trip_Cost_LKR",
    ascending=False
)

# Round the numeric values.
destination_cost["Average_Trip_Cost_LKR"] = destination_cost["Average_Trip_Cost_LKR"].round(2)
destination_cost["Median_Trip_Cost_LKR"] = destination_cost["Median_Trip_Cost_LKR"].round(2)

# Get the most expensive destination.
most_expensive_destination = destination_cost.iloc[0]


# Question 2: What is the average cost per day by destination?
cost_per_day_by_destination = trip_summary.groupby("Destination", as_index=False).agg(
    Average_Cost_Per_Day_LKR=("Cost_Per_Day_LKR", "mean"),
    Median_Cost_Per_Day_LKR=("Cost_Per_Day_LKR", "median"),
    Number_Of_Trips=("Trip_ID", "count")
)

# Sort by average cost per day.
cost_per_day_by_destination = cost_per_day_by_destination.sort_values(
    by="Average_Cost_Per_Day_LKR",
    ascending=False
)

# Round the numeric values.
cost_per_day_by_destination["Average_Cost_Per_Day_LKR"] = cost_per_day_by_destination[
    "Average_Cost_Per_Day_LKR"
].round(2)

cost_per_day_by_destination["Median_Cost_Per_Day_LKR"] = cost_per_day_by_destination[
    "Median_Cost_Per_Day_LKR"
].round(2)


# Question 3: Which expense category is highest?
category_spending = df.groupby("Category", as_index=False).agg(
    Total_Spending_LKR=("Amount_LKR", "sum"),
    Average_Expense_LKR=("Amount_LKR", "mean"),
    Number_Of_Expenses=("Category", "count")
)

# Sort categories by total spending.
category_spending = category_spending.sort_values(
    by="Total_Spending_LKR",
    ascending=False
)

# Round average expense.
category_spending["Average_Expense_LKR"] = category_spending["Average_Expense_LKR"].round(2)

# Get the highest spending category.
highest_category = category_spending.iloc[0]


# Question 4: How does spending compare between peak vs off-peak season?
season_spending = trip_summary.groupby("Season", as_index=False).agg(
    Total_Spending_LKR=("Total_Trip_Cost_LKR", "sum"),
    Average_Trip_Cost_LKR=("Total_Trip_Cost_LKR", "mean"),
    Median_Trip_Cost_LKR=("Total_Trip_Cost_LKR", "median"),
    Average_Cost_Per_Day_LKR=("Cost_Per_Day_LKR", "mean"),
    Number_Of_Trips=("Trip_ID", "count")
)

# Round numeric values.
season_spending["Average_Trip_Cost_LKR"] = season_spending["Average_Trip_Cost_LKR"].round(2)
season_spending["Median_Trip_Cost_LKR"] = season_spending["Median_Trip_Cost_LKR"].round(2)
season_spending["Average_Cost_Per_Day_LKR"] = season_spending["Average_Cost_Per_Day_LKR"].round(2)


# Question 5: How does solo travel compare to family travel?
traveler_type_spending = trip_summary.groupby("Traveler_Type", as_index=False).agg(
    Total_Spending_LKR=("Total_Trip_Cost_LKR", "sum"),
    Average_Trip_Cost_LKR=("Total_Trip_Cost_LKR", "mean"),
    Median_Trip_Cost_LKR=("Total_Trip_Cost_LKR", "median"),
    Average_Cost_Per_Day_LKR=("Cost_Per_Day_LKR", "mean"),
    Number_Of_Trips=("Trip_ID", "count")
)

# Sort traveler types by average trip cost.
traveler_type_spending = traveler_type_spending.sort_values(
    by="Average_Trip_Cost_LKR",
    ascending=False
)

# Round numeric values.
traveler_type_spending["Average_Trip_Cost_LKR"] = traveler_type_spending[
    "Average_Trip_Cost_LKR"
].round(2)

traveler_type_spending["Median_Trip_Cost_LKR"] = traveler_type_spending[
    "Median_Trip_Cost_LKR"
].round(2)

traveler_type_spending["Average_Cost_Per_Day_LKR"] = traveler_type_spending[
    "Average_Cost_Per_Day_LKR"
].round(2)


# Question 6: What is the monthly spending trend?
monthly_spending = df.groupby("Month", as_index=False).agg(
    Total_Spending_LKR=("Amount_LKR", "sum"),
    Number_Of_Expenses=("Amount_LKR", "count"),
    Average_Expense_LKR=("Amount_LKR", "mean")
)

# Round the average expense.
monthly_spending["Average_Expense_LKR"] = monthly_spending["Average_Expense_LKR"].round(2)

# Sort by month.
monthly_spending = monthly_spending.sort_values(by="Month")


# Save all EDA result tables as CSV files.
trip_summary.to_csv(OUTPUT_FOLDER / "trip_summary.csv", index=False)
destination_cost.to_csv(OUTPUT_FOLDER / "destination_cost_analysis.csv", index=False)
cost_per_day_by_destination.to_csv(OUTPUT_FOLDER / "cost_per_day_by_destination.csv", index=False)
category_spending.to_csv(OUTPUT_FOLDER / "category_spending_analysis.csv", index=False)
season_spending.to_csv(OUTPUT_FOLDER / "season_spending_analysis.csv", index=False)
traveler_type_spending.to_csv(OUTPUT_FOLDER / "traveler_type_spending_analysis.csv", index=False)
monthly_spending.to_csv(OUTPUT_FOLDER / "monthly_spending_trend.csv", index=False)


# Print Question 1 result.
print("\nQuestion 1: Which destination is most expensive?")
print(destination_cost)
print(
    f"\nMost expensive destination by average trip cost: "
    f"{most_expensive_destination['Destination']} "
    f"with an average trip cost of LKR "
    f"{most_expensive_destination['Average_Trip_Cost_LKR']:,.2f}"
)


# Print Question 2 result.
print("\nQuestion 2: Average cost per day by destination")
print(cost_per_day_by_destination)


# Print Question 3 result.
print("\nQuestion 3: Which expense category is highest?")
print(category_spending)
print(
    f"\nHighest spending category: "
    f"{highest_category['Category']} "
    f"with total spending of LKR "
    f"{highest_category['Total_Spending_LKR']:,.2f}"
)


# Print Question 4 result.
print("\nQuestion 4: Peak vs Off-Peak spending comparison")
print(season_spending)


# Print Question 5 result.
print("\nQuestion 5: Solo vs Couple vs Family travel comparison")
print(traveler_type_spending)


# Print Question 6 result.
print("\nQuestion 6: Monthly spending trend")
print(monthly_spending)


# Print a final success message.
print("\nEDA completed successfully!")

# Print the saved output location.
print("EDA result files saved in the outputs folder.")