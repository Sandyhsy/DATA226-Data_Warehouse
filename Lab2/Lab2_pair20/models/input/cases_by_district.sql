select 
    police_district,
    count(*) as total_cases
from {{ source('raw', 'law_enforcement_calls') }}
group by police_district