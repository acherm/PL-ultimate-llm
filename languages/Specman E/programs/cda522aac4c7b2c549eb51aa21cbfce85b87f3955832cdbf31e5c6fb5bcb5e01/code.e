<'
// Packet struct with randomization constraints
struct packet {
  %length : uint(bits:8);
  %data   : list of uint(bits:8);

  keep length in [1..15];
  keep data.size() == length;
};

extend sys {
  run() is also {
    var p : packet;
    gen p;
    out("Packet length: ", p.length);
    out("Data bytes: ", p.data);
  };
};
'>
