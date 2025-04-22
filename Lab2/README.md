# Law Enforcement Data Pipeline with Airflow, dbt, and Superset

This project sets up an end-to-end data pipeline using Apache Airflow, dbt Cloud, Snowflake, and Apache Superset. The pipeline ingests public safety data from San Francisco's open data portal, processes it via dbt, and visualizes insights through Superset.

---

## 🔗 Localhost Access

- **Airflow Web UI**: [http://localhost:8081](http://localhost:8081)

---

## 🧩 Environment Variables & Configuration

Ensure the following variables are correctly set in your Airflow/DBT environment:

### 📥 Data Source

- **Public Data URL**:  
  `https://data.sfgov.org/resource/gnap-fj3t.csv`  
  (_This dataset contains raw police incident reports._)

### 🧠 dbt Cloud Job

- **dbt Cloud Job ID**: `70471823455826`  
  (_Used to trigger transformations from Airflow via the dbtCloudRunJobOperator._)

### ❄️ Snowflake Target Configuration

- **Database**: `USER_DB_LION`  
- **Schema**: `raw`

These should match your dbt `profiles.yml` or the credentials defined in Airflow Connections.

Create dbt service token and get the API(name of the tokens doesn’t matter): <br>
<img width="691" alt="Screenshot 2025-04-22 at 4 29 48 PM" src="https://github.com/user-attachments/assets/df7bf324-d578-4113-b7d8-c567418cc725" /> <br> <br>

Set connection to airflow: <br>
<img width="632" alt="Screenshot 2025-04-22 at 4 29 31 PM" src="https://github.com/user-attachments/assets/94e2242b-b353-4d05-ab60-f557be24fb33" /> <br>

---

## 📊 Visualization (Optional)

- Superset can be accessed at [http://localhost:8088](http://localhost:8088) _(if included in the Docker Compose setup)_
- Dashboards include:
  - Daily Case Trends
  - District-wise Case Ranking
  - Average Police Response Time

---

## ⚙️ How to Run

```bash
# Start the entire stack
docker-compose up --build -d

# (Optional) Reset Superset admin user
docker exec -it superset superset fab create-admin \
  --username admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@example.com \
  --password admin
