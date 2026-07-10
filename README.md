# Sri Lanka Travel Expense Intelligence Dashboard

## Project Overview

This project analyzes travel expense patterns across popular Sri Lankan destinations using Python and Streamlit.

The goal of this project is to understand how travel costs vary by destination, expense category, travel season, and traveler type. The project uses a realistic synthetic dataset and includes data generation, cleaning, exploratory data analysis, visualizations, and an interactive dashboard.

This project was created as a beginner-friendly data science portfolio project.

---

## Business Problem

Travelers often struggle to estimate how much they need to budget for trips across Sri Lanka. Costs can vary depending on destination, season, trip duration, traveler type, and expense category.

This project answers questions such as:

* Which Sri Lankan destination has the highest average trip cost?
* Which expense category contributes the most to total spending?
* How does peak-season spending compare with off-peak spending?
* How does solo travel compare with family travel?
* What monthly spending trends can be identified?

---

## Dataset

The dataset was generated using Python and contains realistic travel expense records for Sri Lankan destinations.

### Dataset Columns

| Column         | Description                         |
| -------------- | ----------------------------------- |
| Trip_ID        | Unique trip identifier              |
| Date           | Date of the trip expense            |
| Destination    | Sri Lankan travel destination       |
| Duration_Days  | Number of days in the trip          |
| Category       | Main expense category               |
| Subcategory    | Detailed expense type               |
| Amount_LKR     | Expense amount in Sri Lankan Rupees |
| Payment_Method | Payment method used                 |
| Traveler_Type  | Solo, Couple, or Family             |
| Season         | Peak or Off-Peak                    |
| Rating         | Traveler rating                     |
| Month          | Year-month value for trend analysis |
| Cost_Per_Day   | Daily cost estimate                 |

### Destinations Included

* Kandy
* Ella
* Galle
* Nuwara Eliya
* Colombo
* Mirissa
* Sigiriya
* Arugam Bay

---

## Tools and Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* Streamlit
* Git
* GitHub
* VS Code

---

## Project Workflow

### 1. Dataset Generation

A realistic synthetic travel expense dataset was created using Python. The dataset includes destination-based pricing, seasonal pricing differences, traveler type differences, trip duration, categories, subcategories, and ratings.

### 2. Data Cleaning

The cleaning process included:

* Checking missing values
* Removing duplicate rows
* Converting date and numeric columns
* Fixing unrealistic expense values
* Creating new columns for month and cost per day
* Saving the cleaned dataset

### 3. Exploratory Data Analysis

The analysis answered key questions about destination costs, category spending, seasonal differences, traveler type differences, and monthly spending trends.

### 4. Data Visualization

The project includes the following charts:

* Average trip cost by destination
* Spending distribution by category
* Monthly spending trend
* Destination × Category spending heatmap
* Expense distribution by destination

### 5. Streamlit Dashboard

An interactive Streamlit dashboard was created with filters for:

* Destination
* Season
* Traveler type

The dashboard displays key metrics, interactive charts, filtered data, and project insights.

---

## Key Insights

1. The most expensive destination by average trip cost was identified using trip-level analysis.
2. Accommodation was one of the main cost drivers in the travel budget.
3. Peak-season trips showed higher average spending compared with off-peak trips.
4. Family travel had a higher average trip cost than solo travel.
5. Monthly spending trends helped identify high-spending travel periods.
6. Destination and category analysis showed where travelers spend the most.

---

## How to Run This Project

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/sri-lanka-travel-expense-dashboard.git
```

### 2. Open the Project Folder

```bash
cd sri-lanka-travel-expense-dashboard
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

### 5. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 6. Generate the Dataset

```bash
python scripts/generate_dataset.py
```

### 7. Clean the Data

```bash
python scripts/clean_data.py
```

### 8. Run Exploratory Data Analysis

```bash
python scripts/eda_analysis.py
```

### 9. Create Visualizations

```bash
python scripts/visualize_data.py
```

### 10. Run the Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Project Structure

```text
sri-lanka-travel-expense-dashboard/
│
├── charts/
├── dashboard/
│   └── app.py
├── data/
│   └── raw_travel_expenses.csv
├── outputs/
├── scripts/
│   ├── generate_dataset.py
│   ├── clean_data.py
│   ├── eda_analysis.py
│   └── visualize_data.py
├── screenshots/
├── PROJECT_INSIGHTS.md
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Future Improvements

* Add real travel cost data from public sources
* Include cost-per-person analysis
* Add machine learning to predict estimated trip cost
* Deploy the dashboard online
* Add more Sri Lankan destinations
* Improve dashboard styling and layout

---

## Author

Hirushi Sharanya Meegasdeniya

Data Science Undergraduate | Aspiring Data Scientist | Data Analyst
