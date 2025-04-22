select 
    police_district,
    count(*) as total_cases
from USER_DB_LION.raw.law_enforcement_calls
group by police_district