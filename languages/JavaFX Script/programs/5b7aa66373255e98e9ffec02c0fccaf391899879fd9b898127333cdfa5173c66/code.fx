import javafx.stage.Stage;
import javafx.scene.Scene;
import javafx.scene.shape.Circle;
import javafx.scene.paint.Color;
import javafx.scene.text.Text;
import javafx.scene.text.Font;

Stage {
    title: "JavaFX Script Demo"
    width: 400
    height: 300
    scene: Scene {
        content: [
            Circle {
                centerX: 200
                centerY: 150
                radius: 80
                fill: Color.CORNFLOWERBLUE
                stroke: Color.DARKBLUE
                strokeWidth: 3
            },
            Text {
                x: 130
                y: 155
                content: "Hello, JavaFX!"
                font: Font {
                    size: 20
                }
                fill: Color.WHITE
            }
        ]
    }
}
