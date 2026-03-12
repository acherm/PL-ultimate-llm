#include <systemc-ams>

// TDF module: first-order RC low-pass filter
SCA_TDF_MODULE(rc_lpf) {
    sca_tdf::sca_in<double>  inp;  // input signal
    sca_tdf::sca_out<double> out;  // filtered output

    double tau;     // RC time constant (seconds)
    double y_prev;  // previous output sample

    SCA_CTOR(rc_lpf) : inp("inp"), out("out"), tau(1.0e-3), y_prev(0.0) {}

    void set_attributes() {
        // Set simulation timestep to 10 microseconds
        set_timestep(10.0, sc_core::SC_US);
    }

    void initialize() {
        y_prev = 0.0;
    }

    void processing() {
        double dt = get_timestep().to_seconds();
        double alpha = dt / (tau + dt);
        double y = alpha * inp.read() + (1.0 - alpha) * y_prev;
        out.write(y);
        y_prev = y;
    }
};

int sc_main(int argc, char* argv[]) {
    sca_tdf::sca_signal<double> sig_in, sig_out;

    rc_lpf filter("filter");
    filter.inp(sig_in);
    filter.out(sig_out);

    // Create trace file for output
    sca_util::sca_trace_file* tf =
        sca_util::sca_create_tabular_trace_file("rc_lpf_trace.dat");
    sca_util::sca_trace(tf, sig_in,  "input");
    sca_util::sca_trace(tf, sig_out, "output");

    sc_core::sc_start(1.0, sc_core::SC_MS);

    sca_util::sca_close_tabular_trace_file(tf);
    return 0;
}
