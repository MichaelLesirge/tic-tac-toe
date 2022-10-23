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

	addCords(offset = 1) {
		const cords = document.createElement("span")
		cords.classList.add("cords")
		cords.innerText = "(" + (this.x + offset) + "," + (this.y + offset) + ")"
		this.el.appendChild(cords)
	}
}

class Board {
	constructor(width = DEFAULT_SIZE, height = DEFAULT_SIZE, winRowLength = undefined) {
		this.width = width
		this.height = height
		this.winRowLength = winRowLength

		this.size = this.width * this.height
		this.isPerfectSquare = this.width === this.height

		this.turnCount = 0
		this.gameCount = 0
		this.currentPlayerIndex = 0
		this.isPlaying = true

		this.isDisplayingCords = false

		this.minWinRowLength = this.winRowLength || Math.min(this.width, this.height)
		this.winCheckAfter = (this.minWinRowLength - 1) * players.length

		this.checkDiagnals = this.winRowLength !== undefined || this.isPerfectSquare

		this.checkFuntion = this.winRowLength === undefined ? this._isPlayerWinnerAccros : this._isPlayerWinnerCount

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

			this.currentPlayerIndex = (this.turnCount + this.gameCount) % players.length
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

	_isPlayerWinnerAccros(player, inner, outer, getCell) {
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
			if (isWin) return [isWin, cellArray]
		}
		return [false, null]
	}

	_isPlayerWinnerCount(player, inner, outer, getCell) {
		const cellArray = new Array(this.winRowLength)
		for (let i = 0; i < outer; i++) {
			let count = 0
			for (let j = 0; j < inner; j++) {
				const cell = getCell(j, i)
				cellArray[j] = cell
				if (cell.val === player) {
					count++
					if (count >= this.winRowLength) return [true, cellArray]
				}
				else count = 0
			}
		}
		return [false, null]
	}

	isPlayerWinner(player) {
		if (this.turnCount > this.winCheckAfter) {

			let isWin, cellArray

			// check horizontal
			[isWin, cellArray] = this.checkFuntion(player, this.width, this.height, (x, y) => this.getCell(x, y))
			if (isWin) { return [isWin, cellArray] }

			// check vertical
			[isWin, cellArray] = this.checkFuntion(player, this.height, this.width, (y, x) => this.getCell(x, y))
			console.log(isWin, cellArray)
			if (isWin) { return [isWin, cellArray] }

			// check diagonals if board is square
			if (this.checkDiagnals) {
				// top left to buttom right
				[isWin, cellArray] = this.checkFuntion(player, this.width, 1, (i, _) => this.getCell(i, i))
				if (isWin) { return [isWin, cellArray] }


				// top right to buttom left
				[isWin, cellArray] = this.checkFuntion(player, this.width, 1, (i, _) => this.getCell(i, this.width - i - 1))
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
const oldParems = params.toString()

function getNumberParam(name) {
	return parseInt(params.get(name))
}

function validNumber(num, min, max, fallback = undefined) {
	return isNaN(num) ? fallback : Math.max(min, Math.min(max, num))
}

function getUpdateValidNumberParam(name, min, max, fallback = undefined, toLargeMessage = () => "") {
	const num = getNumberParam(name)

	if (num > max && confirm(`${toLargeMessage(name, num, max)}. Do you want to use suggested max size of ${max}?`)) max = Infinity

	const newNum = validNumber(num, min, max, fallback)

	params.set(name, newNum)

	return newNum
}

function getUpdateValidNumberParamIfExists(name, min, max, toLargeMessage) {
	if (params.has(name)) {
		if (!isNaN(getNumberParam(name))) {
			return getUpdateValidNumberParam(name, min, max, undefined, toLargeMessage)
		}
		params.delete(name)
	}
	return undefined
}

const getUpdateValidSizeParam = (name) => getUpdateValidNumberParam(name, MIN_SIZE, MAX_SIZE, DEFAULT_SIZE, (name, num, max) => `Board ${name} of ${num} is to larger than recomend max of ${max}`)

const width = getUpdateValidSizeParam("width")
const height = getUpdateValidSizeParam("height")

const boardSizes = `${width}x${height}`

const winRowLength = getUpdateValidNumberParamIfExists("win-condition", MIN_SIZE, Math.max(width, height), (name, num, max) => `Impossible to get ${num} in a row with current board sizes of ${boardSizes}`)

const newParms = params.toString()
if (oldParems !== newParms) {
	location.search = newParms
}

const board = new Board(width, height, winRowLength)

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

document.querySelector("title").innerText += ` (${boardSizes})`
