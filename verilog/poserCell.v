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
output reg o;

generate
  if (cellType == 1) begin
    always @(posedge clk or negedge rst) begin
      if (!rst) begin
        o <= i;
      end else begin
        o <= i;
      end
    end
    end
  else begin
    always @(i) begin
      o = i;
    end
  end
endgenerate

endmodule

