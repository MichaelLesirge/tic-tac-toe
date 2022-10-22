import { MIN_SIZE, MAX_SIZE, DEFAULT_SIZE } from "./consts.js"

const toggleCordsButton = document.querySelector("#toggle-cords")
const resetBoardButton = document.querySelector("#reset-button")

const infoSpan = document.querySelector("#info")
const displayInfo = (msg) => (infoSpan.innerText = msg)

// TODO allow users to specify num of players and there letters in home page (index.html)
const players = ["x", "o"].map((element) => element.charAt(0).toUpperCase())

class Cell {
	constructor(x, y, el) {
		this.x = x
		this.y = y

		this.el = el

		this.reset()
	}

	set(text) {
		this.val = this.el.innerText = text
	}

	disable() {
		this.el.onclick = () => { }
		this.el.classList.add("disabled")
	}

	highlight() {
		this.el.classList.add("highlighted")
	}

	reset() {
		this.set("")
		this.el.classList.remove("disabled", "highlighted")
	}

	setOnClick(onclickFunc) {
		this.el.onclick = onclickFunc
	}

	addCords() {
		const cords = document.createElement("span")
		cords.classList.add("cords")
		cords.innerText = "(" + (this.x + 1) + "," + (this.y + 1) + ")"
		this.el.appendChild(cords)
	}
}

class Board {
	constructor(width = DEFAULT_SIZE, height = DEFAULT_SIZE) {
		this.width = width
		this.height = height
		this.size = this.width * this.height
		this.isPerfectSquare = this.width === this.height

		this.turnCount = 0
		this.gameCount = 0
		this.currentPlayerIndex = 0
		this.isPlaying = true

		this.isDisplayingCords = false

		this.winRowLength = Math.min(this.width, this.height)
		this.winCheckAfter = (this.winRowLength - 1) * players.length

		this.boardArray = Array(this.height)
		this.boardBody = document.querySelector(".board-body")

		// create board on page and in array
		for (let y = 0; y < this.height; y++) {
			this.boardArray[y] = Array(this.width)
			let tableRow = this.boardBody.insertRow()
			for (let x = 0; x < this.width; x++) {
				let el = tableRow.insertCell()

				let cell = new Cell(x, y, el)
				this.boardArray[y][x] = cell
			}
		}

		this.updateCordsVisablity()
	}

	playerTurn(cell) {
		if (this.isPlaying) {
			resetBoardButton.classList.remove("fade-button")

			const currentPlayer = players[this.currentPlayerIndex]

			cell.set(currentPlayer)
			cell.disable()

			this.currentPlayerIndex =
				(this.turnCount + this.gameCount) % players.length
			this.turnCount++

			let [isWinner, winningArray] = this.isPlayerWinner(currentPlayer)

			if (isWinner) {
				this.highlightArray(winningArray)
				this.gameOver()
				displayInfo(currentPlayer + " Wins!")
			} else if (this.turnCount >= this.size) {
				this.gameOver()
				displayInfo("Tie!")
			} else {
				displayInfo(players[this.currentPlayerIndex] + "s turn.")
			}
		}
	}

	newGame() {
		this.isPlaying = true
		this.currentPlayerIndex = this.gameCount % players.length
		displayInfo("Starting with " + players[this.currentPlayerIndex] + "s.")
		this.turnCount = 0

		this.reset()
		resetBoardButton.classList.add("fade-button")

		this.gameCount++
	}

	gameOver() {
		this.isPlaying = false
		this.forEach((cell) => cell.disable())
	}

	reset() {
		this.forEach((cell) => {
			cell.reset()
			cell.addCords()
			cell.setOnClick(() => {
				this.playerTurn(cell)
			})
		})
	}

	_isPlayerWinnerRow(player, inner, outer, getCell) {
		const cellArray = new Array(inner)
		for (let i = 0; i < outer; i++) {
			let isWin = true
			for (let j = 0; j < inner; j++) {
				const cell = getCell(j, i)
				cellArray[j] = cell
				if (cell.val !== player) {
					isWin = false
					break
				}
			}
			return [isWin, cellArray]
		}
		return [false, cellArray]
	}


