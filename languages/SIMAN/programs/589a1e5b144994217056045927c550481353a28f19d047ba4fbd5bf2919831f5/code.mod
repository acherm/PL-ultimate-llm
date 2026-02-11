BEGIN;
CREATE: EX(1);        -- Create entities with exponential interarrival time
QUEUE, WaitLine;      -- Place entities in queue
SEIZE: Server;        -- Seize the server resource
DELAY: UN(2,4);       -- Service time uniformly distributed between 2 and 4
RELEASE: Server;      -- Release the server
COUNT: TotalServed;   -- Count entities served
DISPOSE;              -- Dispose of entities
END;
