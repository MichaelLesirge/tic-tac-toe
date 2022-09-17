// I have very little javascript experience currently.

const MIN_SIZE = 1;
const DEFAULT_SIZE = 3;

const currentPlayerSpan = document.querySelector(".current-player");
const gameOverSpan = document.querySelector(".game-over");

// TODO allow users to specify num of players and there letters in home page (index.html)
const players = ["x", "o"].map(element => element.toUpperCase());

const params = new URLSearchParams(location.search);
function getValidSizeParam(name) {
    if (params.has(name)) {
        const size = parseInt(params.get(name));
        if (!isNaN(size)) {
            return Math.max(size, MIN_SIZE);
        }
    }
    return DEFAULT_SIZE;
}

const BLANK_CHAR = '';
class Board {
    constructor(width = DEFAULT_SIZE, height = DEFAULT_SIZE) {
        this.width = width;
        this.height = height;
        this.size = this.width * this.height;

        this.turnCount = 0;
        this.gameCount = 0;
        this.currentPlayerIndex = 0;
        this.gameOver = false;

        this.boardArray = Array(this.height);
        this.boardBody = document.querySelector('.board-body');

        // create board on page and in array
        for (let y = 0; y < this.height; y++) {
            this.boardArray[y] = Array(this.width);
            let tableRow = this.boardBody.insertRow();
            for (let x = 0; x < this.width; x++) {
                let cell = document.createElement('td');
                tableRow.insertCell(cell);
            }
        }
    }
    

    getCell(x, y) { return this.boardBody.children[y].children[x]; }
    
    set(x, y, char, setOccupied=true) {
        let cell = this.getCell(x, y);
        cell.innerText = this.boardArray[y][x] = char;
        if (setOccupied) {
            cell.classList.add('occupied');
        }
    }


    playerTurn(x, y) {
        let cell = this.getCell(x, y);
        if (!this.gameOver && !cell.classList.contains('occupied')) {
            const currentPlayer = players[this.currentPlayerIndex];
            this.set(x, y, currentPlayer);
            
            this.currentPlayerIndex = (this.turnCount + this.gameCount) % players.length;
            this.turnCount++;

            if (this.turnCount >= this.size) {
                this.gameOver = true;
                displayTie()
            }
            else if (this.isPlayerWinner(currentPlayer)) {
                this.gameOver = true;
                displayWinner(currentPlayer);
            }
            else {
                currentPlayerSpan.innerText = players[this.currentPlayerIndex] + "s turn.";
            }
            // cell.onclick = () => {}
        }
    }

    reset(showCords=false) {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                this.set(x, y, BLANK_CHAR, false);
                let cell = this.getCell(x, y);
                if (showCords) {
                    const cords = document.createElement("span");
                    cords.classList.add("cords");
                    // cords.innerText = "(" + (x+1) + "," + (this.height-y) + ")";
                    cords.innerText = "(" + (y) + "," + (x) + ")";
                    cell.appendChild(cords);
                }
                cell.classList.remove('occupied');
                cell.onclick = () => this.playerTurn(x, y);
            }
        }
    }

    newGame(showCords=false) {
        this.currentPlayerIndex = this.gameCount % players.length;
        currentPlayerSpan.innerText = "Starting game with " + players[this.currentPlayerIndex] + "s.";
        this.turnCount = 0;
        this.gameOver = false;

        this.reset(showCords);

        this.gameCount++;
    }

    getStringSize() { return '(' + this.width + 'x' + this.height + ')'; }

    #isWinningArray(array, player) { return array.every( val => val === player ) }

    isPlayerWinner(player) {
        // check horizontal
        for (let y = 0; y < this.height; y++) {
            const row = this.boardArray[y];
            if (this.#isWinningArray(row, player)) {
                return true;
            }
        }

        // check vertical
        for (let x = 0; x < this.width; x++) {
            const collum = new Array(this.height);
            for (let y = 0; y < this.height; y++) {
                collum.push(this.boardArray[y][x]);
            }
            if (this.#isWinningArray(collum, player)) {
                return true;
            }
        }

        // check diagnals if board is a square
        if (this.width === this.height) {
            
            const horizontalLeftToRight = new Array(this.width);

            // check top left to buttom right
            for (let i = 0; i < this.width; i++) {
                horizontalLeftToRight.push(this.boardArray[i][i]);
            }
            if (this.#isWinningArray(horizontalLeftToRight, player)) {
                return true;
            }

            const horizontalRightToLeft = new Array(this.width);

            // check top right to button left
            for (let i = 0; i < this.width; i++) {
                horizontalRightToLeft.push(this.boardArray[i][this.width-i-1]);
            }
            if (this.#isWinningArray(horizontalRightToLeft, player)) {
                return true;
            }    
        }
    }

    isOverflowing() {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                if (this.getCell(x, y).getBoundingClientRect().left < 0) { return true; }
            }
        }
    }
}

const board = new Board(getValidSizeParam('width'), getValidSizeParam('height'));

function displayWinner(player) {
    currentPlayerSpan.innerText = player + " Wins!";
    startNewGame();
}

function displayTie() {
    currentPlayerSpan.innerText = "Tie";
    startNewGame();
}

function startNewGame() {

}

const boardClassList = document.querySelector(".board-container").classList
const bodyStyle = document.body.style
function fixOverflow() {
    if (board.isOverflowing()) {
        boardClassList.remove("centered-container");
        bodyStyle.overflowX = "scroll";
    }
    else {
        boardClassList.add("centered-container");
        bodyStyle.overflowX = "default";
    }
}

fixOverflow();
window.onresize = fixOverflow;

let showCords = true;
const newGame = () => board.newGame(showCords);

document.querySelector('.reset-board').onclick = newGame;
newGame();

document.querySelector('title').innerText += ' ' + board.getStringSize();