	isPlayerWinner(player) {
		if (this.turnCount > this.winCheckAfter) {

			let isWin, cellArray;

			// check horizontal
			[isWin, cellArray] = this._isPlayerWinnerRow(player, this.width, this.height, (x, y) => this.getCell(x, y))
			if (isWin) { return [isWin, cellArray] }
			
			// // check vertical
			// [isWin, cellArray] = this._isPlayerWinnerRow(player, this.height, this.width, (y, x) => this.getCell(x, y))
			// if (isWin) { return [isWin, cellArray] }

			// check diagonals if board is square
			if (this.isPerfectSquare && false) {
				// top left to buttom right
				[isWin, cellArray] = this._isPlayerWinnerRow(player, this.width, 1, (i, _) => this.getCell(i, i))
				if (isWin) { return [isWin, cellArray] }


				// top right to buttom left
				[isWin, cellArray] = this._isPlayerWinnerRow(player, this.width, 1, (i, _) => this.getCell(i, this.width - i - 1))
				console.log(cellArray)
				if (isWin) { return [isWin, cellArray] }
			}
		}
		return [false, null]
	}

	highlightArray(array) {
		array.forEach((cell) => cell.highlight())
	}

	isOverflowing() {
		for (let y = 0; y < this.height; y++) {
			for (let x = 0; x < this.width; x++) {
				if (this.getCell(x, y).el.getBoundingClientRect().left < 0)
					return true
			}
		}
		return false
	}

	toggleCords() {
		this.isDisplayingCords = !this.isDisplayingCords
		this.updateCordsVisablity(this.isDisplayingCords)
	}

	updateCordsVisablity() {
		toggleCordsButton.innerText =
			(this.isDisplayingCords ? "Hide" : "Display") + " Cords"
		this.boardBody.style.setProperty(
			"--cords-visibility",
			this.isDisplayingCords ? "defalt" : "hidden"
		)
	}

	forEach(callback) {
		for (let y = 0; y < this.height; y++) {
			for (let x = 0; x < this.width; x++) {
				callback(this.getCell(x, y))
			}
		}
	}

	getCell(x, y) {
		return this.boardArray[y][x]
	}
}

const params = new URLSearchParams(location.search)

function getNumberParam(name) {
	return parseInt(params.get(name))
}

function validNumber(num, min, max, fallback) {
	return isNaN(num) ? fallback : Math.max(min, Math.min(max, num))
}

function getUpdateValidNumberParam(name, min, max, fallback) {
	const num = getNumberParam(name)

	if (
		num > max &&
		confirm(
			`Board ${name} of ${num} is to larger than recomend max of ${max}. Are you sure you want this size?`
		)
	) {
		max = Infinity
	}

	const newNum = validNumber(num, min, max, fallback)
	const needUpdate = num !== newNum

	if (needUpdate) params.set(name, newNum)

	return [newNum, needUpdate]
}

const getUpdateValidSizeParam = (name) =>
	getUpdateValidNumberParam(name, MIN_SIZE, MAX_SIZE, DEFAULT_SIZE)

const [width, wNeedsUpdate] = getUpdateValidSizeParam("width")
const [height, hNeedsUpdate] = getUpdateValidSizeParam("height")

if (wNeedsUpdate || hNeedsUpdate) {
	location.search = params.toString()
}

const board = new Board(width, height)

board.newGame()
resetBoardButton.onclick = () => board.newGame()

toggleCordsButton.onclick = () => board.toggleCords()

const boardClassList = document.querySelector(".board-container").classList
const bodyStyle = document.body.style
function fixOverflow() {
	if (board.isOverflowing()) {
		boardClassList.remove("centered-container")
		bodyStyle.overflowX = "scroll"
	} else {
		boardClassList.add("centered-container")
		bodyStyle.overflowX = "default"
	}
}

fixOverflow()
window.onresize = fixOverflow

document.querySelector("title").innerText += ` (${width}x${height})`
