select 
    date_trunc('day', received_datetime) as case_date,
    id as case_id
from {{ source('raw', 'law_enforcement_calls') }}