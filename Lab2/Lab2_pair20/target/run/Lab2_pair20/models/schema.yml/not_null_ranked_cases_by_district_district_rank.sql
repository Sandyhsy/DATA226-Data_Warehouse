select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select district_rank
from USER_DB_LION.analytics.ranked_cases_by_district
where district_rank is null



      
    ) dbt_internal_test