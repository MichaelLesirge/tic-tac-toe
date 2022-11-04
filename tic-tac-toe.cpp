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
    static const size_t SIZE = 3;
    static const size_t TOTAL_SIZE = SIZE*SIZE;

    static const char FILLER = '-';

    char board[SIZE][SIZE];
    size_t turnCount;

    Board()
    {
        reset();
    }

    void reset()
    {   
        turnCount = 0;
        for (size_t i = 0; i < SIZE; i++) {
            for (size_t j = 0; j < SIZE; j++) {
                board[i][j] = FILLER;
            }
        }
    }

    // bool isWinner(char potentialWinner) const
    // {
        
    // }

    inline void place(size_t x, size_t y, char val)
    {
        board[y][x] = val;
    }

    const String toString() const {
        String out = "";
        for (size_t i = 0; i < SIZE; i++)
        {
            for (size_t j = 0; j < SIZE; j++)
            {
                out.push_back(board[i][j]);
                out.push_back(' ');
            }
            out.push_back('\n');
        }
        
        return out; 
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

        // println(choiceX << ", " << choiceY);
        // println("");

    }
}