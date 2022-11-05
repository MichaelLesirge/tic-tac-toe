import { MIN_SIZE, SUGGESTED_MAX_SIZE, DEFAULT_SIZE } from "./consts.js"

const toggleCordsButton = document.getElementById("toggle-cords")
const resetBoardButton = document.getElementById("reset-button")

const infoSpan = document.querySelector("#info")
const displayInfo = (msg) => (infoSpan.innerText = msg)

const displayInfoPulse = () => { infoSpan.classList.add("tie"); setTimeout(() => infoSpan.classList.remove("tie"), 1000)} 
const displayInfoPulseGreen = () => { infoSpan.classList.add("win"); setTimeout(() => infoSpan.classList.remove("win"), 1000)} 

// TODO allow users to specify num of players and there letters in home page (index.html)
const players = ["x", "o"].map((element) => element.charAt(0).toUpperCase())

const OFFSET = 0

class Cell {
	constructor(el, name) {
		this.el = el
		this.name = name

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
		cords.innerText = "(" + this.name + ")"
		this.el.appendChild(cords)
	}
}

const PLACEHOLDER_CELL = new Cell(document.createElement("div"), null)

class WinChecker {
	constructor(board, piecesToWin) {
		this.board = board

		let checkVertical, checkHorizontal, checkDiagnal
		if (piecesToWin === undefined) {
			this.winCheckFunc = this.isPlayerWinnerAcross

			this.minPicesesToWin = Math.min(this.board.width, this.board.height)

			checkVertical = true
			checkHorizontal = true

			checkDiagnal = this.board.width === this.board.height

		}
		else {
			this.winCheckFunc = this.isPlayerWinnerCount

			this.minPicesesToWin = piecesToWin

			checkVertical = this.minPicesesToWin <= this.board.height
			checkHorizontal = this.minPicesesToWin <= this.board.width

			checkDiagnal = checkVertical && checkHorizontal
		}
		const allCheckers = {
			verticle: this._isPlayerWinnerRowPromise(0, 0, this.board.width, this.board.height, (x, y) => this.board.getCell(x, y)),
			horizontal: this._isPlayerWinnerRowPromise(0, 0, this.board.height, this.board.width, (x, y) => this.board.getCell(y, x)),
			topLeftToButtomRight: this._isPlayerWinnerRowPromise(0, this.minPicesesToWin - this.board.height, this.board.height, this.board.width - this.minPicesesToWin + 1, (j, i) => this.board.getCellWithFallback(j + i, j)),
			topRightToButtomLeft: this._isPlayerWinnerRowPromise(0, this.minPicesesToWin - 1, this.board.height, this.board.height + (this.board.width - this.minPicesesToWin), (j, i) => this.board.getCellWithFallback(i - j, j)),
		}

		this.usedWinChecker = []

		this.winCheckForWinAfter = (this.minPicesesToWin - 1) * players.length

		if (checkVertical) this.usedWinChecker.push(allCheckers.verticle)
		if (checkHorizontal) this.usedWinChecker.push(allCheckers.horizontal)

		if (checkDiagnal) this.usedWinChecker.push(
			allCheckers.topLeftToButtomRight,
			allCheckers.topRightToButtomLeft,
		)
	}

	async isPlayerWinner(player) {
		let [isWinner, winningArray] = [false, undefined]
		if (this.isPossibleToWin()) {
			try {
				[isWinner, winningArray] = await Promise.any(this.usedWinChecker.map((func) => func(player)))
			} catch (error) {
				if (!(error instanceof AggregateError)) throw error
			}
		}
		return [isWinner, winningArray]
	}

	_isPlayerWinnerRowPromise(innerStart, outerStart, inner, outer, getCell) {
		return (player) => {
			return new Promise((resolve, reject) => {
				const [isWin, cellArray] = this.winCheckFunc(player, innerStart, outerStart, inner, outer, getCell)
				if (isWin) resolve([isWin, cellArray])
				reject([isWin, cellArray])
			})
		}
	}

	isPossibleToWin() {
		return this.board.turnCount > this.winCheckForWinAfter
	}

	isPlayerWinnerAcross(player, innerStart, outerStart, inner, outer, getCell) {
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
		return [false, undefined]
	}

	isPlayerWinnerCount(player, innerStart, outerStart, inner, outer, getCell) {
		const cellArray = new Array(this.minPicesesToWin)
		for (let i = outerStart; i < outer; i++) {
			let count = 0
			for (let j = innerStart; j < inner; j++) {
				const cell = getCell(j, i)
				if (cell.val === player) {
					cellArray[count] = cell
					count++
					if (count >= this.minPicesesToWin) return [true, cellArray]
				}
				else {
					count = 0
				}
			}
		}
		return [false, null]
	}
}

