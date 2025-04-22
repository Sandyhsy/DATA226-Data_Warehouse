select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select case_date
from USER_DB_LION.analytics.count_daily_cases
where case_date is null



      
    ) dbt_internal_test