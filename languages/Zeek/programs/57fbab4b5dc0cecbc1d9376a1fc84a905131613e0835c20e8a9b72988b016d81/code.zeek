# Simple connection logger in Zeek
# Logs basic information about network connections

@load base/protocols/conn

event connection_state_remove(c: connection)
{
    local id = c$id;
    local orig = id$orig_h;
    local resp = id$resp_h;
    local sport = id$orig_p;
    local dport = id$resp_p;

    if ( c$conn$proto == tcp )
    {
        print fmt("TCP Connection: %s:%s -> %s:%s", orig, sport, resp, dport);
    }
    else if ( c$conn$proto == udp )
    {
        print fmt("UDP Connection: %s:%s -> %s:%s", orig, sport, resp, dport);
    }
}

event zeek_init()
{
    print "Connection logger started";
}

event zeek_done()
{
    print "Connection logger finished";
}