import {MIN_SIZE, MAX_SIZE, DEFAULT_SIZE} from "./consts.js";

const root = document.documentElement;

const infoSpan = document.querySelector("#info");
const displayInfo = msg => infoSpan.innerText = msg;

const toggleCordsButton = document.querySelector("#toggle-cords");
const resetBoardButton = document.querySelector("#reset-button");

// TODO allow users to specify num of players and there letters in home page (index.html)
const players = ["x", "o"].map(element => element.toUpperCase());

const params = new URLSearchParams(location.search);
function getValidSizeParam(name) {
    if (params.has(name)) {
        const size = parseInt(params.get(name));
        if (!isNaN(size)) {
            // no check for to big becuase if someone wants to try it I wont stop them
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

        this.isDisplayingCords = false;
        root.style.setProperty("--cords-visibility", this.isDisplayingCords ? "defalt" : "hidden")

        this.minTurnsToWin = Math.min(this.width, this.height);

        this.boardArray = Array(this.height);
        this.boardBody = document.querySelector(".board-body");

        // create board on page and in array
        for (let y = 0; y < this.height; y++) {
            this.boardArray[y] = Array(this.width);
            let tableRow = this.boardBody.insertRow();
            for (let x = 0; x < this.width; x++) {
                let cell = document.createElement("td");
                tableRow.insertCell(cell);
            }
        }
    }

    playerTurn(x, y) {
        if (this.isPlaying) {
            let cell = this.getCell(x, y);
            resetBoardButton.disabled = false;
            cell.onclick = () => {}

            const currentPlayer = players[this.currentPlayerIndex];
            this.set(x, y, currentPlayer);
            
            this.currentPlayerIndex = (this.turnCount + this.gameCount) % players.length;
            this.turnCount++;

            let [isWinner, winningArray] = this.isPlayerWinner(currentPlayer);

            if (isWinner) {
                this.highlightArray(winningArray);
                this.gameOver(currentPlayer + " Wins");
            }
            else if (this.turnCount >= this.size) {
                this.gameOver("Tie");
            }
            else {
                displayInfo(players[this.currentPlayerIndex] + "s turn.");
            }
        }
    }

    newGame() {
        this.isPlaying = true;
        this.currentPlayerIndex = this.gameCount % players.length;
        infoSpan.innerText = "Starting game with " + players[this.currentPlayerIndex] + "s.";
        this.turnCount = 0;

        this.reset();
        document.querySelector("#reset-button").disabled = true;

        this.gameCount++;
    }

    gameOver(msg) {
        this.isPlaying = false;
        displayInfo(msg + "!")
        this.forEach((x, y) => this.getCell(x, y).classList.add("occupied"));
    }

    reset() {
        this.forEach((x, y) => {
            this.set(x, y, BLANK_CHAR, false);
            let cell = this.getCell(x, y);

            const cords = document.createElement("span");
            cords.classList.add("cords");
            cords.innerText = "(" + (x+1) + "," + (this.height-y) + ")";
            // cords.innerText = "(" + (y) + "," + (x) + ")";
            cell.appendChild(cords);

            cell.classList.remove("occupied", "highlighted");
            cell.onclick = () => this.playerTurn(x, y);
        })
    }

    isPlayerWinner(player) {
        if ((this.turnCount / players.length)+1 < this.minTurnsToWin) return [false, null];

        let isWin = false;
        let winningArrayHeight = new Array(this.height);
        let winningArrayWidth = new Array(this.width)

        // check horizontal
        for (let y = 0; y < this.height; y++) {
            isWin = true;
            for (let x = 0; x < this.width; x++) {
                if (this.getElement(x, y) !== player) {
                    isWin = false;
                    break;
                }
            }
            if (isWin) {
                for (let x = 0; x < this.width; x++) {
                    winningArrayWidth[x] = this.getCell(x, y)
                }
                return [true, winningArrayWidth];
            }
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
            if (isWin) {
                for (let y = 0; y < this.height; y++) {
                    winningArrayHeight[y] = this.getCell(x, y)
                }
                return [true, winningArrayHeight];
            }
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
            if (isWin) {
                for (let i = 0; i < this.width; i++) {
                    winningArrayWidth[i] = this.getCell(i, i)
                }
                return [true, winningArrayWidth];
            }

            isWin = true;
            for (let i = 0; i < this.width; i++) {
                if (this.getElement(this.width-i-1, i) !== player) {
                    isWin = false;
                    break;
                }
            }
            if (isWin) {
                for (let i = 0; i < this.width; i++) {
                    winningArrayWidth[i] = this.getCell(this.width-i-1, i)
                }
                return [true, winningArrayWidth];
            }

            }
        return [false, null];
    }

    isOverflowing() {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                if (this.getCell(x, y).getBoundingClientRect().left < 0) return true;
            }
        }
        return false;
    }

    highlightArray = (array) => array.forEach(el =>  el.classList.add("highlighted"));

    toggleCords() {
        this.isDisplayingCords = !this.isDisplayingCords;
        root.style.setProperty("--cords-visibility", this.isDisplayingCords ? "defalt" : "hidden")
    }

    getStringSize = () => '(' + this.width + 'x' + this.height + ')';

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

toggleCordsButton.onclick = () => board.toggleCords();

const newGame = () => board.newGame(true);

resetBoardButton.onclick = newGame;
newGame();

document.querySelector('title').innerText += ' ' + board.getStringSize();