select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



with __dbt__cte__daily_cases as (
select 
    date_trunc('day', received_datetime) as case_date,
    id as case_id
from USER_DB_LION.raw.law_enforcement_calls
) select case_date
from __dbt__cte__daily_cases
where case_date is null



      
    ) dbt_internal_test