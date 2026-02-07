import com.ms.wfc.app.*;
import com.ms.wfc.core.*;
import com.ms.wfc.ui.*;
import com.ms.wfc.html.*;

public class HelloWorld extends Form
{
    public HelloWorld()
    {
        super();
        this.setText("Visual J++ Application");
        this.setSize(new Point(300, 200));

        Label label = new Label();
        label.setText("Hello, World!");
        label.setLocation(new Point(100, 80));
        this.add(label);
    }

    public static void main(String[] args)
    {
        Application.run(new HelloWorld());
    }
}