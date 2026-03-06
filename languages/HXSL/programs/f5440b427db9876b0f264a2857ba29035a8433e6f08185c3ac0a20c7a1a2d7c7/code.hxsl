class ColorShader extends hxsl.Shader {
    static var SRC = {
        @input var input : {
            pos : Vec3,
            uv : Vec2,
        };
        var output : {
            pos : Vec4,
            color : Vec4,
        };
        var color : Vec3;

        function vertex() {
            output.pos = vec4(input.pos, 1.0);
        }

        function fragment() {
            output.color = vec4(color, 1.0);
        }
    };
}
