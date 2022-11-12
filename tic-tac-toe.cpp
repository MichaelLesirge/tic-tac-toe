// Run here by copying and pasting code in to main file:
// https://www.programiz.com/cpp-programming/online-compiler/

// g++ -Wall -Wextra -pedantic -O3 -g -std=c++17 tic-tac-toe.cpp -o tic-tac-toe.exe

#include <iostream>
#include <string>
#include <map>

#define PRINT(x) std::cout << x
#define PRINTLN(x) std::cout << x << '\n'

using String = std::string;

class Board
{
private:
    static const size_t SIZE = 3;
    static const size_t TOTAL_SIZE = SIZE * SIZE;

    char board[SIZE][SIZE];

    static const char FILLER = '-';

    size_t placed;

    void set(size_t i, size_t j, char val)
    {
        board[i][j] = val;
    }

protected:
    char get(size_t i, size_t j) const
    {
        return board[i][j];
    }

public:
    Board()
    {
        reset();
    }

    void reset()
    {
        placed = 0;
        for (size_t i = 0; i < SIZE; i++)
        {
            for (size_t j = 0; j < SIZE; j++)
            {
                set(i, j, '\0');
            }
        }
    }

    bool isBoardFull() const
    {
        return placed >= TOTAL_SIZE;
    }

    void place(size_t x, size_t y, char val)
    {
        if (get(y, x) != '\0')
        {
            throw std::invalid_argument("location is already occuiped");
        }
        set(y, x, val);
        placed++;
    }

    const String toString() const
    {
        String out = "";
        for (size_t i = 0; i < SIZE; i++)
        {
            for (size_t j = 0; j < SIZE; j++)
            {
                out.push_back(get(i, j) == '\0' ? FILLER : get(i, j));
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
    {"top", 0},
    {"center", 1},
    {"middle", 1},
    {"buttom", 2}};

const std::map<String, size_t> horizontalInputMapper = {
    {"left", 0},
    {"center", 1},
    {"middle", 1},
    {"right", 2}};

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

int main()
{
    bool isPlaying = true;
    size_t choiceX;
    size_t choiceY;

    Board board;

    PRINTLN("This project is incomplete.");

    while (isPlaying)
    {

        PRINTLN("");
        PRINTLN(board);

        bool hasGotValidInput = false;
        String choice;
        while (!hasGotValidInput)
        {
            PRINT("Where do you want to go: ");
            std::getline(std::cin, choice);

            if (choice == "QUIT")
            {
                PRINTLN("Good Bye");
                exit(0);
            }

            try
            {
                getPosInput(choice, choiceX, choiceY);
                board.place(choiceX, choiceY, 'X'); // place current player at choice X, Y

                hasGotValidInput = true;
            }
            catch (const std::invalid_argument &ex)
            {
                PRINTLN(ex.what());
            }
        }
    }

    PRINTLN(board);
}