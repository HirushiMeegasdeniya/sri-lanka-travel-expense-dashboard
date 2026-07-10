# Import pandas so we can load and prepare data for charts.
import pandas as pd

# Import matplotlib so we can create and save charts.
import matplotlib.pyplot as plt

# Import seaborn so we can create heatmaps and boxplots more easily.
import seaborn as sns

# Import Path so file paths work properly on Windows, Mac, and Linux.
from pathlib import Path


# Create the path to the cleaned dataset.
CLEAN_FILE = Path("outputs") / "cleaned_travel_expenses.csv"

# Create the path to the trip summary file created in Step 4.
TRIP_SUMMARY_FILE = Path("outputs") / "trip_summary.csv"

# Create the folder where charts will be saved.
CHARTS_FOLDER = Path("charts")

# Create the charts folder if it does not already exist.
CHARTS_FOLDER.mkdir(exist_ok=True)


# Print a message so we know the script has started.
print("Starting visualization process...")


# Load the cleaned expense-level dataset.
df = pd.read_csv(CLEAN_FILE)

# Load the trip-level summary dataset.
trip_summary = pd.read_csv(TRIP_SUMMARY_FILE)

# Convert the Date column in the cleaned dataset into datetime format.
df["Date"] = pd.to_datetime(df["Date"])

# Convert the Date column in the trip summary dataset into datetime format.
trip_summary["Date"] = pd.to_datetime(trip_summary["Date"])


# -----------------------------
# Chart 1: Bar chart
# Average trip cost by destination
# -----------------------------

# Group trips by destination and calculate average trip cost.
average_trip_cost = trip_summary.groupby("Destination", as_index=False)[
    "Total_Trip_Cost_LKR"
].mean()

# Rename the total trip cost column to make the chart label clearer.
average_trip_cost = average_trip_cost.rename(
    columns={"Total_Trip_Cost_LKR": "Average_Trip_Cost_LKR"}
)

# Sort destinations from highest average trip cost to lowest.
average_trip_cost = average_trip_cost.sort_values(
    by="Average_Trip_Cost_LKR",
    ascending=False
)

# Create a new chart figure.
plt.figure(figsize=(10, 6))

# Create a bar chart using seaborn.
sns.barplot(
    data=average_trip_cost,
    x="Destination",
    y="Average_Trip_Cost_LKR"
)

# Add a chart title.
plt.title("Average Trip Cost by Destination")

# Add a label to the x-axis.
plt.xlabel("Destination")

# Add a label to the y-axis.
plt.ylabel("Average Trip Cost (LKR)")

# Rotate destination names so they are easier to read.
plt.xticks(rotation=45)

# Adjust spacing so labels do not get cut off.
plt.tight_layout()

# Save the chart as a PNG image.
plt.savefig(CHARTS_FOLDER / "average_trip_cost_by_destination.png")

# Close the chart so the next chart starts fresh.
plt.close()


# -----------------------------
# Chart 2: Pie chart
# Spending by category
# -----------------------------

# Group expenses by category and calculate total spending.
category_spending = df.groupby("Category")["Amount_LKR"].sum()

# Create a new chart figure.
plt.figure(figsize=(8, 8))

# Create a pie chart.
plt.pie(
    category_spending,
    labels=category_spending.index,
    autopct="%1.1f%%",
    startangle=90
)

# Add a chart title.
plt.title("Spending Distribution by Category")

# Make sure the pie chart is drawn as a circle.
plt.axis("equal")

# Adjust spacing.
plt.tight_layout()

# Save the pie chart as a PNG image.
plt.savefig(CHARTS_FOLDER / "spending_by_category_pie_chart.png")

# Close the chart.
plt.close()


# -----------------------------
# Chart 3: Line chart
# Monthly spending trend
# -----------------------------

# Group expenses by month and calculate total spending.
monthly_spending = df.groupby("Month", as_index=False)["Amount_LKR"].sum()

# Sort the monthly spending data by month.
monthly_spending = monthly_spending.sort_values(by="Month")

# Create a new chart figure.
plt.figure(figsize=(12, 6))

# Create a line chart.
sns.lineplot(
    data=monthly_spending,
    x="Month",
    y="Amount_LKR",
    marker="o"
)

# Add a chart title.
plt.title("Monthly Spending Trend")

# Add a label to the x-axis.
plt.xlabel("Month")

# Add a label to the y-axis.
plt.ylabel("Total Spending (LKR)")

# Rotate month labels so they are easier to read.
plt.xticks(rotation=45)

# Adjust spacing so labels do not get cut off.
plt.tight_layout()

# Save the line chart as a PNG image.
plt.savefig(CHARTS_FOLDER / "monthly_spending_trend.png")

# Close the chart.
plt.close()


# -----------------------------
# Chart 4: Heatmap
# Destination × Category spending
# -----------------------------

# Create a pivot table showing total spending by destination and category.
destination_category_spending = df.pivot_table(
    values="Amount_LKR",
    index="Destination",
    columns="Category",
    aggfunc="sum",
    fill_value=0
)

# Create a new chart figure.
plt.figure(figsize=(12, 7))

# Create a heatmap.
sns.heatmap(
    destination_category_spending,
    annot=True,
    fmt=".0f",
    linewidths=0.5
)

# Add a chart title.
plt.title("Destination × Category Spending Heatmap")

# Add a label to the x-axis.
plt.xlabel("Expense Category")

# Add a label to the y-axis.
plt.ylabel("Destination")

# Adjust spacing.
plt.tight_layout()

# Save the heatmap as a PNG image.
plt.savefig(CHARTS_FOLDER / "destination_category_spending_heatmap.png")

# Close the chart.
plt.close()


# -----------------------------
# Chart 5: Boxplot
# Expense distribution by destination
# -----------------------------

# Create a new chart figure.
plt.figure(figsize=(12, 6))

# Create a boxplot showing expense distribution by destination.
sns.boxplot(
    data=df,
    x="Destination",
    y="Amount_LKR"
)

# Add a chart title.
plt.title("Expense Distribution by Destination")

# Add a label to the x-axis.
plt.xlabel("Destination")

# Add a label to the y-axis.
plt.ylabel("Expense Amount (LKR)")

# Rotate destination names so they are easier to read.
plt.xticks(rotation=45)

# Adjust spacing.
plt.tight_layout()

# Save the boxplot as a PNG image.
plt.savefig(CHARTS_FOLDER / "expense_distribution_by_destination.png")

# Close the chart.
plt.close()


# Print a success message.
print("Visualizations created successfully!")

# Print the folder where charts were saved.
print("Charts saved in the charts folder.")