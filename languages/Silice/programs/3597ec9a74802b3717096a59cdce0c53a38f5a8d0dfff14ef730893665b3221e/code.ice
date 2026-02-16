algorithm main(
  output uint1 led
) <autorun> {
  uint28 counter = 0;

  while (1) {
    led = counter[27,1];
    counter = counter + 1;
  }
}
