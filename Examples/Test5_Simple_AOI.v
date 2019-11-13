module AOI (A, B, C, D, F);

  input A;
  input B;
  input C;
  input D;
  output F;


OAI21X1 OAI21X1_8 ( .A(D), .B(C), .C(B), .D(A), .Y(F));
endmodule
