// Simple register definitions in TableGen (LLVM's domain-specific language)
class Register<string name, list<string> altNames = []> {
  string AsmName = name;
  list<string> AltNames = altNames;
}

class RegisterClass<list<Register> regs, int alignment> {
  list<Register> MemberList = regs;
  int Alignment = alignment;
}

// Define individual 64-bit general-purpose registers
def X0 : Register<"x0">;
def X1 : Register<"x1">;
def X2 : Register<"x2">;
def X3 : Register<"x3">;
def X4 : Register<"x4">;
def SP : Register<"sp", ["x31"]>;

// Define a register class for 64-bit general-purpose registers
def GPR64 : RegisterClass<[X0, X1, X2, X3, X4], 64>;
