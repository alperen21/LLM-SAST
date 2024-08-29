#include <iostream>
#include <cstdlib>

void vulnerableFunction() {
    int* ptr = (int*)malloc(sizeof(int));  // Dynamically allocate memory
    if (ptr == nullptr) {
        std::cerr << "Memory allocation failed" << std::endl;
        return;
    }

    *ptr = 42;  // Assign a value to the allocated memory

    free(ptr);  // Free the allocated memory

    // Double-free vulnerability: freeing the memory again
    free(ptr);
}

int main() {
    vulnerableFunction();
    return 0;
}