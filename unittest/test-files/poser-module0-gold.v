module module0(clk, rst_n, bar, foo);
  input clk, rst_n;
  input [1:0] bar;
  output [1:0] foo;

  parameter width_in = 2;
  parameter width_out = 2;

  wire [width_in-1:0] inputs;
  wire [width_out-1:0] outputs;

  assign inputs[1:0] = bar;
  assign foo = outputs[1:0];

  assign outputs = { out_d0_w0 , out_d0_w1 };
  assign '{ in_d0_w0 , in_d0_w1 } = inputs;

  poserCell pc_d0_w0 #(.type(0)) (.clk(clk), .rst_n(rst_n), ^{ tied , in_d0_w0 }, out_d0_w0);
  poserCell pc_d0_w1 #(.type(0)) (.clk(clk), .rst_n(rst_n), ^{ out_d0_w0 , in_d0_w1 }, out_d0_w1);
endmodule
