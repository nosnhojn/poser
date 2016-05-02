module poserCell
(
  clk,
  rst,
  i,
  o
);

parameter cellType = 0;
parameter activeRst = 0;

input clk;
input rst;
input i;
output wire o;

generate
  if (cellType == 0) begin
    reg o_i;
    assign o = o_i;
    always @(posedge clk or negedge rst) begin
      if (!rst) begin
        o_i <= i;
      end else begin
        o_i <= i;
      end
    end
    end
  else begin
    assign o = i;
  end
endgenerate

endmodule

