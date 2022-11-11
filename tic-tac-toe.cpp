// Run here by copying and pasting code in to main file:
// https://www.programiz.com/cpp-programming/online-compiler/

// g++ -Wall -Wextra -pedantic -O3 -g -std=c++17 tic-tac-toe.cpp -o tic-tac-toe.exe

#include <iostream>
#include <string>
#include <map>

#define print(x) std::cout << x
#define println(x) std::cout << x << '\n'

using String = std::string;

class Board
{
private:
public:
    static const size_t SIZE = 3;
    static const size_t TOTAL_SIZE = SIZE * SIZE;

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
        for (size_t i = 0; i < SIZE; i++)
        {
            for (size_t j = 0; j < SIZE; j++)
            {
                board[i][j] = FILLER;
            }
        }
    }

    // bool isWinner(char potentialWinner) const
    // {

    // }

    void placePlayer(size_t x, size_t y, char player)
    {
        turnCount++;
        place(y, x, player);
    }

    inline bool isBoardFull() const
    {
        return turnCount >= TOTAL_SIZE;
    }

    inline char get(size_t i, size_t j) const
    {
        return board[i][j];
    }

    inline void place(size_t i, size_t j, char val)
    {
        board[i][j] = val;
    }

    const String toString() const
    {
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

std::ostream &operator<<(std::ostream &streem, const Board &board)
{
    streem << board.toString();
    return streem;
}

const std::map<String, size_t> verticalInputMapper = {
    { "top", 0 },
    { "center", 1 },
    { "middle", 1 },
    { "buttom", 2 }
};

const std::map<String, size_t> horizontalInputMapper = {
    { "left", 0 },
    { "center", 1 },
    { "middle", 1 },
    { "right", 2 }
};

void getPosInput(const String &s, size_t &choiceX, size_t &choiceY)
{
    const int mid = s.find_first_of(" ");

    const String verticlePos = s.substr(0, mid);
    const String horizontalPos = s.substr(mid + 1, s.length());

    if (verticalInputMapper.count(verticlePos))
    {
        choiceY = verticalInputMapper.find(verticlePos)->second;
    }
    else
    {
        throw std::invalid_argument("Verticle postion (first value) must be \"top\", \"center\", or \"buttom\".");
    }

    if (horizontalInputMapper.count(horizontalPos))
    {
        choiceX = horizontalInputMapper.find(horizontalPos)->second;
    }
    else
    {
        throw std::invalid_argument("Horizontal postion (second value) must be \"left\", \"center\", or \"right\".");
    }
}

void getValidInput(size_t &choiceX, size_t &choiceY)
{
    bool hasGotValidInput = false;

    String choice;
    while (!hasGotValidInput)
    {
        print("Where do you want to go: ");
        std::getline(std::cin, choice);

        if (choice == "QUIT")
        {
            println("Good Bye");
            exit(0);
        }

        try
        {
            getPosInput(choice, choiceX, choiceY);
            hasGotValidInput = true;
        }
        catch (const std::invalid_argument &ex)
        {
            println(ex.what());
        }
    }
}

int main()
{
    bool isPlaying = true;
    size_t choiceX;
    size_t choiceY;

    Board board;

    println("This project is incomplete.\n");

    while (isPlaying)
    {
        

        println(board);

        getValidInput(choiceX, choiceY); // store valid location from user in choice X,Y

        board.placePlayer(choiceX, choiceY, 'X'); // place current player at choice X, Y
    }

    println(board);



}