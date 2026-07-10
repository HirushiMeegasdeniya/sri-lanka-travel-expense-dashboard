# Import pandas so we can load, filter, and summarize the travel expense data.
import pandas as pd

# Import Streamlit so we can create the interactive web dashboard.
import streamlit as st

# Import Plotly Express so we can create interactive charts.
import plotly.express as px

# Import Path so our file paths work correctly on Windows, Mac, and Linux.
from pathlib import Path


# Get the main project folder path.
BASE_DIR = Path(__file__).resolve().parents[1]

# Create the path to the cleaned expense-level dataset.
CLEAN_FILE = BASE_DIR / "outputs" / "cleaned_travel_expenses.csv"

# Create the path to the trip-level summary dataset.
TRIP_SUMMARY_FILE = BASE_DIR / "outputs" / "trip_summary.csv"

# Create the path to the folder that contains saved chart images.
CHARTS_FOLDER = BASE_DIR / "charts"


# Configure the Streamlit page title, icon, and layout.
st.set_page_config(
    page_title="Sri Lanka Travel Expense Dashboard",
    page_icon="🇱🇰",
    layout="wide"
)


# Define a function to format Sri Lankan Rupee values.
def format_lkr(value):
    # Check whether the value is missing.
    if pd.isna(value):

        # Return zero rupees if the value is missing.
        return "LKR 0"

    # Return the value formatted with commas and no decimal places.
    return f"LKR {value:,.0f}"


# Cache the data loading function so the dashboard runs faster.
@st.cache_data
def load_data():
    # Load the cleaned expense-level dataset.
    df = pd.read_csv(CLEAN_FILE)

    # Load the trip-level summary dataset.
    trip_summary = pd.read_csv(TRIP_SUMMARY_FILE)

    # Convert the Date column in the expense-level dataset into datetime format.
    df["Date"] = pd.to_datetime(df["Date"])

    # Convert the Date column in the trip-level dataset into datetime format.
    trip_summary["Date"] = pd.to_datetime(trip_summary["Date"])

    # Return both datasets.
    return df, trip_summary


# Load the datasets by calling the load_data function.
df, trip_summary = load_data()


# Create the main dashboard title.
st.title("🇱🇰 Sri Lanka Travel Expense Intelligence Dashboard")

# Add a short professional project description.
st.markdown(
    """
    This dashboard analyzes travel expense patterns across popular Sri Lankan destinations.
    It helps compare trip costs, daily spending, expense categories, traveler types, and seasonal trends.
    """
)


# Add a horizontal divider.
st.divider()


# Create a sidebar title for filters.
st.sidebar.title("Dashboard Filters")

# Create a list of available destinations.
destination_options = sorted(df["Destination"].dropna().unique())

# Create a multi-select filter for destinations.
selected_destinations = st.sidebar.multiselect(
    "Select Destination",
    options=destination_options,
    default=destination_options
)

# Create a list of available seasons.
season_options = sorted(df["Season"].dropna().unique())

# Create a multi-select filter for seasons.
selected_seasons = st.sidebar.multiselect(
    "Select Season",
    options=season_options,
    default=season_options
)

# Create a list of available traveler types.
traveler_type_options = sorted(df["Traveler_Type"].dropna().unique())

# Create a multi-select filter for traveler type.
selected_traveler_types = st.sidebar.multiselect(
    "Select Traveler Type",
    options=traveler_type_options,
    default=traveler_type_options
)


# Filter the expense-level dataset based on selected dashboard filters.
filtered_df = df[
    (df["Destination"].isin(selected_destinations))
    & (df["Season"].isin(selected_seasons))
    & (df["Traveler_Type"].isin(selected_traveler_types))
]

# Filter the trip-level dataset based on selected dashboard filters.
filtered_trip_summary = trip_summary[
    (trip_summary["Destination"].isin(selected_destinations))
    & (trip_summary["Season"].isin(selected_seasons))
    & (trip_summary["Traveler_Type"].isin(selected_traveler_types))
]


