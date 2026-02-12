MODULE QueueSimulation;

FROM InOut IMPORT WriteString, WriteLn, WriteInt;
FROM Random IMPORT Uniform;

TYPE
    Customer = OBJECT
        arrivalTime: REAL;
        serviceTime: REAL;
    END;

VAR
    queue: ARRAY [1..100] OF Customer;
    queueSize: INTEGER;
    currentTime: REAL;
    totalWaitTime: REAL;

PROCEDURE InitializeQueue();
BEGIN
    queueSize := 0;
    currentTime := 0.0;
    totalWaitTime := 0.0;
END InitializeQueue;

PROCEDURE Arrive(VAR cust: Customer);
BEGIN
    INC(queueSize);
    cust.arrivalTime := currentTime;
    cust.serviceTime := Uniform(1.0, 5.0);
    WriteString("Customer arrived at time ");
    WriteInt(TRUNC(currentTime), 0);
    WriteLn;
END Arrive;

PROCEDURE Serve();
VAR
    waitTime: REAL;
BEGIN
    IF queueSize > 0 THEN
        waitTime := currentTime - queue[1].arrivalTime;
        totalWaitTime := totalWaitTime + waitTime;
        currentTime := currentTime + queue[1].serviceTime;
        DEC(queueSize);
        WriteString("Customer served. Wait time: ");
        WriteInt(TRUNC(waitTime), 0);
        WriteLn;
    END;
END Serve;

BEGIN
    InitializeQueue();
    WriteString("Queue Simulation Starting");
    WriteLn;
END QueueSimulation.
