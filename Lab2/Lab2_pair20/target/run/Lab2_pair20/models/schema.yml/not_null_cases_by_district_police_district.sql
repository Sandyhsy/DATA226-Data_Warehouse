select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



with __dbt__cte__cases_by_district as (
select 
    police_district,
    count(*) as total_cases
from USER_DB_LION.raw.law_enforcement_calls
group by police_district
) select police_district
from __dbt__cte__cases_by_district
where police_district is null



      
    ) dbt_internal_test