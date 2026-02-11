-module(echo_server).
-export([listen/1]).

listen(Port) ->
    {ok, Socket} = gen_tcp:listen(Port, [binary, {packet, 0}, {active, false}, {reuseaddr, true}]),
    accept(Socket).

accept(Socket) ->
    {ok, Conn} = gen_tcp:accept(Socket),
    Handler = spawn(fun () -> handle(Conn) end),
    gen_tcp:controlling_process(Conn, Handler),
    accept(Socket).

handle(Socket) ->
    case gen_tcp:recv(Socket, 0) of
        {ok, Data} ->
            gen_tcp:send(Socket, Data),
            handle(Socket);
        {error, closed} ->
            ok
    end.