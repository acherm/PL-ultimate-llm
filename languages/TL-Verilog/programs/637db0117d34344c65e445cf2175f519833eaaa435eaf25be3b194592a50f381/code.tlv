\m4_TLV_version 1d: tl-x.org
\SV
   m4_makerchip_module
\TLV
   $reset = *reset;

   // A simple pipeline counter
   |count
      @1
         $cnt[7:0] = $reset ? 8'b0 : >>1$cnt + 8'b1;

   *passed = *cyc_cnt > 40;
   *failed = 1'b0;
\SV
   endmodule
