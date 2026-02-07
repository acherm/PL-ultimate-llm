import "ecere"

class HelloWorldApp : GuiApplication
{
   void Main()
   {
      MessageBox { contents = "Hello, World!" }.Modal();
   }
}