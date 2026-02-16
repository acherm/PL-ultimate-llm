-- Simple register example in L3
-- Defining a register file

type regType = bits(32)

construct reg { R0 R1 R2 R3 R4 R5 R6 R7 }

declare
{
   GPR :: reg -> regType
   PC :: regType
}

component GPR(n::reg) :: regType
{
   value = match n
   {
      case R0 => 0
      case _ => #GPR(n)
   }
   return value
}