select 
    police_district,
    avg(dispatch_to_received_min + enroute_to_dispatch_min + onscene_to_enroute_min) as avg_response_time
from {{ source('raw', 'law_enforcement_calls') }}
group by police_district