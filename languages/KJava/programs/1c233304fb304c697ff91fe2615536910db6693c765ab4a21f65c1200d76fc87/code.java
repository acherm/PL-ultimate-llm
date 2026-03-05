import com.sun.kjava.*;

public class HelloSpotlet extends Spotlet {
    private Graphics g;
    private Button quitButton;
    private String message = "Hello Spotlet";

    public HelloSpotlet() {
        g = Graphics.getGraphics();
        g.clearScreen();
        quitButton = new Button("Quit", 5, 125);
        quitButton.paint();
        g.drawString(message, 5, 5, Graphics.PLAIN);
    }

    public void penDown(int x, int y) {
        if (quitButton.pressed(x, y)) {
            System.exit(0);
        }
    }

    public static void main(String[] args) {
        new HelloSpotlet().register(Spotlet.NO_EVENT_OPTIONS);
    }
}
