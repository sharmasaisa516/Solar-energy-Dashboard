# ☀️ Solar Energy Consumption Analysis & Visualization

A data analysis and visualization project built using **Python, Pandas, Streamlit, and Plotly** to analyze solar energy consumption across different countries and products. The project transforms raw energy consumption data into interactive and easy-to-understand visualizations, helping users explore consumption patterns and compare different energy products.

**Python** **Pandas** **Streamlit** **Plotly**

## 📝 Project Overview

Solar energy is an important source of renewable energy and understanding its consumption patterns can help in analyzing energy usage across different countries and products.

The main goal of this project is to analyze a solar energy consumption dataset and present the information through an interactive web application. Instead of viewing raw data in tables, the project uses interactive charts such as **Sunburst Charts and Bar Charts** to make the data easier to understand.

Users can select a country and explore its product-wise solar energy consumption through an interactive Sunburst visualization, while the overall consumption data can be represented using a Bar Chart.

### Key Features & Architecture

**Data Cleaning & Processing:**
Raw CSV data is cleaned and converted into a suitable format using Pandas. Missing and invalid consumption values are handled before visualization.

**Interactive Visualization:**
Plotly is used to create interactive charts that allow users to explore energy consumption data.

**Country-wise Analysis:**
Users can select a country from a dropdown menu and view the consumption distribution of different products for that country.

**Sunburst Visualization:**
The Sunburst chart displays the hierarchy of **Country → Product → Consumption**, making it easy to understand the contribution of different products.

**Bar Chart Visualization:**
A bar chart is used to compare product-wise consumption values and identify products with higher or lower energy consumption.

**Streamlit Web Application:**
Streamlit provides an interactive web interface where users can view charts and analyze the dataset without writing code.

## 💻 Tech Stack & Dependencies

### Core Language

**Python:**
Used as the primary programming language for data processing, analysis, and application development.

### Data Processing

**Pandas:**
Used for reading the CSV dataset, cleaning data, filtering records, grouping data, and calculating consumption values.

**NumPy:**
Can be used for numerical operations and efficient data handling.

### Data Visualization

**Plotly:**
Used to create interactive **Sunburst and Bar Charts** for visualizing energy consumption.

### Web Application

**Streamlit:**
Used to build the interactive dashboard and provide features such as titles, dropdown menus, charts, and user interaction.

## 📊 Dataset

The dataset used in this project contains information about energy consumption from different countries and products.

| Column        | Description               |
| ------------- | ------------------------- |
| `COUNTRY`     | Name of the country       |
| `CODE_TIME`   | Country/time related code |
| `TIME`        | Time period of the record |
| `YEAR`        | Year of consumption       |
| `MONTH`       | Month number              |
| `MONTH_NAME`  | Name of the month         |
| `PRODUCT`     | Type of energy product    |
| `CONSUMPTION` | Energy consumption value  |

The project mainly focuses on the **COUNTRY, PRODUCT, YEAR, and CONSUMPTION** columns for visualization and analysis.

## ⚙️ Detailed Workflow & Steps

### 1. Data Loading

The dataset is loaded from a CSV file using Pandas.

```python
df = pd.read_csv("data.csv")
```

The dataset is then stored in a Pandas DataFrame for further processing.

### 2. Data Cleaning

Before creating visualizations, the consumption column is converted into numeric format.

```python
df["CONSUMPTION"] = pd.to_numeric(
    df["CONSUMPTION"], errors="coerce"
)
```

Missing values and invalid records are removed to prevent errors during visualization.

Negative consumption values are also filtered out.

### 3. Data Filtering

A country selection option is provided using Streamlit.

```python
country = st.selectbox(
    "Select Country",
    sorted(df["COUNTRY"].unique())
)
```

When the user selects a country, only the corresponding records are used for the country-specific Sunburst visualization.

### 4. Product-wise Consumption

The selected country's data is grouped according to the product.

```python
country_data = df[df["COUNTRY"] == country]

country_data = country_data.groupby(
    "PRODUCT",
    as_index=False
)["CONSUMPTION"].sum()
```

This calculates the total consumption for each product.

### 5. Sunburst Chart

Plotly Express is used to create an interactive Sunburst chart.

```python
fig = px.sunburst(
    country_data,
    names="PRODUCT",
    values="CONSUMPTION"
)
```

The chart allows users to visually understand which products contribute more to the selected country's total energy consumption.

### 6. Bar Chart

A Bar Chart can be used to compare products based on their consumption.

```python
fig = px.bar(
    country_data,
    x="PRODUCT",
    y="CONSUMPTION",
    title="Product-wise Energy Consumption"
)

st.plotly_chart(fig, width="stretch")
```

The bar chart provides a simple comparison between different products.

### 7. Interactive Dashboard

Finally, all visualizations are displayed through Streamlit.

The dashboard allows users to:

* Select a country
* View product-wise consumption
* Explore the Sunburst Chart
* Compare products using a Bar Chart
* Interact with Plotly visualizations

## 📈 Expected Results

The project provides an interactive visualization of energy consumption data and makes it easier to identify consumption patterns.

The **Sunburst Chart** helps analyze the product distribution for the selected country, while the **Bar Chart** provides a direct comparison of product consumption.

The dashboard makes large amounts of energy data easier to understand and helps users quickly identify products with high and low consumption.

## 🎯 Project Objective

The main objective of this project is to demonstrate how **Python-based data analysis and visualization tools** can be used to convert raw energy consumption data into meaningful and interactive insights.

This project also demonstrates practical use of:

* Python
* Pandas
* Data Cleaning
* Data Aggregation
* Plotly Visualization
* Streamlit
* Interactive Data Analysis

## 🚀 Conclusion

The **Solar Energy Consumption Analysis & Visualization** project successfully converts raw energy consumption data into an interactive dashboard. By combining **Pandas for data processing, Plotly for visualization, and Streamlit for the user interface**, the project provides an easy and interactive way to explore energy consumption across countries and products.

The project can be further extended by adding yearly trend analysis, country comparisons, filters for months and years, and additional visualization techniques.
