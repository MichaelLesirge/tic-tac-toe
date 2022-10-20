import {MIN_SIZE, MAX_SIZE, DEFAULT_SIZE} from "./consts.js";

const toggleCordsButton = document.querySelector("#toggle-cords");
const resetBoardButton = document.querySelector("#reset-button");

const infoSpan = document.querySelector("#info");
const displayInfo = msg => infoSpan.innerText = msg;

// TODO allow users to specify num of players and there letters in home page (index.html)
const players = ["x", "o"].map(element => element.charAt(0).toUpperCase());

class Cell {
    constructor(x, y, el) {
        this.x = x;
        this.y = y;

        this.el = el;
        
        this.reset()
    }

    set(text) {
        this.val = this.el.innerText = text;
    }

    disable() {
        this.el.onclick = () => {};
        this.el.classList.add("disabled");
    }

    highlight() {
        this.el.classList.add("highlighted")
    }

    reset() {
        this.set("");
        this.el.classList.remove("disabled", "highlighted");
    }

    setOnClick(onclickFunc) {
        this.el.onclick = onclickFunc;
    }

    addCords() {
        const cords = document.createElement("span");
        cords.classList.add("cords");
        cords.innerText = "(" + (this.x+1) + "," + (this.y+1) + ")";
        this.el.appendChild(cords)
    }
}

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
        
        this.winRowLength = Math.min(this.width, this.height);
        this.winCheckAfter = ((this.winRowLength - 1) * players.length);
        
        this.boardArray = Array(this.height);
        this.boardBody = document.querySelector(".board-body");
        
        // create board on page and in array
        for (let y = 0; y < this.height; y++) {
            this.boardArray[y] = Array(this.width);
            let tableRow = this.boardBody.insertRow();
            for (let x = 0; x < this.width; x++) {
                let el = tableRow.insertCell();
                
                let cell = new Cell(x, y, el)
                this.boardArray[y][x] = cell;
                
            }
        }
        
        this.updateCordsVisablity();
    }

    playerTurn(cell) {
        if (this.isPlaying) {
            resetBoardButton.disabled = false;

            const currentPlayer = players[this.currentPlayerIndex];

            cell.set(currentPlayer);
            cell.disable()

            this.currentPlayerIndex = (this.turnCount + this.gameCount) % players.length;
            this.turnCount++;

            let [isWinner, winningArray] = this.isPlayerWinner(currentPlayer);

            if (isWinner) {
                this.highlightArray(winningArray);
                this.gameOver();
                displayInfo(currentPlayer + " Wins!")
            }
            else if (this.turnCount >= this.size) {
                this.gameOver();
                displayInfo("Tie!")
            }
            else {
                displayInfo(players[this.currentPlayerIndex] + "s turn.");
            }
        }
    }

    newGame() {
        this.isPlaying = true;
        this.currentPlayerIndex = this.gameCount % players.length;
        displayInfo("Starting with " + players[this.currentPlayerIndex] + "s.");
        this.turnCount = 0;

        this.reset();
        resetBoardButton.disabled = true;

        this.gameCount++;
    }

    gameOver() {
        this.isPlaying = false;
        this.forEach(cell => cell.disable());
    }

    reset() {
        this.forEach(cell => {
            cell.reset();
            cell.addCords();
            cell.setOnClick(() => { this.playerTurn(cell) });
        })
    }

    isPlayerWinner(player) {
        if (this.turnCount > this.winCheckAfter) {
            let isWin = false;
            let winningArrayHeight = new Array(this.height);
            let winningArrayWidth = new Array(this.width)

            // check horizontal
            for (let y = 0; y < this.height; y++) {
                isWin = true;
                for (let x = 0; x < this.width; x++) {
                    if (this.getCell(x, y).val !== player) {
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
                    if (this.getCell(x, y).val !== player) {
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
            if (this.width === this.height) {

                // top left to buttom right
                isWin = true;
                for (let i = 0; i < this.width; i++) {
                    if (this.getCell(i, i).val !== player) {
                        isWin = false;
                        break;
                    }
                }
                if (isWin) {
                    for (let i = 0; i < this.width; i++) {
                        winningArrayWidth[i] = this.getCell(i, i);
                    }
                    return [true, winningArrayWidth];
                }

                // top right to buttom left
                isWin = true;
                for (let i = 0; i < this.width; i++) {
                    if (this.getCell(this.width-i-1, i).val !== player) {
                        isWin = false;
                        break;
                    }
                }
                if (isWin) {
                    for (let i = 0; i < this.width; i++) {
                        winningArrayWidth[i] = this.getCell(this.width-i-1, i);
                    }
                    return [true, winningArrayWidth];
                }

            }
        }
        return [false, null];
    }

    highlightArray(array) { array.forEach((cell) => cell.highlight()) };

    isOverflowing() {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                if (this.getCell(x, y).el.getBoundingClientRect().left < 0) return true;
            }
        }
        return false;
    }

    toggleCords() {
        this.isDisplayingCords = !this.isDisplayingCords;
        this.updateCordsVisablity(this.isDisplayingCords);
    }

    updateCordsVisablity() {
        toggleCordsButton.innerText = (this.isDisplayingCords ?  "Hide" : "Display") + " Cords";
        this.boardBody.style.setProperty("--cords-visibility", this.isDisplayingCords ? "defalt" : "hidden");
    }

    forEach(callback) {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                callback(this.getCell(x, y));
            }
        }
    }
    
    getCell(x, y) { return this.boardArray[y][x]; }
}

const params = new URLSearchParams(location.search);
const new_params = new URLSearchParams()

function getNumberParam(name) {
    return parseInt(params.get(name));
}

function validNumber(num, min, max, fallback) {
    return isNaN(num) ? fallback : Math.max(min, Math.min(max, num))
}

function getUpdateValidNumberParam(name, min, max, fallback) {
    let num = getNumberParam(name)

    if (num > max && confirm(`Board ${name} of ${num} is to larger than recomend max of ${max}. Are you sure you want this size?`)) {
        max = Infinity
    }

    let newNum = validNumber(num, min, max, fallback)
    new_params.set(name, newNum)

    return [newNum, num !== newNum]
}

const getUpdateValidSizeParam = (name) => getUpdateValidNumberParam(name, MIN_SIZE, MAX_SIZE, DEFAULT_SIZE);

const [width, wNeedsUpdate] = getUpdateValidSizeParam("width");
const [height, hNeedsUpdate] = getUpdateValidSizeParam("height");


if (wNeedsUpdate || hNeedsUpdate) {
    location.search = new_params.toString()
}

console.log(width, height)
const board = new Board(width, height);

board.newGame();
resetBoardButton.onclick = () => board.newGame();

toggleCordsButton.onclick = () => board.toggleCords();

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

document.querySelector("title").innerText += ` (${width}x${height})`