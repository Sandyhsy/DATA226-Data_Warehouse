
  create or replace   view USER_DB_LION.analytics.session_summary
  
   as (
    WITH u AS (
    SELECT * FROM USER_DB_LION.analytics.user_session_channel
), st AS (
    SELECT * FROM USER_DB_LION.analytics.session_timestamp
)
SELECT u.userId, u.sessionId, u.channel, st.ts
FROM u
JOIN st ON u.sessionId = st.sessionId
  );

