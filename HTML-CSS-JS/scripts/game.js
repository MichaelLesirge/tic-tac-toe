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

const PLACEHOLDER_CELL = new Cell(null, null, document.createElement("div"))

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

		this.minWinRowLength = Math.min(this.width, this.height)
		this.winCheckAfter = (this.minWinRowLength - 1) * players.length

		this.shouldCheckHorizontal = this.shouldCheckVertical = true
		this.shouldCheckDiagnals = this.isPerfectSquare

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

			displayInfo(players[this.currentPlayerIndex] + "s turn.")

			console.time("Normal win check")
			let [isWinner, winningArray] = this.isPlayerWinner(currentPlayer)
			console.timeEnd("Noraml win check")

			if (isWinner) {
				this.highlightArray(winningArray)
				this.gameOver()
				displayInfo(currentPlayer + " Wins!")
			} else if (this.turnCount >= this.size) {
				this.gameOver()
				displayInfo("Tie!")
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
			cell.addCords(1)
			cell.setOnClick(() => {
				this.playerTurn(cell)
			})
		})
	}

	_isPlayerWinnerRow(player, inner, outer, getCell, innerStart=0, outerStart=0) {
		const cellArray = new Array(inner)
		for (let i = outerStart; i < outer; i++) {
			let isWin = true
			for (let j = innerStart; j < inner; j++) {
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

	isPlayerWinner(player) {
		if (this.turnCount > this.winCheckAfter) {
			let isWin, cellArray

			if (this.shouldCheckHorizontal) {
				[isWin, cellArray] = this._isPlayerWinnerRow(player, this.width, this.height, (x, y) => this.getCell(x, y))
				if (isWin) { return [isWin, cellArray] }
			}
			
			// vertical
			if (this.shouldCheckVertical) {
				[isWin, cellArray] = this._isPlayerWinnerRow(player, this.height, this.width, (y, x) => this.getCell(x, y))
				if (isWin) { return [isWin, cellArray] }
			}
			
			if (this.shouldCheckDiagnals) {			
				// top left to buttom right
				[isWin, cellArray] = this._isPlayerWinnerRow(player, board.height, this.width-this.minWinRowLength+1, (j, i) => this.getCellSafe(j+i, j), 0, this.minWinRowLength-this.height)
				if (isWin) { return [isWin, cellArray] }
				
				// top right to buttom left
				[isWin, cellArray] = this._isPlayerWinnerRow(player, board.height, this.width+(this.width-this.minWinRowLength), (j, i) => this.getCellSafe(i-j, j), 0, this.minWinRowLength-1)
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

	getCellSafe(x, y) {
		let out;
		try {
			out = this.getCell(x, y)
		} catch (error) {}

		return out || PLACEHOLDER_CELL

	}
}

 class CustomWinCondition extends Board {
	constructor(width, height, winRowLength) {
		super(width, height)

		this.minWinRowLength = winRowLength
		this.winCheckAfter = (this.minWinRowLength - 1) * players.length

		this.shouldCheckHorizontal = this.minWinRowLength <= this.width
		this.shouldCheckVertical = this.minWinRowLength <= this.height
		this.shouldCheckDiagnals = this.shouldCheckHorizontal && this.shouldCheckVertical
	}

	_isPlayerWinnerRow(player, inner, outer, getCell, innerStart=0, outerStart=0) {
		const cellArray = new Array(this.minWinRowLength)
		for (let i = outerStart; i < outer; i++) {
			let count = 0
			for (let j = innerStart; j < inner; j++) {
				const cell = getCell(j, i)
				if (cell.val === player) {
					cellArray[count] = cell
					count++
					if (count >= this.minWinRowLength) return [true, cellArray]
				}
				else {
					count = 0
				}
			}
		}
		return [false, null]
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

	if (num > max) {
		let warningMessage = toLargeMessage(name, num, max)
		if (warningMessage !== "") warningMessage += ". "
		if (!confirm(warningMessage + `Do you want to use suggested max size of ${max}?`)) {
			console.warn(toLargeMessage(name, num, max) + ".")
			max = Infinity
		}
	}

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

const board = new (winRowLength === undefined ? Board : CustomWinCondition) (width, height, winRowLength)

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
