// Initial beliefs
temperature(20).
humidity(50).

// Initial goal
!monitor_environment.

// Plan to achieve the goal
+!monitor_environment : temperature(T) & T > 25
  <- .print("Warning: Temperature is high: ", T);
     !check_humidity.

+!monitor_environment : temperature(T) & T <= 25
  <- .print("Temperature is normal: ", T);
     !check_humidity.

// Plan to check humidity
+!check_humidity : humidity(H) & H > 70
  <- .print("Warning: Humidity is high: ", H).

+!check_humidity : humidity(H) & H <= 70
  <- .print("Humidity is normal: ", H).

// React to temperature changes
+temperature(T) : T > 25
  <- .print("Temperature changed to high: ", T).
