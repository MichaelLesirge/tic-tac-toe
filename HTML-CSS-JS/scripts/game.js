// I have very little javascript experience currently.

const MIN_SIZE = 1;
const MAX_SIZE = 100;
const DEFAULT_SIZE = 3;

const infoSpan = document.querySelector("#info");
function displayInfo(msg) {
    infoSpan.innerText = msg;
}

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
        this.isPlaying = true;

        this.minTurnsToWin = Math.min(this.width, this.height)

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

    playerTurn(x, y) {
        let cell = this.getCell(x, y);
        if (this.isPlaying) {
            cell.onclick = () => {}

            const currentPlayer = players[this.currentPlayerIndex];
            this.set(x, y, currentPlayer);
            
            this.currentPlayerIndex = (this.turnCount + this.gameCount) % players.length;
            this.turnCount++;

            if (this.isPlayerWinner(currentPlayer)) {
                this.gameOver(currentPlayer + " Wins");
            }
            else if (this.turnCount >= this.size) {
                this.gameOver("Tie")
            }
            else {
                displayInfo(players[this.currentPlayerIndex] + "s turn.");
            }
        }
    }

    newGame(showCords=false) {
        this.currentPlayerIndex = this.gameCount % players.length;
        infoSpan.innerText = "Starting game with " + players[this.currentPlayerIndex] + "s.";
        this.turnCount = 0;
        this.isPlaying = true;

        this.reset(showCords);

        this.gameCount++;
    }

    gameOver(msg) {
        displayInfo(msg + "!")
        this.isPlaying = false;
        this.forEach((x, y) => {
            this.getCell(x, y).classList.add('occupied')
        })
    }

    reset(showCords=false) {
        this.forEach((x, y) => {
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
        })
    }

    isPlayerWinner(player) {
        if ((this.turnCount / players.length)+1 < this.minTurnsToWin) return false;

        let isWin;

        // check horizontal
        for (let y = 0; y < this.height; y++) {
            isWin = true;
            for (let x = 0; x < this.width; x++) {
                if (this.getElement(x, y) !== player) {
                    isWin = false;
                    break;
                }
            }
            if (isWin) return true;
        }

        // check vertical
        for (let x = 0; x < this.width; x++) {
            isWin = true;
            for (let y = 0; y < this.height; y++) {
                if (this.getElement(x, y) !== player) {
                    isWin = false;
                    break;
                }
            }
            if (isWin) return true;
        }

        // check diagonals if board is square
        if (this.width == this.height) {
            isWin = true;
            for (let i = 0; i < this.width; i++) {
                if (this.getElement(i, i) !== player) {
                    isWin = false;
                    break;
                }
            }
            if (isWin) return true;

            isWin = true;
            for (let i = 0; i < this.width; i++) {
                if (this.getElement(this.width-i-1, i) !== player) {
                    isWin = false;
                    break;
                }
            }
            if (isWin) return true;
        }
    }

    isOverflowing() {
        this.forEach((x, y) => {
            if (this.getCell(x, y).getBoundingClientRect().left < 0) { return true; }
        })
        return false;
    }

    getStringSize() { return '(' + this.width + 'x' + this.height + ')'; }

    getCell = (x, y) => this.boardBody.children[y].children[x];
    getElement = (x,y) => this.boardArray[y][x];

    forEach (callback) {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                callback(x, y)
            }
        }
    }
    
    set(x, y, char, setOccupied=true) {
        let cell = this.getCell(x, y);
        cell.innerText = this.boardArray[y][x] = char;
        if (setOccupied) {
            cell.classList.add('occupied');
        }
    }
}

const board = new Board(getValidSizeParam('width'), getValidSizeParam('height'));

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

const newGame = () => board.newGame(false);

document.querySelector('#reset-button').onclick = newGame;
newGame();

document.querySelector('title').innerText += ' ' + board.getStringSize();