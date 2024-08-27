#include <cstring>
#include <iostream>

void copyInput(char* input) {
    char buffer[10];
    strcpy(buffer, input);
}

int main() {
    char userInput[100];

    std::cout << 'Enter text: ';
    std::cin >> userInput;

    copyInput(userInput);

    std::cin >> userInput;

    return 0;
}