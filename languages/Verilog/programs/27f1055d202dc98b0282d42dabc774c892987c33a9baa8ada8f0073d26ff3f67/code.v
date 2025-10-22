module counter(clk, rst, count);
input clk, rst;
output [3:0] count;
reg [3:0] count;

always @(posedge clk or posedge rst)
begin
    if (rst)
        count <= 4'b0000;
    else
        count <= count + 1;
end
endmodule