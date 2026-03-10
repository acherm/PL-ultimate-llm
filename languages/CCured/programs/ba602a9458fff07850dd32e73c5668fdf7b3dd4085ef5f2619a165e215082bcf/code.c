/* CCured: type-safe C with safe pointer arithmetic
 * CCured retrofits legacy C code with type safety by inferring
 * pointer kinds (SAFE, SEQ, WILD) and inserting runtime checks.
 */
#include <stdio.h>
#include <string.h>

/* Reverse a string in place using safe sequential pointers */
void reverse(char *s, int len) {
    int i, j;
    char tmp;
    for (i = 0, j = len - 1; i < j; i++, j--) {
        tmp = s[i];
        s[i] = s[j];
        s[j] = tmp;
    }
}

/* Compute the length of a string */
int my_strlen(const char *s) {
    int n = 0;
    while (s[n] != '\0') n++;
    return n;
}

int main(void) {
    char buf[] = "Hello, CCured!";
    int len = my_strlen(buf);

    printf("Original: %s\n", buf);
    reverse(buf, len);
    printf("Reversed: %s\n", buf);

    /* Demonstrate safe array access */
    int arr[5] = {10, 20, 30, 40, 50};
    int i, total = 0;
    for (i = 0; i < 5; i++) {
        total += arr[i];
    }
    printf("Array sum: %d\n", total);

    return 0;
}
