select *,
       rank() over (order by avg_response_time) as response_time_rank
from {{ ref('avg_response_by_district') }}