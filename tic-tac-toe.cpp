// Run here by copying and pasting code in to main file:
// https://www.programiz.com/cpp-programming/online-compiler/

// THIS PROJECT IS NOT COMPLETE

#include <iostream>
#include <string>

using String = std::string;


class Board{
private:
    static const int SIZE = 3;
public:
    char board[3][3];

    Board()
    {
        
    }
};


int main()
{  
    bool isPlaying = true;
    String shouldPlayAgien;

    std::cout << "This project is incomplete." << "\n" ;

    while (isPlaying)
    {
        std::cout << "Enter \"QUIT\" to quit: ";
        std::cin >> shouldPlayAgien;
        isPlaying = shouldPlayAgien != "QUIT";
        
    }
}