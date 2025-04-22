
  
    

        create or replace transient table USER_DB_LION.analytics.count_daily_cases
         as
        (with __dbt__cte__daily_cases as (
select 
    date_trunc('day', received_datetime) as case_date,
    id as case_id
from USER_DB_LION.raw.law_enforcement_calls
) select 
    case_date,
    count(case_id) as daily_case_count
from __dbt__cte__daily_cases
group by case_date
order by case_date
        );
      
  