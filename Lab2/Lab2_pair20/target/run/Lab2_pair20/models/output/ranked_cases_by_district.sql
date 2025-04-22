
  
    

        create or replace transient table USER_DB_LION.analytics.ranked_cases_by_district
         as
        (with __dbt__cte__cases_by_district as (
select 
    police_district,
    count(*) as total_cases
from USER_DB_LION.raw.law_enforcement_calls
group by police_district
) select *,
       rank() over (order by total_cases desc) as district_rank
from __dbt__cte__cases_by_district
        );
      
  