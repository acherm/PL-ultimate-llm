-- Fjord: Streaming sensor query with sliding window aggregation
-- UC Berkeley Database Group, 2003

CREATE STREAM SensorReadings (
  sensor_id  INTEGER,
  location   VARCHAR(64),
  temp       FLOAT,
  humidity   FLOAT,
  ts         TIMESTAMP
);

SELECT sensor_id,
       location,
       AVG(temp)     AS avg_temp,
       AVG(humidity) AS avg_humidity,
       COUNT(*)      AS num_readings
FROM SensorReadings [RANGE 60 SECONDS SLIDE 10 SECONDS]
WHERE temp > 20.0
GROUP BY sensor_id, location
HAVING AVG(temp) > 25.0;
