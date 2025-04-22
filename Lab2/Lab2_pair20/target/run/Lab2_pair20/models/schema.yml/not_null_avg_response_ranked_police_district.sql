select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select police_district
from USER_DB_LION.analytics.avg_response_ranked
where police_district is null



      
    ) dbt_internal_test