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

BLANK_CHAR = ''
class Board {
    constructor(width = DEFAULT_SIZE, height = DEFAULT_SIZE) {
        this.width = width;
        this.height = height;
        this.size = this.width * this.height;

        this.turnCount = 0;
        this.gameCount = 0;
        this.currentPlayerIndex = 0;

        this.boardArray = Array(this.height);
        this.boardBody = document.querySelector('.board-body');

        // create board on page and in array
        for (let i = 0; i < this.height; i++) {
            this.boardArray[i] = Array(this.width);
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
        cell.innerText = this.boardArray[i][j] = char;

        if (char !== BLANK_CHAR) {
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
                this.set(i, j, BLANK_CHAR);
                // this.set(i, j, "(" + i + "," + j + ")")
                let cell = this.getCell(i, j);
                cell.classList.remove('occupied');
                cell.onclick = () => this.playerTurn(i, j)
            }
        }
        this.gameCount++;
    }

    getStringSize() { return '(' + this.width + 'x' + this.height + ')'; }

    isPlayerWinner(player) {
        for (let i = 0; i < this.width; i++) {

        }
    }

    #isWinningArray(array) {
        for (let i = 1; i < array.length; i++) {
            const element = array[i];
            
        }
    }
}


const board = new Board(getValidSizeParam('width'), getValidSizeParam('height'));

document.querySelectorAll("td").forEach((td) => {
    if (td.getBoundingClientRect().left < 0){
        document.querySelector(".board").classList.remove("centered-container")
        document.body.style.overflowX = "scroll"
    }
})


document.querySelector('.reset-board').onclick = () => board.reset();
board.reset();

document.querySelector('title').innerText += ' ' + board.getStringSize();