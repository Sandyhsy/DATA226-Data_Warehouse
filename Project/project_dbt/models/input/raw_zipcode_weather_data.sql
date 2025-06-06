SELECT LOCATION_NAME,
       LAT,
       LON,
       "localtime",
       TEMP_F,
       WIND_MPH,
       WIND_DIR,
       PRECIP_IN,
       HUMIDITY,
       CLOUD AS CLOUDINESS,
       CONDITION,
       UV,
       GUST_KPH,
FROM {{ source('RAW', 'CALIFORNIA_ZIP_CODE_WEATHER_DATA') }}