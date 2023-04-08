// Run here by copying and pasting code in to main file:
// https://www.programiz.com/cpp-programming/online-compiler/

// g++ -Wall -Wextra -pedantic -O3 -g -std=c++17 tic_tac_toe.cpp -o tic_tac_toe.exe

#include <iostream>
#include <string>
#include <map>

using String = std::string;

bool is_number(const String& s)
{
    std::string::const_iterator it = s.begin();
    while (it != s.end() && std::isdigit(*it)) ++it;
    return !s.empty() && it == s.end();
}

const int OFFSET_FOR_HUMANS = 1;

class Board
{
public:
    static const size_t SIDE_SIZE = 3;
    static const size_t TOTAL_SIZE = SIDE_SIZE * SIDE_SIZE;

private:
    char board[SIDE_SIZE][SIDE_SIZE];

    static const char FILLER = '-';

    size_t placed;

    void set(size_t row, size_t col, char val)
    {
        board[row][col] = val;
    }

    bool checkDirection(size_t row_start, size_t col_start, int row_change, int col_change, char player) const
    {
        size_t row = row_start, col = col_start;
        while (row < SIDE_SIZE && col < SIDE_SIZE)
        
        {
            if (get(row, col) != player)
            {
                return false;
            }
            row += row_change;
            col += col_change;
        }
        return true;
    }

public:
    Board()
    {
        reset();
    }

    void reset()
    {
        placed = 0;
        for (size_t row = 0; row < SIDE_SIZE; row++)
        {
            for (size_t col = 0; col < SIDE_SIZE; col++)
            {
                set(row, col, FILLER);
            }
        }
    }

    char get(size_t row, size_t col) const
    {
        return board[row][col];
    }

    bool isFull() const
    {
        return placed >= TOTAL_SIZE;
    }


    bool isPlayerWinner(char player) const
    {
        if (checkDirection(0, 0, 1, 1, player) || checkDirection(SIDE_SIZE - 1, 0, 1, -1, player))
        {
            return true;
        }
        for (size_t i = 0; i < SIDE_SIZE; i++)
        {
            if (checkDirection(i, 0, 1, 0, player) || checkDirection(0, i, 0, 1, player))
            {
                return true;
            }
        }
        return false;
    }

    bool isValidPosition(int row, int col) const
    {
        return (row > -1) && (row < (int) SIDE_SIZE) && (col > -1) && (col < (int) SIDE_SIZE);
    }

    void placeCell(int row, int col, char val)
    {
        if (!isValidPosition(row, col))
        {
            throw std::invalid_argument("Location is not in board");
        }
        if (get(row, col) != FILLER)
        {
            throw std::invalid_argument("Location is already occuiped");
        }
        set(row, col, val);
        placed++;
    }

    const String toString() const
    {
        String out = "";
        for (size_t row = 0; row < SIDE_SIZE; row++)
        {
            for (size_t col = 0; col < SIDE_SIZE; col++)
            {
                out.push_back(get(row, col));
                out.push_back(' ');
            }
            out.push_back('\n');
        }

        return out.erase(out.length() - 1);
    }
};

const std::map<String, size_t> rowInputMapper = {
    {"top", 0},
    {"center", Board::SIDE_SIZE / 2},
    {"bottom", Board::SIDE_SIZE - 1},
};

const std::map<String, size_t> colInputMapper = {
    {"left", 0},
    {"center", Board::SIDE_SIZE / 2},
    {"right", Board::SIDE_SIZE - 1},
};

int getPositionInput(const String &userChoice, const std::map<String, size_t> &valueMap)
{
    if (valueMap.count(userChoice))
    {
        return valueMap.find(userChoice)->second;
    }
    else if (is_number(userChoice) )
    {
        return std::stoi(userChoice) - OFFSET_FOR_HUMANS;
    }
    else
    {
        throw std::invalid_argument("\"" + userChoice + "\" is not a valid location."); 
    }
}

int main()
{
    Board board;

    const size_t playerCount = 2;
    const char players[playerCount] = {'X', 'O'};

    bool playAgain = true;

    while (playAgain)
    {
        board.reset();

        size_t turnCount = 0;

        bool playing = true;
        while (playing)
        {
            char currentPlayer = players[turnCount % playerCount];

            std::cout << '\n' << currentPlayer << " turn." << '\n';
            std::cout << '\n' << board.toString() << '\n' << '\n';

            bool hasGotValidInput = false;

            while (!hasGotValidInput)
            {
                String userChoice;
                std::cout << "Where do you want to go: ";
                std::getline(std::cin, userChoice);

                if (userChoice == "QUIT")
                {
                    std::cout << "Good Bye!" << '\n';
                    exit(0);
                }

                const int mid = userChoice.find_first_of(" ");

                const String userRowChoice = userChoice.substr(0, mid);
                const String userColChoice = userChoice.substr(mid + 1, userChoice.length());


                try
                {
                    const int rowChoice = getPositionInput(userRowChoice, rowInputMapper);
                    const int colChoice = getPositionInput(userColChoice, colInputMapper);
                    
                    board.placeCell(rowChoice, colChoice, currentPlayer);
                }
                catch (std::invalid_argument &e)
                {
                    std::cout << e.what() << '\n';
                    continue;
                }

                hasGotValidInput = true;
            }

            if (board.isFull())
            {
                std::cout << '\n' << board.toString() << '\n' << '\n';
                std::cout << "Its a tie" << '\n' << '\n';
                playing = false;
            }
            else if (board.isPlayerWinner(currentPlayer))
            {
                std::cout << '\n' << board.toString() << '\n' << '\n';
                std::cout << "Player " << currentPlayer << " wins!" << '\n';
                playing = false;
            }

            turnCount++;
        }

        String wantsToPlayAgain;

        std::cout << "Do you want to play agien: [Y/n] ";
        std::cin >> wantsToPlayAgain;

        playAgain = wantsToPlayAgain == "y" || wantsToPlayAgain == "Y";
        std::cin.get();
    }
}