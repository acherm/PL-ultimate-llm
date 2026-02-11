/* Simple robot control program */
void main() {
    int sensor_value;

    printf("Robot started\n");

    while(1) {
        sensor_value = analog(0);

        if (sensor_value > 128) {
            motor(0, 100);
            motor(1, 100);
        } else {
            motor(0, 50);
            motor(1, -50);
        }

        msleep(100);
    }
}
