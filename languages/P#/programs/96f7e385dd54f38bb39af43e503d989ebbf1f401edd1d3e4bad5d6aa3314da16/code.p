event Ping;
event Pong;

machine Server
{
    start state Init
    {
        on Ping do { send(payload as machine, Pong); }
    }
}

machine Client
{
    start state Init
    {
        entry
        {
            var server = create(Server);
            send(server, Ping, this);
        }

        on Pong do { raise halt; }
    }
}