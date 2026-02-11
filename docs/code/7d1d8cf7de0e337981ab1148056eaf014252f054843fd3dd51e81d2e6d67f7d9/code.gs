[indent=4]
init
    Gtk.init(ref args)

    var window = new Gtk.Window(Gtk.WindowType.TOPLEVEL)
    window.title = "Hello, World!"
    window.border_width = 10
    window.window_position = Gtk.WindowPosition.CENTER
    window.set_default_size(350, 70)

    var button = new Gtk.Button.with_label("Click me!")
    button.clicked.connect(on_button_clicked)

    window.add(button)
    window.destroy.connect(Gtk.main_quit)

    window.show_all()
    Gtk.main()

def on_button_clicked(button: Gtk.Button)
    print "Hello World!"