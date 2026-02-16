using EFL;

public class HelloWorld : Evas.Object
{
    public HelloWorld()
    {
        Elm.init();

        var win = new Elm.Win(null, "hello", Elm.WinType.BASIC);
        win.title_set("Hello World");
        win.autodel_set(true);

        var label = new Elm.Label(win);
        label.text = "Hello, World!";
        label.size_hint_weight_set(1.0, 1.0);
        win.resize_object_add(label);
        label.show();

        win.resize(300, 200);
        win.show();

        Elm.run();
    }

    public static int main(string[] args)
    {
        new HelloWorld();
        return 0;
    }
}
