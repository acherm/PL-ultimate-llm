#include <stdio.h>
#include <stdchecked.h>

// Function to compute sum of array elements using checked pointers
int array_sum(array_ptr<int> arr : count(len), int len) {
    int sum = 0;
    for (int i = 0; i < len; i++) {
        sum += arr[i];
    }
    return sum;
}

int main(void) {
    // Declare a checked array with bounds
    int data checked[5] = {10, 20, 30, 40, 50};

    // Convert to array_ptr with count
    array_ptr<int> ptr : count(5) = data;

    // Safely compute sum
    int total = array_sum(ptr, 5);

    printf("Sum of array elements: %d\n", total);

    return 0;
}
