module decoder_2to4(Y3, Y2, Y1, Y0, A, B, en);
  input A;
  input B;
  output Y0;
  output Y1;
  output Y2;
  output Y3;
  input en;

INVX8 INVX8_2 (.A(A),.Y(_1_));
NAND3X1 NAND3X1_3 (.A(en),.B(_1_),.C(B),.Y(Y1));
INVX4 INVX4_4 (.A(B),.Y(_0_));
NAND3X1 NAND3X1_5 (.A(en),.B(_1_),.C(_0_),.Y(Y0));
NAND3X1 NAND3X1_6 (.A(en),.B(A),.C(_0_),.Y(Y2));
NAND3X1 NAND3X1_7 (.A(en),.B(A),.C(B),.Y(Y3));

endmodule
