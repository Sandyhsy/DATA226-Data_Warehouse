select 
    case_date,
    count(case_id) as daily_case_count
from {{ ref('daily_cases') }}
group by case_date
order by case_date