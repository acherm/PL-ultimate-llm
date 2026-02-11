-- Create external table for log analysis
CREATE EXTERNAL TABLE web_logs (
    ip_address STRING,
    request_time STRING,
    method STRING,
    url STRING,
    protocol STRING,
    status INT,
    bytes_sent BIGINT,
    referer STRING,
    user_agent STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/web_logs';

-- Analyze traffic patterns by hour
SELECT
    hour(from_unixtime(unix_timestamp(request_time, 'dd/MMM/yyyy:HH:mm:ss'))) AS request_hour,
    COUNT(*) AS request_count,
    SUM(bytes_sent) AS total_bytes,
    AVG(bytes_sent) AS avg_bytes,
    COUNT(DISTINCT ip_address) AS unique_visitors
FROM web_logs
WHERE status = 200
GROUP BY hour(from_unixtime(unix_timestamp(request_time, 'dd/MMM/yyyy:HH:mm:ss')))
ORDER BY request_hour;
