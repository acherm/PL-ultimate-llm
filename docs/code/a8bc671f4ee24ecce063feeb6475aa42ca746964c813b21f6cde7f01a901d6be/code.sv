// This is an example of a simple register with synchronous reset
module simple_register (
    input  logic        clk,
    input  logic        rst_n,
    input  logic [7:0]  data_in,
    output logic [7:0]  data_out
);

    always_ff @(posedge clk) begin
        if (!rst_n)
            data_out <= 8'b0;
        else
            data_out <= data_in;
    end

endmodule