%% Lasp G-Counter example
%% Demonstrates basic CRDT operations with Lasp distributed programming

%% Declare a G-Counter variable
{ok, {Counter, _, _, _}} = lasp:declare({<<"gcounter">>, state_gcounter},
                                         state_gcounter),

%% Perform updates (increments)
ok = lasp:update(Counter, increment, actor1),
ok = lasp:update(Counter, increment, actor2),
ok = lasp:update(Counter, increment, actor1),

%% Read the current value
{ok, {_, _, _, CounterValue}} = lasp:read(Counter, undefined),

%% Display the result
io:format("Counter value: ~p~n", [lasp:query(CounterValue)]).
