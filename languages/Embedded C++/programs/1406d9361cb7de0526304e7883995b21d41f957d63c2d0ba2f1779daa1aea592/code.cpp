// Simple embedded system LED blink class
class LED {
private:
    volatile unsigned int* port;
    unsigned int pin;

public:
    LED(volatile unsigned int* p, unsigned int n) : port(p), pin(n) {
        *port |= (1 << pin);  // Set pin as output
    }

    void on() {
        *port |= (1 << pin);
    }

    void off() {
        *port &= ~(1 << pin);
    }

    void toggle() {
        *port ^= (1 << pin);
    }
};

// Usage
int main() {
    LED led((volatile unsigned int*)0x12345678, 5);

    while(1) {
        led.on();
        for(volatile int i = 0; i < 100000; i++);
        led.off();
        for(volatile int i = 0; i < 100000; i++);
    }

    return 0;
}
