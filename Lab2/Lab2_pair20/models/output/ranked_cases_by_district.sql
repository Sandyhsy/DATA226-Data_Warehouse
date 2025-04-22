select *,
       rank() over (order by total_cases desc) as district_rank
from {{ ref('cases_by_district') }}