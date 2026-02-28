//
// Simple Aloha network model in NED (OMNeT++ Network Description Language)
//

simple Host
{
    parameters:
        double txRate @unit(bps);
        volatile double iaTime @unit(s);
        volatile int pkLenBits;
    gates:
        output out;
}

simple Server
{
    gates:
        input in[];
}

network Aloha
{
    parameters:
        int numHosts = default(10);
        double txRate @unit(bps) = default(9600bps);
        volatile double iaTime @unit(s);
        volatile int pkLenBits;
    submodules:
        server: Server;
        host[numHosts]: Host {
            txRate = txRate;
            iaTime = iaTime;
            pkLenBits = pkLenBits;
        }
    connections:
        for i=0..numHosts-1 {
            host[i].out --> server.in++;
        }
}
