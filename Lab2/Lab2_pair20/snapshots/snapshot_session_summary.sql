{% snapshot daily_cases_snapshot %}

{{
  config(
    target_schema='snapshots',
    unique_key='CASE_DATE',
    strategy='check',
    check_cols=['DAILY_CASE_COUNT']
  )
}}

select * 
from {{ source('analytics', 'count_daily_cases') }}

{% endsnapshot %}