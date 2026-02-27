.assembly HelloWorld {}
.assembly extern mscorlib {}

.class public auto ansi beforefieldinit HelloWorld
       extends [mscorlib]System.Object
{
  .method public hidebysig static void Main(string[] args) cil managed
  {
    .entrypoint
    .maxstack 1
    ldstr "Hello, World!"
    call void [mscorlib]System.Console::WriteLine(string)
    ret
  }

  .method public hidebysig specialname rtspecialname instance void .ctor() cil managed
  {
    .maxstack 1
    ldarg.0
    call instance void [mscorlib]System.Object::.ctor()
    ret
  }
}
