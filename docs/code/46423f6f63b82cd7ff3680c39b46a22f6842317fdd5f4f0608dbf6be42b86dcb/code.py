import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from System.Windows.Forms import Application, Form, Button, MessageBox
from System.Drawing import Point, Size

class HelloForm(Form):
    def __init__(self):
        self.Text = "IronPython Windows Form"
        self.Size = Size(300, 200)

        button = Button()
        button.Text = "Click Me!"
        button.Location = Point(100, 70)
        button.Click += self.on_button_click

        self.Controls.Add(button)

    def on_button_click(self, sender, args):
        MessageBox.Show("Hello from IronPython!", "Greeting")

if __name__ == "__main__":
    Application.Run(HelloForm())
