module poserMux
(
  i,
  o
);

parameter poser_mux_width_in = 8;
parameter poser_select_width = $ceil(poser_mux_width_in)-1;

input [poser_mux_width_in-1:0] i;
output reg o;

wire [poser_select_width-1:0] s;
assign s = i[poser_select_width-1:0];

always @(i) begin
  if (s > poser_mux_width_in-1) begin
    o = i[poser_mux_width_in-1];
  end else begin
    o = i[s];
  end
end

endmodule

