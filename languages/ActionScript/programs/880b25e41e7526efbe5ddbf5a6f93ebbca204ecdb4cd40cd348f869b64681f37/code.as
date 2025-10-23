package {
    import flash.display.Sprite;
    import flash.text.TextField;
    public class Greeter extends Sprite {
        public function Greeter() {
            var txtField:TextField = new TextField();
            txtField.text = "Hello World";
            addChild(txtField);
        }
    }
}