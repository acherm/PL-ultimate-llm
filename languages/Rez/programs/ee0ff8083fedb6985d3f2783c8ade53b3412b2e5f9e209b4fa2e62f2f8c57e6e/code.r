resource 'ALRT' (128, "Alert Dialog") {
    {40, 40, 140, 340},
    128,
    {
        OK, visible, sound1,
        OK, visible, sound1,
        OK, visible, sound1,
        OK, visible, sound1
    },
    centerMainScreen
};

resource 'DITL' (128) {
    {
        {70, 10, 90, 90},
        Button {
            enabled,
            "OK"
        };
        {10, 10, 60, 290},
        StaticText {
            disabled,
            "Hello from Rez!"
        }
    }
};