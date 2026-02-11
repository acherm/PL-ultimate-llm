#include <core.p4>

header ethernet_t {
    bit<48> dst_addr;
    bit<48> src_addr;
    bit<16> eth_type;
}

struct Headers {
    ethernet_t eth_hdr;
}

struct Metadata {
}

parser MyParser(packet_in pkt,
                out Headers hdr,
                inout Metadata meta,
                inout standard_metadata_t stdmeta) {
    state start {
        pkt.extract(hdr.eth_hdr);
        transition accept;
    }
}

control MyVerifyChecksum(inout Headers hdr, inout Metadata meta) {
    apply { }
}

control MyIngress(inout Headers hdr,
                  inout Metadata meta,
                  inout standard_metadata_t stdmeta) {
    apply { }
}

control MyEgress(inout Headers hdr,
                  inout Metadata meta,
                  inout standard_metadata_t stdmeta) {
    apply { }
}

control MyComputeChecksum(inout Headers hdr, inout Metadata meta) {
    apply { }
}

control MyDeparser(packet_out pkt, in Headers hdr) {
    apply {
        pkt.emit(hdr.eth_hdr);
    }
}

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;