# Check whether the filtered data is empty.
if filtered_df.empty or filtered_trip_summary.empty:

    # Show a warning message if no data matches the selected filters.
    st.warning("No data available for the selected filters. Please change your filter selection.")

    # Stop the dashboard from running further.
    st.stop()


# Calculate total number of unique trips.
total_trips = filtered_trip_summary["Trip_ID"].nunique()

# Calculate total spending.
total_spending = filtered_df["Amount_LKR"].sum()

# Calculate average trip cost.
average_trip_cost = filtered_trip_summary["Total_Trip_Cost_LKR"].mean()

# Calculate average cost per day.
average_cost_per_day = filtered_trip_summary["Cost_Per_Day_LKR"].mean()


# Calculate average trip cost by destination.
destination_cost = filtered_trip_summary.groupby("Destination", as_index=False)[
    "Total_Trip_Cost_LKR"
].mean()

# Rename the cost column.
destination_cost = destination_cost.rename(
    columns={"Total_Trip_Cost_LKR": "Average_Trip_Cost_LKR"}
)

# Sort destinations by average trip cost.
destination_cost = destination_cost.sort_values(
    by="Average_Trip_Cost_LKR",
    ascending=False
)

# Get the most expensive destination name.
most_expensive_destination = destination_cost.iloc[0]["Destination"]


# Create a section heading for key metrics.
st.subheader("Key Metrics")

# Create four dashboard metric columns.
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

# Display total trips in the first metric column.
metric_col1.metric("Total Trips", f"{total_trips:,}")

# Display total spending in the second metric column.
metric_col2.metric("Total Spending", format_lkr(total_spending))

# Display average trip cost in the third metric column.
metric_col3.metric("Average Trip Cost", format_lkr(average_trip_cost))

# Display most expensive destination in the fourth metric column.
metric_col4.metric("Most Expensive Destination", most_expensive_destination)


# Add a small note below the metrics.
st.caption(
    f"Average cost per day for the selected filters: {format_lkr(average_cost_per_day)}"
)


# Add a horizontal divider.
st.divider()


# Create two columns for the first row of charts.
chart_col1, chart_col2 = st.columns(2)


# -----------------------------
# Chart 1: Average trip cost by destination
# -----------------------------

# Create a bar chart for average trip cost by destination.
fig_destination = px.bar(
    destination_cost,
    x="Destination",
    y="Average_Trip_Cost_LKR",
    title="Average Trip Cost by Destination",
    labels={
        "Destination": "Destination",
        "Average_Trip_Cost_LKR": "Average Trip Cost (LKR)"
    }
)

# Update the bar chart layout.
fig_destination.update_layout(
    xaxis_tickangle=-45,
    height=450
)

# Display the bar chart in the first chart column.
chart_col1.plotly_chart(fig_destination, use_container_width=True)


# -----------------------------
# Chart 2: Spending by category
# -----------------------------

# Group the filtered data by category and calculate total spending.
category_spending = filtered_df.groupby("Category", as_index=False)["Amount_LKR"].sum()

# Sort categories by total spending.
category_spending = category_spending.sort_values(
    by="Amount_LKR",
    ascending=False
)

# Create a pie chart for category spending.
fig_category = px.pie(
    category_spending,
    names="Category",
    values="Amount_LKR",
    title="Spending Distribution by Category"
)

# Update the pie chart layout.
fig_category.update_layout(height=450)

# Display the pie chart in the second chart column.
chart_col2.plotly_chart(fig_category, use_container_width=True)


# Add a horizontal divider.
st.divider()


# -----------------------------
# Chart 3: Monthly spending trend
# -----------------------------

# Group the filtered data by month and calculate total spending.
monthly_spending = filtered_df.groupby("Month", as_index=False)["Amount_LKR"].sum()

# Sort monthly spending by month.
monthly_spending = monthly_spending.sort_values(by="Month")

