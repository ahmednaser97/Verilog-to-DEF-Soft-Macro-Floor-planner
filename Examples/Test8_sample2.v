module rca4 (a, b, ci, s, co);

input ci;
output co;
input [1:0] a;
input [1:0] b;
output [2:0] s;

wire vdd = 1'b1;
wire gnd = 1'b0;

BUFX2 BUFX2_1 ( .A(fa0_s), .Y(s[0]) );
BUFX2 BUFX2_2 ( .A(fa1_s), .Y(s[1]) );
BUFX2 BUFX2_3 ( .A(fa2_s), .Y(s[2]) );
BUFX2 BUFX2_5 ( .A(_0_), .Y(co) );
INVX1 INVX1_1 ( .A(b[0]), .Y(_4_) );
OR2X2 OR2X2_1 ( .A(ci), .B(a[0]), .Y(_5_) );
NAND2X1 NAND2X1_1 ( .A(ci), .B(a[0]), .Y(_6_) );
NAND3X1 NAND3X1_1 ( .A(_4_), .B(_6_), .C(_5_), .Y(_7_) );
NOR2X1 NOR2X1_1 ( .A(ci), .B(a[0]), .Y(_1_) );
AND2X2 AND2X2_1 ( .A(ci), .B(a[0]), .Y(_2_) );
OAI21X1 OAI21X1_1 ( .A(_1_), .B(_2_), .C(b[0]), .Y(_3_) );
NAND2X1 NAND2X1_2 ( .A(_3_), .B(_7_), .Y(fa0_s) );
OAI21X1 OAI21X1_2 ( .A(_4_), .B(_1_), .C(_6_), .Y(c1) );
INVX1 INVX1_2 ( .A(b[1]), .Y(_11_) );
OR2X2 OR2X2_2 ( .A(c1), .B(a[1]), .Y(_12_) );
NAND2X1 NAND2X1_3 ( .A(c1), .B(a[1]), .Y(_13_) );
NAND3X1 NAND3X1_2 ( .A(_11_), .B(_13_), .C(_12_), .Y(_14_) );
NOR2X1 NOR2X1_2 ( .A(c1), .B(a[1]), .Y(_8_) );
AND2X2 AND2X2_2 ( .A(c1), .B(a[1]), .Y(_9_) );
OAI21X1 OAI21X1_3 ( .A(_8_), .B(_9_), .C(b[1]), .Y(_10_) );
NAND2X1 NAND2X1_4 ( .A(_10_), .B(_14_), .Y(fa1_s) );
OAI21X1 OAI21X1_4 ( .A(_11_), .B(_8_), .C(_13_), .Y(c2) );
NAND2X1 NAND2X1_8 ( .A(_24_), .B(_28_), .Y(fa3_s) );
OAI21X1 OAI21X1_8 ( .A(_25_), .B(_22_), .C(_27_), .Y(_0_) );
endmodule
