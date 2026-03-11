// MultiJava: multiple dispatch example
// Shapes hierarchy with area computed via multi-methods

class Shape {
    String name() { return "Shape"; }
}

class Circle extends Shape {
    double radius;
    Circle(double r) { radius = r; }
    String name() { return "Circle"; }
}

class Square extends Shape {
    double side;
    Square(double s) { side = s; }
    String name() { return "Square"; }
}

// Multi-method specialization using MultiJava @-syntax
double area(Shape@Circle c) { return Math.PI * c.radius * c.radius; }
double area(Shape@Square s) { return s.side * s.side; }
double area(Shape s) { return 0.0; }

class Main {
    public static void main(String[] args) {
        Shape[] shapes = { new Circle(5.0), new Square(4.0) };
        for (Shape s : shapes) {
            System.out.println(s.name() + " area: " + area(s));
        }
    }
}
