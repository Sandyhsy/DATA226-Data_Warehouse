# 🚔 Law Enforcement Data Pipeline with Airflow, dbt Cloud, Snowflake, and Superset

This project implements an end-to-end analytics pipeline for real-time law enforcement dispatch data from the City of San Francisco. It leverages **Apache Airflow** for orchestration, **dbt Cloud** for ELT modeling, **Snowflake** as the cloud data warehouse, and **Apache Superset** for dashboard visualization.

---

## 🔧 Localhost Access

- **Airflow Web UI**: [http://localhost:8081](http://localhost:8081)  
- **Superset (Optional)**: [http://localhost:8088](http://localhost:8088)

---

## 🗂️ Project Components

| Component         | Tool            | Purpose                                                 |
|------------------|------------------|----------------------------------------------------------|
| Data Orchestration | Apache Airflow | Automates ETL and triggers dbt Cloud ELT jobs           |
| Data Warehouse    | Snowflake        | Stores raw and transformed data                         |
| Data Modeling     | dbt Cloud        | Cleans and transforms data via SQL models               |
| Data Visualization| Apache Superset  | Visualizes key performance metrics through dashboards   |

---

## 🧩 Configuration & Variables

### 📥 Data Source

- **Source**: `https://data.sfgov.org/resource/gnap-fj3t.csv`  
  (_Real-time dispatched calls for service from SFPD_)

### ❄️ Snowflake

- **Database**: `USER_DB_LION`
- **Schema**: `raw`

These variables are set in Airflow using the UI or environment variables.

### 🧠 dbt Cloud

- **Job ID**: `70471823455826`  
  Used in the `DbtCloudRunJobOperator` inside Airflow.

**Airflow Connection Setup:**

1. Create a personal or service token in dbt Cloud.  
2. In Airflow → Admin → Connections, create:
   - **Conn Id**: `dbt_cloud`
   - **Conn Type**: `Dbt Cloud`
   - **Account ID**: (from dbt URL)
   - **API Token**: (your generated token)


---

## 📊 Superset Dashboards (Optional)

If enabled, Superset can be used to visualize key metrics like:

- 📈 Daily Case Trends
- 🗺️ District-wise Case Counts
- ⏱️ Average Response Times

---

## ⚙️ How to Run the Project

```bash
# Step 1: Launch Docker services
docker-compose up --build -d

# Step 2 (Optional): Create Superset admin user
docker exec -it superset superset fab create-admin \
  --username admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@example.com \
  --password admin
