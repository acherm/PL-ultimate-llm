// Alice program: Simple animation
public class HelloWorld extends SScene {
    private final SBiped person = new SBiped();

    public void initializeEventListeners() {
        this.addSceneActivationListener((SceneActivationEvent e) -> {
            person.say("Hello, World!");
            person.turn(TurnDirection.RIGHT, 0.25);
            person.move(MoveDirection.FORWARD, 1.0);
        });
    }
}
