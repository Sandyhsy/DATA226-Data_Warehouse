
  create or replace   view USER_DB_LION.analytics.user_session_channel
  
   as (
    SELECT userId, sessionId, channel
FROM USER_DB_LION.raw.user_session_channel
WHERE sessionId IS NOT NULL
  );

