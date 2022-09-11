#include <iostream>
#include <string>

using String = std::string;


class Board{
private:
    static const int s_DEFAULT_SIZE = 3;
public:
    int width;
    int height;
    int size;

    Board(int width = s_DEFAULT_SIZE, int height = s_DEFAULT_SIZE)
        : width(width), height(height), size(width * height)
    {
        
    }
};


int main()
{  
    bool isPlaying = true;
    String shouldPlayAgien;

    while (isPlaying)
    {
        std::cout << "Enter \"QUIT\" to quit: ";
        std::cin >> shouldPlayAgien;
        isPlaying = shouldPlayAgien != "QUIT";
        
    }
}