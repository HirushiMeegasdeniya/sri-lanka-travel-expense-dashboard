# Import pandas so we can create and save tabular data as a CSV file.
import pandas as pd

# Import numpy so we can generate random numbers for realistic data.
import numpy as np

# Import random so we can randomly choose destinations, categories, and traveler types.
import random

# Import datetime so we can create realistic travel dates.
from datetime import datetime, timedelta

# Import Path so our file paths work cleanly on Windows, Mac, or Linux.
from pathlib import Path


# Set a random seed so the dataset is reproducible every time we run the script.
random.seed(42)

# Set a NumPy random seed for the same reason.
np.random.seed(42)


# Create the folder path where the CSV dataset will be saved.
DATA_FOLDER = Path("data")

# Create the data folder if it does not already exist.
DATA_FOLDER.mkdir(exist_ok=True)


# Set the number of unique trips we want to generate.
NUMBER_OF_TRIPS = 140

# Create a list of Sri Lankan destinations for the project.
destinations = [
    "Kandy",
    "Ella",
    "Galle",
    "Nuwara Eliya",
    "Colombo",
    "Mirissa",
    "Sigiriya",
    "Arugam Bay",
]


# Create destination popularity weights.
destination_weights = [0.14, 0.14, 0.13, 0.13, 0.15, 0.12, 0.10, 0.09]


# Create a list of traveler types.
traveler_types = ["Solo", "Couple", "Family"]

# Create traveler type weights to make the dataset realistic.
traveler_type_weights = [0.35, 0.40, 0.25]


# Create a list of possible payment methods.
payment_methods = ["Cash", "Card", "Online Transfer"]

# Create payment method weights.
payment_method_weights = [0.45, 0.35, 0.20]


# Create a dictionary for traveler cost multipliers.
traveler_multipliers = {
    "Solo": 1.00,
    "Couple": 1.75,
    "Family": 3.20,
}


# Create a dictionary for season cost multipliers.
season_multipliers = {
    "Peak": 1.25,
    "Off-Peak": 0.90,
}


# Create a dictionary for destination-based base prices.
destination_price_profile = {
    "Kandy": {
        "Accommodation": 9500,
        "Food": 2800,
        "Transport": 6500,
        "Activities": 3500,
        "Shopping": 4500,
        "Miscellaneous": 1800,
    },
    "Ella": {
        "Accommodation": 8000,
        "Food": 2600,
        "Transport": 7000,
        "Activities": 4200,
        "Shopping": 3000,
        "Miscellaneous": 1500,
    },
    "Galle": {
        "Accommodation": 12000,
        "Food": 3500,
        "Transport": 7500,
        "Activities": 3800,
        "Shopping": 5500,
        "Miscellaneous": 2000,
    },
    "Nuwara Eliya": {
        "Accommodation": 13500,
        "Food": 3200,
        "Transport": 7200,
        "Activities": 3600,
        "Shopping": 4200,
        "Miscellaneous": 1900,
    },
    "Colombo": {
        "Accommodation": 17000,
        "Food": 4500,
        "Transport": 5500,
        "Activities": 3000,
        "Shopping": 8500,
        "Miscellaneous": 2500,
    },
    "Mirissa": {
        "Accommodation": 11000,
        "Food": 3300,
        "Transport": 7600,
        "Activities": 4800,
        "Shopping": 4200,
        "Miscellaneous": 2100,
    },
    "Sigiriya": {
        "Accommodation": 9000,
        "Food": 2500,
        "Transport": 6800,
        "Activities": 5200,
        "Shopping": 3200,
        "Miscellaneous": 1600,
    },
    "Arugam Bay": {
        "Accommodation": 10500,
        "Food": 3100,
        "Transport": 8200,
        "Activities": 4600,
        "Shopping": 3500,
        "Miscellaneous": 2000,
    },
}


# Create subcategories for each main expense category.
subcategories = {
    "Accommodation": ["Hotel", "Guest House", "Villa", "Hostel"],
    "Food": ["Restaurant", "Cafe", "Street Food", "Hotel Dining"],
    "Transport": ["Train", "Bus", "Taxi", "Fuel", "Tuk Tuk"],
    "Activities": ["Tickets", "Safari", "Surfing", "Guided Tour", "Museum"],
    "Shopping": ["Souvenirs", "Clothes", "Local Products", "Gifts"],
    "Miscellaneous": ["Tips", "Mobile Data", "Laundry", "Emergency"],
}


# Create a list of all main categories.
categories = list(subcategories.keys())


# Define a function to identify the travel season based on the month.
def get_season(date):
    # Get the month number from the date.
    month = date.month

    # Treat December, January, February, March, July, and August as peak travel months.
    if month in [12, 1, 2, 3, 7, 8]:

        # Return Peak if the month is considered high-demand travel season.
        return "Peak"

    # Return Off-Peak for all other months.
    return "Off-Peak"


# Define a function to generate a random travel date.
def generate_random_date():
    # Set the first possible travel date.
    start_date = datetime(2025, 1, 1)

    # Set the last possible travel date.
    end_date = datetime(2026, 6, 30)

    # Calculate how many days exist between the start date and end date.
    days_between = (end_date - start_date).days

    # Randomly choose how many days to add to the start date.
    random_days = random.randint(0, days_between)

    # Return the final random date.
    return start_date + timedelta(days=random_days)


