// Run here by copying and pasting code in to main file:
// https://www.programiz.com/cpp-programming/online-compiler/

// g++ -Wall -Wextra -pedantic -O3 -g -std=c++17 tic_tac_toe.cpp -o tic_tac_toe.exe

#include <iostream>
#include <string>
#include <map>

#define PRINT(x) std::cout << x
#define PRINTLN(x) std::cout << x << "\n"
#define ERROR(x) std::cout << x
#define ERRORLN(x) std::cerr << x << "\n"

using String = std::string;

class Board
{
public:
    static const size_t SIDE_SIZE = 3;
    static const size_t TOTAL_SIZE = SIDE_SIZE * SIDE_SIZE;
private:
    char board[SIDE_SIZE][SIDE_SIZE];

    static const char FILLER = '-';

    size_t placed;

    void set(size_t i, size_t j, char val)
    {
        board[i][j] = val;
    }

    char get(size_t i, size_t j) const
    {
        return board[i][j];
    }

    void incIfEqual(size_t i, size_t j, char val, size_t& counter) {
        if (get(i, j) == val) counter++;
    }

public:
    Board()
    {
        reset();
    }

    void reset()
    {
        placed = 0;
        for (size_t i = 0; i < SIDE_SIZE; i++)
        {
            for (size_t j = 0; j < SIDE_SIZE; j++)
            {
                set(i, j, '\0');
            }
        }
    }

    bool isFull() const
    {
        return placed >= TOTAL_SIZE;
    }

    bool isPlayerWinner(char player) {
        size_t hCount = 0;
        size_t vCount = 0;
        size_t dlrCount = 0;
        size_t drlCount = 0;
        for (size_t i = 0; i < SIDE_SIZE; i++)
        {   
            incIfEqual(i, i, player, dlrCount);
            incIfEqual(i, SIDE_SIZE-i-1, player, drlCount);
            for (size_t j = 0; j < SIDE_SIZE; j++)
            {
                incIfEqual(i, j, player, hCount);
                incIfEqual(j, i, player, vCount);
            }
        }
        // PRINTLN(hCount << ", " << vCount << ", " << dlrCount << ", " << drlCount);
        return hCount >= SIDE_SIZE || vCount >= SIDE_SIZE || dlrCount >= SIDE_SIZE || drlCount >= SIDE_SIZE;
        
    }

    void placeCell(size_t x, size_t y, char val)
    {
        if (get(y, x) != '\0')
        {
            throw std::invalid_argument("location is already occuiped");
        }
        set(y, x, val);
        placed++;
    }

    char getCell(size_t x, size_t y)
    {
        return get(y, x);
    }

    const String toString() const
    {
        String out = "";
        for (size_t i = 0; i < SIDE_SIZE; i++)
        {
            for (size_t j = 0; j < SIDE_SIZE; j++)
            {
                out.push_back(get(i, j) == '\0' ? FILLER : get(i, j));
                out.push_back(' ');
            }
            out.push_back('\n');
        }

        return out.erase(out.length()-1);
    }
};

const std::map<String, size_t> verticalInputMapper = {
    {"top", 1},
    {"center", (Board::SIDE_SIZE / 2)+1},
    {"middle", (Board::SIDE_SIZE / 2)+1},
    {"buttom", Board::SIDE_SIZE},
};

const std::map<String, size_t> horizontalInputMapper = {
    {"left", 1},
    {"center", (Board::SIDE_SIZE / 2)+1},
    {"middle", (Board::SIDE_SIZE / 2)+1},
    {"right", Board::SIDE_SIZE},
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
        try
        {
            choiceY = std::stoi(verticlePos);
        }
        catch(const std::invalid_argument& e)
        {
            throw std::invalid_argument("Verticle postion (first value) must be a number or \"top\", \"center\", or \"buttom\"");;
        }
        
    }

    if (horizontalInputMapper.count(horizontalPos))
    {
        choiceX = horizontalInputMapper.find(horizontalPos)->second;
    }
    else
    {
        try {
            choiceX = std::stoi(horizontalPos);
        }
        catch (std::invalid_argument& e) {
            throw std::invalid_argument("Horizontal postion (second value) must be a number or \"left\", \"center\", or \"right\"");
        }
    }
    choiceX--;
    choiceY--;
}

int main()
{
    Board board;

    const size_t playerCount = 2;
    const char players[playerCount] = {'X', 'O'};

    PRINTLN("This project is incomplete.");

    bool playAgain = true;

    while (playAgain)
    {
        board.reset();

        size_t turnCount = 0;

        bool playing = true;
        while (playing)
        {
            PRINTLN("\n" + board.toString() + "\n");

            bool hasGotValidInput = false;

            char currentPlayer = players[turnCount % playerCount];

            while (!hasGotValidInput)
            {   
                String choice;
                PRINT("Where do you want to go: ");
                std::getline(std::cin, choice);

                if (choice == "QUIT")
                {
                    PRINTLN("Good Bye! :(");
                    exit(0);
                }

                size_t choiceX;
                size_t choiceY;

                try {
                    getPosInput(choice, choiceX, choiceY); // store x and y pos in choiceX and choiceY

                    if (choiceX >= Board::SIDE_SIZE) {
                        throw std::invalid_argument("X position must be between 1 and " + std::to_string(Board::SIDE_SIZE));
                    }
                    if (choiceY >= Board::SIDE_SIZE) {
                        throw std::invalid_argument("Y position must be between 1 and " +std::to_string(Board::SIDE_SIZE));
                    }
                    board.placeCell(choiceX, choiceY, currentPlayer); // placeCell current player at choice X, Y
                }
                catch (std::invalid_argument& e) {
                    ERRORLN(e.what());
                }

                hasGotValidInput = true;
            }

            if (board.isFull()) {
                PRINTLN("Its a tie");
                playing = false;
            }
            else if (board.isPlayerWinner(currentPlayer)) {
                PRINTLN("Player " << currentPlayer << " wins!");
                playing = false;
            }

            turnCount++;
        }

        PRINTLN("\n" + board.toString() + "\n");

        String wantsToPlayAgain;

        std::cout << "Do you want to play agien: [Y/n] ";
        std::cin >> wantsToPlayAgain;

        playAgain = wantsToPlayAgain == "y" || wantsToPlayAgain == "Y";
        std::cin.get();
    }
}