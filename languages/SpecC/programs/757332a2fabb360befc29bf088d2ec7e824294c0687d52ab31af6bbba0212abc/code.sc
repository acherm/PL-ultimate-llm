behavior Main {
    void main(void) {
        int x, y;

        x = 10;
        y = 20;

        par {
            {
                x = x + 5;
                printf("Process 1: x = %d\n", x);
            }
            {
                y = y * 2;
                printf("Process 2: y = %d\n", y);
            }
        }

        printf("Final: x = %d, y = %d\n", x, y);
    }
}
