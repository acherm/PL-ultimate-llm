-- SCOOP (Simple Concurrent Object-Oriented Programming) example
-- Demonstrates parallel execution with separate concurrent objects
-- Source: EiffelStudio SCOOP examples and documentation

class COUNTER
feature
    value: INTEGER

    increment
        do
            value := value + 1
        end

    add (n: INTEGER)
        do
            value := value + n
        end
end

class APPLICATION
create
    make

feature
    make
            -- Create two separate (concurrent) counters and drive them in parallel
        local
            c1: separate COUNTER
            c2: separate COUNTER
        do
            create c1
            create c2
            bump (c1)
            bump (c1)
            bump (c1)
            bump (c2)
            bump (c2)
            io.put_string ("Counter 1: ")
            io.put_integer (snapshot (c1))
            io.put_new_line
            io.put_string ("Counter 2: ")
            io.put_integer (snapshot (c2))
            io.put_new_line
        end

    bump (c: separate COUNTER)
            -- Asynchronously increment c; call is queued on c's handler
        do
            c.increment
        end

    snapshot (c: separate COUNTER): INTEGER
            -- Wait for all pending calls on c, then return its value
        do
            Result := c.value
        end
end
