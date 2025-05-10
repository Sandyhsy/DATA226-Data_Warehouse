# Weather Analytics Pipeline 🌦️  
**DATA 226 Final Project – Real-time and Historical Weather Data Dashboard**

## Overview

This project presents an end-to-end weather data pipeline that extracts, processes, and visualizes both real-time and historical weather data from a public API. Using tools like Apache Airflow, Snowflake, and dbt, we built a system that supports:

- Real-time and historical weather data ingestion (ETL via Airflow)
- Data transformation, quality checks, and aggregation (ELT via dbt)
- Interactive dashboards using Tableau and Power BI
- Machine learning models to predict weather indicators and sports suitability

The final pipeline demonstrates a scalable architecture that connects raw data ingestion with business intelligence and predictive analytics.

> 📁 GitHub Repository: [DATA226_PROJECT](https://github.com/matthewleffler1/DATA226_PROJECT)  
> 🌐 Weather API Explorer: [WeatherAPI](https://www.weatherapi.com/api-explorer.aspx#current)

---

## Technologies Used

- **Apache Airflow**: Orchestration of ETL and ELT workflows  
- **Snowflake**: Cloud data warehouse  
- **dbt (data build tool)**: SQL-based transformation and quality testing  
- **Tableau & Power BI**: Visualization tools  
- **WeatherAPI**: Real-time & historical weather data  
- **Python + REST API + DAGs**: Custom extraction and scheduling logic  

---

## How to Run the Project

1. **Start the pipeline environment**

   ```bash
   docker compose up
2. **Access Apache Airflow UI**

   After starting the containers, open your browser and navigate to: http://localhost:8081/

  Use the default login credentials:
  
  - **Username**: `airflow`
  - **Password**: `airflow`
  
  Once logged in:
  
  - Go to **Admin > Connections** to configure your database connection (e.g., Snowflake).  
    - Set up your connection with appropriate credentials and schema details.
  - Then go to **Admin > Variables**, and add a variable:
  
    | Key              | Value                                |
    |------------------|----------------------------------------|
    | `weather_api_key` | *(Your API Key from [weatherapi.com](https://www.weatherapi.com/))* |
  
  These configurations are required before running any DAGs.
## 🔧 Configure Airflow Connections and Variables

1. Go to **Admin > Connections** in the Airflow UI and set up your **Snowflake** connection with the appropriate credentials.

2. Navigate to **Admin > Variables** and add the following variable:

   - **Key**: `weather_api_key`  
   - **Value**: *(Your API key from [WeatherAPI](https://www.weatherapi.com/))*

3. Trigger DAGs in Airflow

  Once setup is complete, trigger the following DAGs:
  
  - `weather_etl_sanjose`: Fetch historical weather data for San Jose
  - `weather_etl_zipcode`: Fetch current weather data across California ZIP codes
  - `weather_elt_dbt`: Run dbt transformations and data validation

4. View Dashboards
  - Open `visualizations/tableau_dashboard.twb` using **Tableau Public**
  - Open `visualizations/powerbi_dashboard.pbix` using **Power BI**

5. Project Highlights
  - **Live weather monitoring** across California
  - **ML predictions** for sports suitability & heat stress risk
  - **Dashboards** for public health, planning, and forecasting
  - **Hourly ingestion** and automation via Apache Airflow

---

## Contributors

**Group 6 – Department of Applied Data Science, San Jose State University**  
- Lam Tran  
- Khac Minh Dai Vo  
- Matthew Leffler  
- Shao-Yu Huang  
- Yilin Sun
