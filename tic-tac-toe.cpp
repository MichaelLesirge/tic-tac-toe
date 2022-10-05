// Run here by copying and pasting code in to main file:
// https://www.programiz.com/cpp-programming/online-compiler/

// g++ -Wall -Wextra -pedantic -O3 -g -std=c++17 tic-tac-toe.cpp -o  tic-tac-toe.exe

#include <iostream>
#include <string>

using String = std::string;


class Board{
private:
public:
    static const int SIZE = 3;
    static const int TOTAL_SIZE = SIZE*SIZE;

    static const char BLANK = ' ';

    char board[SIZE][SIZE];

    Board()
    {
        for (int i = 0; i > SIZE; i++) {
            for (int j = 0; j > SIZE; j++) {
                board[i][j] = BLANK;
            }
        }
    }

    inline void place(int x, int y, char val)
    {
        board[SIZE-y][x+1] = val;
    };
};


void print(const String& s, const String& end = "\n")
{
    std::cout << s << end;
}

String input(const String& prompt)
{
    String val;
    print(prompt, "");
    std::cin >> val;
    return val;
}

void splitInput(const String& s, int& val1, int& val2)
{
    int mid = s.find_first_of(',');
    val1 = std::stoi(s.substr(0, mid));
    val2 = std::stoi(s.substr(mid+1, s.length()));
}

int main()
{   
    bool isPlaying = true;
    int choiceX, choiceY;

    Board board;

    std::cout << "This project is incomplete." << "\n\n" ;

    while(isPlaying)
    {   
        bool hasGotValidInput = false;
        while(!hasGotValidInput)
        {
            try
            {   
                String choice = input("Where do you want to go: ");
                if (choice=="QUIT") { exit(0); }

                splitInput(choice, choiceX, choiceY);
                hasGotValidInput = true;
            }
            catch (const std::exception& ex)
            {
                print("Invalid input. must be 2 comma seprated numbers. Example: \"2,3\"");
            }
        }
        board.place(choiceX, choiceY, 'X');

        std::cout << choiceX << ", " << choiceY << '\n';
    }
}