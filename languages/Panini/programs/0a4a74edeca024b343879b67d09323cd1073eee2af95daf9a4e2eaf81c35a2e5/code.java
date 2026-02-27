capsule Greeter(String name) {
    void greet() {
        System.out.println("Hello, " + name + "!");
    }
}

capsule Main {
    design {
        Greeter g;
        g("World");
    }
    void run() {
        g.greet();
    }
}