class Board {
	constructor(width, height, piecesToWin) {
		this.width = width
		this.height = height

		this.size = this.width * this.height

		this.turnCount = 0
		this.gameCount = 0
		this.currentPlayerIndex = 0
		this.isPlaying = true

		this.isDisplayingCords = false

		this.usedWinChecker = []

		this.boardArray = Array(this.height)
		this.boardBody = document.querySelector(".board-body")

		// create board on page and in array
		for (let y = 0; y < this.height; y++) {
			this.boardArray[y] = Array(this.width)
			let tableRow = this.boardBody.insertRow()
			for (let x = 0; x < this.width; x++) {
				const el = tableRow.insertCell()
				const cordName = (x + OFFSET) + "," + (y + OFFSET)

				let cell = new Cell(el, cordName)
				this.boardArray[y][x] = cell
			}
		}

		this.winChecker = new WinChecker(this, piecesToWin)
		this.updateCordsVisablity()
	}

	async playerTurn(cell) {
		if (this.isPlaying) {
			resetBoardButton.classList.remove("fade-button")

			const currentPlayer = players[this.currentPlayerIndex]

			cell.set(currentPlayer)
			cell.disable()

			this.currentPlayerIndex = (this.turnCount + this.gameCount) % players.length
			this.turnCount++

			displayInfo(players[this.currentPlayerIndex] + "s turn.")

			let isWinner = false
			let winningArray

			[isWinner, winningArray] = await this.winChecker.isPlayerWinner(currentPlayer)


			if (isWinner) {
				winningArray.forEach((cell) => cell.highlight())
				this.gameOver()
				displayInfo(currentPlayer + " Wins!")
				displayInfoPulseGreen()
			} else if (this.turnCount >= this.size) {
				this.gameOver()
				displayInfo("Tie!")
				displayInfoPulse()
			}
		}
	}

	newGame() {
		this.isPlaying = true
		this.currentPlayerIndex = this.gameCount % players.length
		displayInfo(`Starting with ${players[this.currentPlayerIndex]}s.`)
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

	isOverflowing() {
		return this.getCell(0, 0).el.getBoundingClientRect().left < 0
	}

	toggleCords() {
		this.isDisplayingCords = !this.isDisplayingCords
		this.updateCordsVisablity()
	}

	updateCordsVisablity() {
		toggleCordsButton.innerText = (this.isDisplayingCords ? "Hide" : "Display") + " Cords"
		this.setCssVar("cords-visibility", this.isDisplayingCords ? "block" : "none")
	}

	setCssVar(name, value) {
		this.boardBody.style.setProperty("--" + name, value)
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

	getCellWithFallback(x, y) {
		let out;
		try {
			out = this.getCell(x, y)
		} catch (error) {
			return PLACEHOLDER_CELL
		}

		return out || PLACEHOLDER_CELL

	}
}

// get board varibles

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
			console.warn(warningMessage)
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

const params = new URLSearchParams(location.search)
const oldParems = params.toString()

const getUpdateValidSizeParam = (name) => getUpdateValidNumberParam(name, MIN_SIZE, SUGGESTED_MAX_SIZE, DEFAULT_SIZE, (name, num, max) => `Board ${name} of ${num} is to larger than recomend max of ${max}`)

const width = getUpdateValidSizeParam("width")
const height = getUpdateValidSizeParam("height")

const boardSizes = `${width}x${height}`

const winRowLength = getUpdateValidNumberParamIfExists("win-condition", MIN_SIZE, Math.max(width, height), (name, num, max) => `Impossible to get ${num} in a row with current board sizes of ${boardSizes}`)

const newParms = params.toString()
if (oldParems !== newParms) {
	location.search = newParms
}

// start game
document.querySelector("title").innerText += ` (${boardSizes})`

const board = new Board(width, height, winRowLength)
board.newGame()

// fix overflow

const boardClassList = document.querySelector(".board-container").classList
const bodyStyle = document.body.style
function fixOverflow() {
	if (board.isOverflowing()) {
		boardClassList.remove("centered-container")
		bodyStyle.overflowX = "scroll"
	} else {
		boardClassList.add("centered-container")
		bodyStyle.overflowX = "hidden"
	}
}

fixOverflow()
window.onresize = fixOverflow

// nav buttons

resetBoardButton.onclick = () => board.newGame()
toggleCordsButton.onclick = () => board.toggleCords()

// zoom in / out

const zoomScaleDisplay = document.getElementById("zoom-scale-display")

let zoomScale = 0
function changeZoomScaleBy(by) {
	zoomScale += by
	fixOverflow()
	board.setCssVar("zoom-scale", zoomScale + "vmin")
	zoomScaleDisplay.innerText = 100 + zoomScale
	fixOverflow()
}

const zoomInBtn = document.getElementById("zoom-in")
const zoomOutBtn = document.getElementById("zoom-out")

const zoomScaleChangeBy = 1;
const zoomInFunc = () => changeZoomScaleBy(zoomScaleChangeBy)
const zoomOutFunc = () => changeZoomScaleBy(-zoomScaleChangeBy)

zoomInBtn.onmousedown = zoomInFunc
zoomOutBtn.onmousedown = zoomOutFunc
