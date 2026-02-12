task main()
{
    // Move forward for 2 seconds
    motor[motorA] = 50;
    motor[motorB] = 50;
    wait1Msec(2000);

    // Turn right for 1 second
    motor[motorA] = 50;
    motor[motorB] = -50;
    wait1Msec(1000);

    // Stop motors
    motor[motorA] = 0;
    motor[motorB] = 0;
}
