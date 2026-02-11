#import <Foundation/Foundation.h>
#include <vector>
#include <iostream>

int main() {
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];

    // C++ STL vector
    std::vector<int> numbers = {1, 2, 3, 4, 5};

    // Objective-C NSString
    NSString *message = @"Sum: ";

    // Calculate sum using C++
    int sum = 0;
    for (int num : numbers) {
        sum += num;
    }

    // Print using Objective-C and C++
    std::cout << [message UTF8String] << sum << std::endl;

    [pool drain];
    return 0;
}
