// I have very little javascript experience currently.

const MIN_SIZE = 1;
const DEFAULT_SIZE = 3;

const currentPlayerSpan = document.querySelector(".current-player");
const gameOverSpan = document.querySelector(".game-over");

// TODO allow users to specify num of players and there letters in home page (index.html)
const players = ["x", "o"].map(element => { return element.toUpperCase(); });

const params = new URLSearchParams(location.search);
function getValidSizeParam(name) {
    if (params.has(name)) {
        const size = parseInt(params.get(name));
        if (!isNaN(size)) {
            return Math.max(size, MIN_SIZE)
        }
    }
    return DEFAULT_SIZE
}

DEFUALT_CHAR = ''
class Board {
    constructor(width = DEFAULT_SIZE, height = DEFAULT_SIZE) {
        this.width = width;
        this.height = height;
        this.size = this.width * this.height;

        this.turnCount = 0;
        this.gameCount = 0;
        this.currentPlayerIndex = 0;

        this.boardMap = Array(this.height);
        this.boardBody = document.querySelector('.board-body');

        // create board on page and in array
        for (let i = 0; i < this.height; i++) {
            this.boardMap[i] = Array(this.width);
            let tableRow = this.boardBody.insertRow();
            for (let j = 0; j < this.width; j++) {
                let cell = document.createElement('td');
                tableRow.insertCell(cell);
            }
        }
    }

    getCell(i, j) { return this.boardBody.children[i].children[j]; }

    set(i, j, char) {
        let cell = this.getCell(i, j);
        cell.innerText = this.boardMap[i][j] = char;

        if (char !== DEFUALT_CHAR) {
            cell.classList.add('occupied');
        }
    }

    playerTurn(i, j) {
        console.log(this.turnCount, this.currentPlayerIndex);
        if (!this.getCell(i, j).classList.contains('occupied')) {
            this.set(i, j, players[this.currentPlayerIndex]);

            this.currentPlayerIndex = (this.turnCount + this.gameCount) % players.length;
            currentPlayerSpan.innerText = players[this.currentPlayerIndex] + "s turn.";

            this.turnCount++;
        }
    }

    reset() {
        this.currentPlayerIndex = this.gameCount % players.length
        currentPlayerSpan.innerText = "Starting game with " + players[this.currentPlayerIndex] + "s.";
        this.turnCount = 0;

        for (let i = 0; i < this.height; i++) {
            for (let j = 0; j < this.width; j++) {
                this.set(i, j, DEFUALT_CHAR);
                let cell = this.getCell(i, j);
                cell.classList.remove('occupied');
                cell.onclick = () => this.playerTurn(i, j)
            }
        }
        this.gameCount++;
    }

    getStringSize() { return '(' + this.width + 'x' + this.height + ')'; }
}


const board = new Board(getValidSizeParam('width'), getValidSizeParam('height'));

document.querySelector('.reset-board').onclick = () => board.reset();
board.reset();

document.querySelector('title').innerText += ' ' + board.getStringSize();