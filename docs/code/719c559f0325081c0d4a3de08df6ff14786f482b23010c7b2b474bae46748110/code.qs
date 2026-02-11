namespace HelloWorld {
    open Microsoft.Quantum.Diagnostics;

    @EntryPoint()
    operation HelloWorld() : Unit {
        Message("Hello, quantum world!");
    }
}