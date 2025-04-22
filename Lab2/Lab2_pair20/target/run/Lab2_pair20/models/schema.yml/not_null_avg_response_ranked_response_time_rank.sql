select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select response_time_rank
from USER_DB_LION.analytics.avg_response_ranked
where response_time_rank is null



      
    ) dbt_internal_test