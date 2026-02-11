using Gtk;

public class HelloWorld : Window {
    public HelloWorld() {
        this.title = "Hello World";
        this.window_position = WindowPosition.CENTER;
        this.destroy.connect(Gtk.main_quit);
        this.set_default_size(350, 70);

        var label = new Label("Hello World!");
        this.add(label);
    }

    public static int main(string[] args) {
        Gtk.init(ref args);

        var window = new HelloWorld();
        window.show_all();

        Gtk.main();
        return 0;
    }
}