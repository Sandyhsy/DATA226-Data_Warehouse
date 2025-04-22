select 
    date_trunc('day', received_datetime) as case_date,
    id as case_id
from USER_DB_LION.raw.law_enforcement_calls