# Define a function to generate realistic trip duration.
def generate_duration(destination):
    # Use shorter trips for Colombo because it is often a city/business stop.
    if destination == "Colombo":

        # Return a random duration between 1 and 3 days.
        return random.randint(1, 3)

    # Use slightly longer durations for Ella, Mirissa, and Arugam Bay.
    if destination in ["Ella", "Mirissa", "Arugam Bay"]:

        # Return a random duration between 2 and 5 days.
        return random.randint(2, 5)

    # Use medium trip durations for other destinations.
    return random.randint(2, 4)


# Define a function to generate a realistic rating.
def generate_rating(amount):
    # Generate a base rating between 3.2 and 5.0.
    rating = np.random.normal(loc=4.2, scale=0.45)

    # Slightly reduce rating if the amount is very high.
    if amount > 50000:

        # Subtract a small value from the rating because expensive trips may feel less value-friendly.
        rating -= 0.3

    # Keep the rating between 1.0 and 5.0.
    rating = max(1.0, min(5.0, rating))

    # Round the rating to one decimal place.
    return round(rating, 1)


# Create an empty list to store all generated expense rows.
rows = []


# Start a loop to generate multiple trips.
for trip_number in range(1, NUMBER_OF_TRIPS + 1):

    # Create a trip ID like TRP_001, TRP_002, and so on.
    trip_id = f"TRP_{trip_number:03d}"

    # Randomly choose one destination using the destination weights.
    destination = random.choices(destinations, weights=destination_weights, k=1)[0]

    # Generate a random date for the trip.
    trip_date = generate_random_date()

    # Determine whether the trip happened in peak or off-peak season.
    season = get_season(trip_date)

    # Generate the duration of the trip.
    duration_days = generate_duration(destination)

    # Randomly choose the traveler type.
    traveler_type = random.choices(traveler_types, weights=traveler_type_weights, k=1)[0]

    # Get the traveler multiplier.
    traveler_multiplier = traveler_multipliers[traveler_type]

    # Get the season multiplier.
    season_multiplier = season_multipliers[season]

    # Make sure each trip includes the important core categories.
    selected_categories = ["Accommodation", "Food", "Transport", "Activities"]

    # Add Shopping to some trips.
    if random.random() < 0.75:

        # Add Shopping category to the selected category list.
        selected_categories.append("Shopping")

    # Add Miscellaneous to some trips.
    if random.random() < 0.65:

        # Add Miscellaneous category to the selected category list.
        selected_categories.append("Miscellaneous")

    # Loop through each selected expense category for the trip.
    for category in selected_categories:

        # Randomly choose a subcategory that belongs to the selected category.
        subcategory = random.choice(subcategories[category])

        # Get the base price for this destination and category.
        base_price = destination_price_profile[destination][category]

        # Use duration for categories that usually increase daily.
        if category in ["Accommodation", "Food", "Activities", "Miscellaneous"]:

            # Calculate the raw amount using base price, trip duration, traveler type, and season.
            amount = base_price * duration_days * traveler_multiplier * season_multiplier

        # Use a different calculation for transport and shopping.
        else:

            # Calculate transport or shopping as a trip-level cost instead of daily cost.
            amount = base_price * traveler_multiplier * season_multiplier

        # Add random variation so the dataset does not look fake.
        amount = amount * np.random.uniform(0.75, 1.35)

        # Round the amount to the nearest 100 Sri Lankan rupees.
        amount = round(amount / 100) * 100

        # Make sure amount is stored as an integer.
        amount = int(amount)

        # Randomly choose a payment method.
        payment_method = random.choices(payment_methods, weights=payment_method_weights, k=1)[0]

        # Generate a realistic rating for this expense row.
        rating = generate_rating(amount)

        # Create one complete row of data.
        row = {
            "Trip_ID": trip_id,
            "Date": trip_date.strftime("%Y-%m-%d"),
            "Destination": destination,
            "Duration_Days": duration_days,
            "Category": category,
            "Subcategory": subcategory,
            "Amount_LKR": amount,
            "Payment_Method": payment_method,
            "Traveler_Type": traveler_type,
            "Season": season,
            "Rating": rating,
        }

        # Add the row to the rows list.
        rows.append(row)


# Convert the list of rows into a pandas DataFrame.
df = pd.DataFrame(rows)


# Add one duplicate row intentionally so we can practice duplicate removal in Step 3.
df = pd.concat([df, df.sample(1, random_state=42)], ignore_index=True)


# Add a missing rating intentionally so we can practice missing value handling in Step 3.
df.loc[df.sample(1, random_state=10).index, "Rating"] = np.nan


# Add an unrealistic amount intentionally so we can practice fixing unrealistic values in Step 3.
df.loc[df.sample(1, random_state=20).index, "Amount_LKR"] = 999999


# Shuffle the rows so the data looks more natural.
df = df.sample(frac=1, random_state=42).reset_index(drop=True)


# Create the output file path.
output_file = DATA_FOLDER / "raw_travel_expenses.csv"


# Save the DataFrame as a CSV file without the pandas index column.
df.to_csv(output_file, index=False)


# Print a success message.
print("Dataset generated successfully!")


# Print the file location.
print(f"File saved at: {output_file}")


# Print the number of rows and columns in the dataset.
print(f"Dataset shape: {df.shape[0]} rows and {df.shape[1]} columns")


# Print the first five rows so we can preview the dataset.
print(df.head())