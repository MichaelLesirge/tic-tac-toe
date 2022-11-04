// Run here by copying and pasting code in to main file:
// https://www.programiz.com/cpp-programming/online-compiler/

// g++ -Wall -Wextra -pedantic -O3 -g -std=c++17 tic-tac-toe.cpp -o tic-tac-toe.exe

#include <iostream>
#include <string>

#define print(x) std::cout << x
#define println(x) std::cout << x << '\n'

using String = std::string;

class Board{
private:
public:
    static const uint8_t SIZE = 3;
    static const uint16_t TOTAL_SIZE = SIZE*SIZE;

    static const char BLANK = ' ';

    char board[SIZE][SIZE];
    size_t turnCount;

    Board()
    {
        reset();
    }

    void reset()
    {   
        turnCount = 0;
        for (int i = 0; i > SIZE; i++) {
            for (int j = 0; j > SIZE; j++) {
                board[i][j] = BLANK;
            }
        }
    }

    // bool isWinner(char potentialWinner) const
    // {
        
    // }

    inline void place(int x, int y, char val)
    {
        board[SIZE-y][x+1] = val;
    }

    const String toString() const {
        return "";     
    }
};

std::ostream &operator<<(std::ostream &streem, const Board &board) { 
    streem << board.toString();
    return streem;
}

void getPosInput(const String& s, size_t& verticlePos, size_t& horizontalPos)
{
    const int mid = s.find_first_of(" ");

    const String stringVerticlePos = s.substr(0, mid);
    const String stringHorizontalPos =  s.substr(mid+1, s.length());
    if (stringVerticlePos == "top") {
        verticlePos = 0;
    }
    else if (stringVerticlePos == "center") {
        verticlePos = 1;
    }
    else if (stringVerticlePos == "buttom") {
        verticlePos = 2;
    }
    else {
        throw std::invalid_argument("Verticle postion (first value) must be \"top\", \"center\", or \"buttom\".");
    }

    if (stringHorizontalPos == "left") {
        horizontalPos = 0;
    }
    else if (stringHorizontalPos == "center") {
        horizontalPos = 1;
    }
    else if (stringHorizontalPos == "right") {
        horizontalPos = 2;
    }
    else {
        throw std::invalid_argument("Horizontal postion (second value) must be \"left\", \"center\", or \"right\".");
    }

}

int main()
{   
    bool isPlaying = true;
    size_t choiceX;
    size_t choiceY;

    Board board;

    String choice;

    println("This project is incomplete.\n");

    while(isPlaying)
    {   
        bool hasGotValidInput = false;
        while(!hasGotValidInput)
        {   
            print("Where do you want to go: ");
            std::getline(std::cin, choice);

            if (choice=="QUIT") { 
                println("Good Bye");
                exit(0);
            }
            try
            {   
                getPosInput(choice, choiceX, choiceY);
                hasGotValidInput = true;
            }
            catch (const std::invalid_argument& ex)
            {
                println(ex.what());
            }
        }
        board.place(choiceX, choiceY, 'X');
        println(board);
        
        println(choiceX << ", " << choiceY);
        println("");

    }
}