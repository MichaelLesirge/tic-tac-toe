// Run here by copying and pasting code in to main file:
// https://www.programiz.com/cpp-programming/online-compiler/

// THIS PROJECT IS NOT COMPLETE

#include <iostream>
#include <string>

using String = std::string;


class Board{
private:
    static const int s_DEFAULT_SIZE = 3;
public:
    const int width;
    const int height;
    const int size;

    Board(int width = s_DEFAULT_SIZE, int height = s_DEFAULT_SIZE)
        : width(width), height(height), size(width * height)
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