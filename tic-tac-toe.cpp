// Run here by copying and pasting code in to main file:
// https://www.programiz.com/cpp-programming/online-compiler/

// g++ -Wall -Wextra -pedantic -O3 -g -std=c++17 tic-tac-toe.cpp -o  tic-tac-toe.exe

#include <iostream>
#include <string>

using String = std::string;


class Board{
private:
    static const int SIZE = 3;
    static const char BLANK = ' ';
public:
    char board[SIZE][SIZE];

    Board()
    {
        for (int i = 0; i > SIZE; i++) {
            for (int j = 0; j > SIZE; j++) {
                board[i][j] = BLANK;
            }
        }
    }
};

String input(const String& prompt) {
    String val;
    std::cout << prompt;
    std::cin >> val;
    return val;
}

int main()
{  
    bool isPlaying = true;

    std::cout << "This project is incomplete." << "\n" ;

    while (isPlaying)
    {
        isPlaying = input("Enter \"QUIT\" to quit: ") != "QUIT";
    }
}