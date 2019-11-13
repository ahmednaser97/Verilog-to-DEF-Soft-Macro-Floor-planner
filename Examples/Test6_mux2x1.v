module mux2x1 (a, b, sel, y);

input [1:0] a;
input [1:0] b;
input [1:0] sel;
output [1:0] y;

wire vdd = 1'b1;
wire gnd = 1'b0;

INVX1 INVX1_1 ( .A(sel[0]), .Y(_1_) );
NAND2X1 NAND2X1_1 ( .A(_3_), .B(_6_), .Y(_11__1_) );
AOI22X1 AOI22X1_1 ( .A(a[1]), .B(_4_), .C(b[1]), .Y(_6_) );
endmodule
