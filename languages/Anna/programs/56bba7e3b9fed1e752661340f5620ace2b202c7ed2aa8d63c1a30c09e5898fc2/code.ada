-- Anna example: Simple stack with formal annotations
package Stack is
   type Stack_Type is private;

   procedure Push(S: in out Stack_Type; X: Integer);
   --| requires: not Full(S);
   --| modifies: S;
   --| ensures: Top(S) = X and Size(S) = Size(S'old) + 1;

   procedure Pop(S: in out Stack_Type; X: out Integer);
   --| requires: not Empty(S);
   --| modifies: S, X;
   --| ensures: X = Top(S'old) and Size(S) = Size(S'old) - 1;

   function Top(S: Stack_Type) return Integer;
   --| requires: not Empty(S);

   function Empty(S: Stack_Type) return Boolean;

   function Full(S: Stack_Type) return Boolean;

   function Size(S: Stack_Type) return Natural;

private
   Max_Size: constant := 100;
   type Stack_Array is array (1..Max_Size) of Integer;
   type Stack_Type is record
      Items: Stack_Array;
      Top_Index: Natural := 0;
   end record;
end Stack;
