module module2(clk_, rst_, bar0, bar1, foo0, foo1);
  input clk_;
  input rst_;
  input [1:0] bar0;
  input [1:0] bar1;
  output [1:0] foo0;
  output [1:0] foo1;
  parameter poser_tied = 1'b1;
  parameter poser_width_in = 0+1-0+1+1-0+1;
  parameter poser_width_out = 0+1-0+1+1-0+1;
  parameter poser_grid_width = 5;
  parameter poser_grid_depth = 9;
  parameter [poser_grid_width-1:0] cellTypes [0:poser_grid_depth-1] = '{ 5'b11111,5'b11111,5'b11111,5'b11111,5'b11111,5'b11111,5'b11111,5'b11111,5'b11111 };
  wire [poser_width_in-1:0] poser_inputs;
  assign poser_inputs = { bar0,bar1 };
  wire [poser_width_out-1:0] poser_outputs;
  assign { foo0,foo1 } = poser_outputs;
  wire [poser_grid_width-1:0] poser_grid_output [0:poser_grid_depth-1];
  assign poser_outputs = poser_grid_output[poser_grid_depth-1];

  wire poser_clk;
  assign poser_clk = clk_;
  wire poser_rst;
  assign poser_rst = rst_;
  for (genvar D = 0; D < poser_grid_depth; D++) begin
    for (genvar W = 0; W < poser_grid_width; W++) begin
      if (D == 0) begin
        if (W == 0) begin
          poserCell #(.cellType(cellTypes[D][W]), .activeRst(0)) pc (.clk(poser_clk),
                                                                     .rst(poser_rst),
                                                                     .i(^{ poser_tied ,
                                                                           poser_inputs[W%poser_grid_width] }),
                                                                     .o(poser_grid_output[D][W]));
        end else begin
          poserCell #(.cellType(cellTypes[D][W]), .activeRst(0)) pc (.clk(poser_clk),
                                                                     .rst(poser_rst),
                                                                     .i(^{ poser_grid_output[D][W-1],
                                                                           poser_inputs[W%poser_grid_width] }),
                                                                     .o(poser_grid_output[D][W]));
        end
      end else begin
        if (W == 0) begin
          poserCell #(.cellType(cellTypes[D][W]), .activeRst(0)) pc (.clk(poser_clk),
                                                                     .rst(poser_rst),
                                                                     .i(^{ poser_grid_output[D-1][W],
                                                                           poser_grid_output[D-1][poser_grid_depth-1] }),
                                                                     .o(poser_grid_output[D][W]));
        end else begin
          poserCell #(.cellType(cellTypes[D][W]), .activeRst(0)) pc (.clk(poser_clk),
                                                                     .rst(poser_rst),
                                                                     .i(^{ poser_grid_output[D-1][W],
                                                                           poser_grid_output[D][W-1] }),
                                                                     .o(poser_grid_output[D][W]));
        end
      end
    end
  end
endmodule
