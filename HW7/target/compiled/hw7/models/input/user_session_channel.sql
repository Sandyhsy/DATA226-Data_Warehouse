SELECT userId, sessionId, channel
FROM USER_DB_LION.raw.user_session_channel
WHERE sessionId IS NOT NULL