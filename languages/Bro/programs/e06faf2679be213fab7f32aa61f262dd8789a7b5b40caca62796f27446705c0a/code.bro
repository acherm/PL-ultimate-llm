# Bro/Zeek script: Monitor and log network connections with basic statistics

global conn_count: count = 0;
global byte_total: count = 0;

event zeek_init()
{
    print "Connection monitor initialized.";
}

event new_connection(c: connection)
{
    ++conn_count;
    local id = c$id;
    print fmt("[%s] New connection #%d: %s:%s -> %s:%s",
              strftime("%H:%M:%S", network_time()),
              conn_count,
              id$orig_h, id$orig_p,
              id$resp_h, id$resp_p);
}

event connection_state_remove(c: connection)
{
    if ( c?$conn )
    {
        byte_total += c$conn$orig_bytes + c$conn$resp_bytes;
    }
}

event zeek_done()
{
    print fmt("Monitor finished. Connections: %d, Total bytes: %d",
              conn_count, byte_total);
}
