import { MIN_SIZE, SUGGESTED_MAX_SIZE, DEFAULT_SIZE } from "./consts.js"

const toggleCordsButton = document.querySelector("#toggle-cords")
const resetBoardButton = document.querySelector("#reset-button")

const infoSpan = document.querySelector("#info")
const displayInfo = (msg) => (infoSpan.innerText = msg)

// TODO allow users to specify num of players and there letters in home page (index.html)
const players = ["x", "o"].map((element) => element.charAt(0).toUpperCase())

const OFFSET = 1

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

class Board {
	constructor(width = DEFAULT_SIZE, height = DEFAULT_SIZE) {
		this.width = width
		this.height = height

		this.size = this.width * this.height
		
		this.minWinPicesesToWin = null
		this.winCheckForWinAfter = null

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
			
			if (this.isPossibleToWin()) {
				try {
					[isWinner, winningArray] = await this.isPlayerWinner(currentPlayer)
				} catch (error) {
					if (error instanceof AggregateError) {
						[isWinner, winningArray] = [false, undefined]
					} else {
						throw error 
					}
				}		
			}
			
			if (isWinner) {
				winningArray.forEach((cell) => cell.highlight())
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

	_isPlayerWinnerRowPromise(inner, outer, getCell, innerStart=0, outerStart=0) {
		return (player) => {
			return new Promise((resolve, reject) => {
				const [isWin, cellArray] = this._isPlayerWinnerRow(player, inner, outer, getCell, innerStart, outerStart)
				if (isWin) resolve([isWin, cellArray])
				reject([isWin, cellArray])
			})
		}
	}

	isPossibleToWin() {
		return this.turnCount > this.winCheckForWinAfter
	}

	isPlayerWinner(player) {
		return Promise.any(this.usedWinChecker.map((func) => func(player)))
	}

	isOverflowing() {
		for (let y = 0; y < this.height; y++) {
			for (let x = 0; x < this.width; x++) {
				if (this.getCell(x, y).el.getBoundingClientRect().left < 0) return true
			}
		}
		return false
	}

	toggleCords() {
		this.isDisplayingCords = !this.isDisplayingCords
		this.updateCordsVisablity(this.isDisplayingCords)
	}

	updateCordsVisablity() {
		toggleCordsButton.innerText = (this.isDisplayingCords ? "Hide" : "Display") + " Cords"
		this.boardBody.style.setProperty("--cords-visibility", this.isDisplayingCords ? "defalt" : "hidden")
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
		} catch (error) {}

		return out || PLACEHOLDER_CELL

	}
}

class StandardBoard extends Board {
	constructor(width, height) {
		super(width, height)

		this.minWinPicesesToWin = Math.min(this.width, this.height)
		this.winCheckForWinAfter = (this.minWinPicesesToWin - 1) * players.length

		this.usedWinChecker = [
			this._isPlayerWinnerRowPromise(this.width, this.height, (x, y) => this.getCell(x, y)),
			this._isPlayerWinnerRowPromise(this.height, this.width, (y, x) => this.getCell(x, y)),
		]
	
		if (this.width === this.height) {
			this.usedWinChecker = [
				...this.usedWinChecker,
				this._isPlayerWinnerRowPromise(this.height, this.width-this.minWinPicesesToWin+1, (j, i) => this.getCellWithFallback(j+i, j), 0, this.minWinPicesesToWin-this.height),
				this._isPlayerWinnerRowPromise(this.height, this.width+(this.width-this.minWinPicesesToWin), (j, i) => this.getCellWithFallback(i-j, j), 0, this.minWinPicesesToWin-1),
			]
		}
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
		return [false, undefined]
	}
}

class CustomWinCondition extends Board {
	constructor(width, height, winRowLength) {
		super(width, height)

		this.minWinPicesesToWin = winRowLength
		this.winCheckForWinAfter = (this.minWinPicesesToWin - 1) * players.length

		let checkVertical = this.minWinPicesesToWin <= this.height
		let checkHorizontal = this.minWinPicesesToWin <= this.width
		
		if (checkVertical) this.usedWinChecker.push(this._isPlayerWinnerRowPromise(this.width, this.height, (x, y) => this.getCell(x, y)),)
		if (checkHorizontal) this.usedWinChecker.push(this._isPlayerWinnerRowPromise(this.height, this.width, (y, x) => this.getCell(x, y)))

		let checkDiagnal = checkVertical && checkHorizontal
		if (checkDiagnal) {
			this.usedWinChecker = [
				...this.usedWinChecker,
				this._isPlayerWinnerRowPromise(this.height, this.width-this.minWinPicesesToWin+1, (j, i) => this.getCellWithFallback(j+i, j), 0, this.minWinPicesesToWin-this.height),
				this._isPlayerWinnerRowPromise(this.height, this.width+(this.width-this.minWinPicesesToWin), (j, i) => this.getCellWithFallback(i-j, j), 0, this.minWinPicesesToWin-1),
			]
		}
	}

	_isPlayerWinnerRow(player, inner, outer, getCell, innerStart=0, outerStart=0) {
		const cellArray = new Array(this.minWinPicesesToWin)
		for (let i = outerStart; i < outer; i++) {
			let count = 0
			for (let j = innerStart; j < inner; j++) {
				const cell = getCell(j, i)
				if (cell.val === player) {
					cellArray[count] = cell
					count++
					if (count >= this.minWinPicesesToWin) return [true, cellArray]
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

const getUpdateValidSizeParam = (name) => getUpdateValidNumberParam(name, MIN_SIZE, SUGGESTED_MAX_SIZE, DEFAULT_SIZE, (name, num, max) => `Board ${name} of ${num} is to larger than recomend max of ${max}`)

const width = getUpdateValidSizeParam("width")
const height = getUpdateValidSizeParam("height")

const boardSizes = `${width}x${height}`

const winRowLength = getUpdateValidNumberParamIfExists("win-condition", MIN_SIZE, Math.max(width, height), (name, num, max) => `Impossible to get ${num} in a row with current board sizes of ${boardSizes}`)

const newParms = params.toString()
if (oldParems !== newParms) {
	location.search = newParms
}

const board = new (winRowLength === undefined ? StandardBoard : CustomWinCondition) (width, height, winRowLength)

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
