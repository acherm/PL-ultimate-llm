#include <systemc.h>

SC_MODULE(counter) {
  sc_in<bool> clk;
  sc_in<bool> reset;
  sc_out<int> count;

  int count_val;

  void count_up() {
    if (reset.read()) {
      count_val = 0;
    } else {
      count_val++;
    }
    count.write(count_val);
  }

  SC_CTOR(counter) {
    count_val = 0;
    SC_METHOD(count_up);
    sensitive << clk.pos();
  }
};

int sc_main(int argc, char* argv[]) {
  sc_signal<bool> clk;
  sc_signal<bool> reset;
  sc_signal<int> count;

  counter counter1("Counter1");
  counter1.clk(clk);
  counter1.reset(reset);
  counter1.count(count);

  sc_start(100, SC_NS);

  return 0;
}
