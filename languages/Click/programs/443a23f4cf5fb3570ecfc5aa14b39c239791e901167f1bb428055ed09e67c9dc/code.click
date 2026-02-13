// Simple IP router configuration
// Reads packets from eth0, classifies, and forwards

FromDevice(eth0)
  -> classifier :: Classifier(12/0806 20/0001,
                              12/0806 20/0002,
                              12/0800,
                              -);

// ARP queries
classifier[0]
  -> ARPResponder(10.0.0.1 00:11:22:33:44:55)
  -> ToDevice(eth0);

// ARP responses
classifier[1]
  -> [1]arpQuerier :: ARPQuerier(10.0.0.1, 00:11:22:33:44:55);

// IP packets
classifier[2]
  -> Strip(14)
  -> CheckIPHeader
  -> rt :: RadixIPLookup(10.0.0.1/32 0,
                         10.0.0.0/24 0,
                         0.0.0.0/0 1);

// Local delivery
rt[0]
  -> IPPrint("local")
  -> Discard;

// Forward to next hop
rt[1]
  -> DecIPTTL
  -> IPPrint("forward")
  -> [0]arpQuerier;

arpQuerier[0]
  -> EtherEncap(0x0800, 00:11:22:33:44:55, ff:ff:ff:ff:ff:ff)
  -> ToDevice(eth0);

// Unclassified packets
classifier[3]
  -> Discard;
