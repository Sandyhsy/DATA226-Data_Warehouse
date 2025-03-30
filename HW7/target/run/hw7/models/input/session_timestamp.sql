
  create or replace   view USER_DB_LION.analytics.session_timestamp
  
   as (
    SELECT sessionId, ts
FROM USER_DB_LION.raw.session_timestamp
WHERE sessionId IS NOT NULL
  );

