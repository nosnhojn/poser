module module0(clk_, rst_, bar, foo);
  input clk_;
  input rst_;
  input [1:0] bar;
  output [1:0] foo;
  parameter poser_tied = 1'b1;
  parameter poser_width_in = 0+1-0+1;
  parameter poser_width_out = 0+1-0+1;
  parameter poser_grid_width = 2;
  parameter poser_grid_depth = 1;
  wire [poser_width_in-1:0] poser_inputs;
  assign poser_inputs = { bar };
  wire [poser_width_out-1:0] poser_outputs;
  assign '{ foo } = poser_outputs;
  wire [poser_grid_width-1:0] poser_grid_output [0:poser_grid_depth-1];
  assign poser_outputs = poser_grid_output[poser_grid_depth-1];

  for (genvar D = 0; D < poser_grid_depth; D++) begin
    for (genvar W = 0; W < poser_grid_width; W++) begin
      if (D == 0) begin
        if (W == 0) begin
          poserCell pc #(.type(0), .active(0)) (.clk(clk), .rst(rst), ^{ poser_tied , poser_inputs[W] }, poser_grid_output[D][W]);
        end else begin
          poserCell pc #(.type(0), .active(0)) (.clk(clk), .rst(rst), ^{ poser_grid_output[D][W-1] , poser_inputs[D][W] }, poser_grid_output[D][W]);
        end
      end
    end
  end
endmodule
