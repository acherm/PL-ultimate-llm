var i, prime, count = 0, SieveSize = 8191, flags = [SieveSize : 1];
for (i = 0; i < SieveSize; i++)
  if (flags[i]) {
    prime = i + i + 3;
    flags[i + prime:SieveSize:prime] = 0;
    count++;
  }
putln (count);