# Create a line chart for monthly spending trend.
fig_monthly = px.line(
    monthly_spending,
    x="Month",
    y="Amount_LKR",
    markers=True,
    title="Monthly Spending Trend",
    labels={
        "Month": "Month",
        "Amount_LKR": "Total Spending (LKR)"
    }
)

# Update the line chart layout.
fig_monthly.update_layout(
    xaxis_tickangle=-45,
    height=450
)

# Display the monthly spending chart.
st.plotly_chart(fig_monthly, use_container_width=True)


# Add a horizontal divider.
st.divider()


# Create two columns for the second row of charts.
chart_col3, chart_col4 = st.columns(2)


# -----------------------------
# Chart 4: Destination × Category heatmap
# -----------------------------

# Create a pivot table for destination and category spending.
heatmap_data = filtered_df.pivot_table(
    values="Amount_LKR",
    index="Destination",
    columns="Category",
    aggfunc="sum",
    fill_value=0
)

# Create an interactive heatmap.
fig_heatmap = px.imshow(
    heatmap_data,
    text_auto=".0f",
    aspect="auto",
    title="Destination × Category Spending Heatmap",
    labels={
        "x": "Expense Category",
        "y": "Destination",
        "color": "Spending (LKR)"
    }
)

# Update the heatmap layout.
fig_heatmap.update_layout(height=500)

# Display the heatmap.
chart_col3.plotly_chart(fig_heatmap, use_container_width=True)


# -----------------------------
# Chart 5: Expense distribution boxplot
# -----------------------------

# Create a boxplot for expense distribution by destination.
fig_boxplot = px.box(
    filtered_df,
    x="Destination",
    y="Amount_LKR",
    title="Expense Distribution by Destination",
    labels={
        "Destination": "Destination",
        "Amount_LKR": "Expense Amount (LKR)"
    }
)

# Update the boxplot layout.
fig_boxplot.update_layout(
    xaxis_tickangle=-45,
    height=500
)

# Display the boxplot.
chart_col4.plotly_chart(fig_boxplot, use_container_width=True)


# Add a horizontal divider.
st.divider()


# Create a section heading for data preview.
st.subheader("Filtered Data Preview")

# Display the first 20 rows of filtered data.
st.dataframe(filtered_df.head(20), use_container_width=True)


# Add a horizontal divider.
st.divider()


# Create a section heading for project insights.
st.subheader("Project Insights Template")

# Display professional insight-writing guidance.
st.markdown(
    """
    Use your analysis results to write insights in this format:

    **Finding + Evidence + Meaning + Recommendation**

    Example:

    **Accommodation was the largest expense category in the selected data.**
    This suggests that lodging is a major cost driver in Sri Lankan travel budgets.
    Travelers who want to reduce total trip cost should compare hotels, guest houses,
    hostels, and off-peak booking options.
    """
)


# Create an expandable section for saved chart images.
with st.expander("View saved chart images from Step 5"):

    # Create a list of saved chart image file names.
    chart_files = [
        "average_trip_cost_by_destination.png",
        "spending_by_category_pie_chart.png",
        "monthly_spending_trend.png",
        "destination_category_spending_heatmap.png",
        "expense_distribution_by_destination.png",
    ]

    # Loop through each chart file.
    for chart_file in chart_files:

        # Create the full file path for the chart image.
        chart_path = CHARTS_FOLDER / chart_file

        # Check whether the chart image exists.
        if chart_path.exists():

            # Display the chart file name.
            st.write(f"**{chart_file}**")

            # Display the chart image.
            st.image(str(chart_path), use_container_width=True)

        # If the chart image does not exist, show a message.
        else:

            # Show a warning for the missing chart.
            st.warning(f"{chart_file} not found in the charts folder.")


# Add a horizontal divider.
st.divider()


# Add a footer.
st.markdown(
    """
    **Project:** Sri Lanka Travel Expense Intelligence Dashboard  
    **Tools:** Python, Pandas, Plotly, Streamlit  
    **Purpose:** Beginner-friendly data analysis and dashboard project for portfolio building.
    """
)