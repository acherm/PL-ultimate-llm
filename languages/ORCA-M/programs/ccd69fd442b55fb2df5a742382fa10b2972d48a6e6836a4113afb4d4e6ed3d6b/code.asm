         case  on
         mcopy hello.macros

hello    start
         using HelloData

         phb
         phk
         plb

         pea   0
         pea   ^message
         pea   message
         _WriteCString

         plb
         rtl

HelloData data
message  dc    c'Hello, World!',h'0d00'
         end
