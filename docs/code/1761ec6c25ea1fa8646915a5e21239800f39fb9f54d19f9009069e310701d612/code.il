// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

.assembly extern System.Runtime
{
  .publickeytoken = (B0 3F 5F 7F 11 D5 0A 3A )
  .ver 4:2:0:0
}
.assembly extern System.Console
{
  .publickeytoken = (B0 3F 5F 7F 11 D5 0A 3A )
  .ver 4:1:0:0
}
.assembly extern mscorlib {}
.assembly StructABIRunner {}

// Verification of this test is not expected to pass.
.verifications 0

.class public auto ansi beforefieldinit StructABI extends [System.Runtime]System.Object
{
  .method public hidebysig static int32 Main() cil managed
  {
    .entrypoint
    .maxstack  2
    .locals init (int32 V_0)
    ldc.i4.s   100
    stloc.0
    call       int32 StructABIClient::Test()
    ldloc.0
    add
    stloc.0
    ldloc.0
    ret
  } // end of method StructABI::Main

  .method public hidebysig specialname rtspecialname
          instance void .ctor() cil managed
  {
    .maxstack  8
    ldarg.0
    call       instance void [System.Runtime]System.Object::.ctor()
    ret
  } // end of method StructABI::.ctor

} // end of class StructABI