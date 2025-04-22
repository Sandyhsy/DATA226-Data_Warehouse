with __dbt__cte__avg_response_by_district as (
select 
    police_district,
    avg(dispatch_to_received_min + enroute_to_dispatch_min + onscene_to_enroute_min) as avg_response_time
from USER_DB_LION.raw.law_enforcement_calls
group by police_district
) select *,
       rank() over (order by avg_response_time) as response_time_rank
from __dbt__cte__avg_response_by_district