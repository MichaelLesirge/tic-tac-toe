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

export class Board {
	constructor(players, width, height) {
		this.width = width
		this.height = height

        this.players = players

		this.size = this.width * this.height
		
		this.minWinPicesesToWin = Math.min(this.width, this.height)
		this.winCheckForWinAfter = (this.minWinPicesesToWin - 1) * this.players.length

		this.turnCount = 0
		this.gameCount = 0
		this.currentPlayerIndex = 0
		this.isPlaying = true

		this.isDisplayingCords = false

        this.displayInfoTo = console.info
		
		this.winCheckers = {
			horizontal: this._isPlayerWinnerRowPromise(this.width, this.height, (x, y) => this.getCell(x, y)),
			vertical: this._isPlayerWinnerRowPromise(this.height, this.width, (y, x) => this.getCell(x, y)),
			topLeftToButtomRight: this._isPlayerWinnerRowPromise(this.height, this.width-this.minWinPicesesToWin+1, (j, i) => this.getCellWithFallback(j+i, j), 0, this.minWinPicesesToWin-this.height),
			topRightToButtomLeft: this._isPlayerWinnerRowPromise(this.height, this.width+(this.width-this.minWinPicesesToWin), (j, i) => this.getCellWithFallback(i-j, j), 0, this.minWinPicesesToWin-1),
		}
		this.winCheckers.diagonals = [this.winCheckers.topLeftToButtomRight, this.winCheckers.topRightToButtomLeft]

		let isPerfectSquare = this.width === this.height

		this.usedWinChecker = [
			this.winCheckers.horizontal, 
			this.winCheckers.vertical, 
			...((isPerfectSquare) ? this.winCheckers.diagonals : [])
		]

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

	async playerTurn(cell) {
		if (this.isPlaying) {
			resetBoardButton.classList.remove("fade-button")

			const currentPlayer = this.players[this.currentPlayerIndex]

			cell.set(currentPlayer)
			cell.disable()

			this.currentPlayerIndex = (this.turnCount + this.gameCount) % this.players.length
			this.turnCount++

			this.displayInfoTo(this.players[this.currentPlayerIndex] + "s turn.")
						
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
				this.displayInfoTo(currentPlayer + " Wins!")
			} else if (this.turnCount >= this.size) {
				this.gameOver()
				this.displayInfoTo("Tie!")
			}
		}
	}

	newGame() {
		this.isPlaying = true
		this.currentPlayerIndex = this.gameCount % this.players.length
		this.displayInfoTo(`Starting with ${this.players[this.currentPlayerIndex]}s.`)
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
		return [false, undefined]
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
		toggleCordsButton.innerText = `${this.isDisplayingCords ? "Hide" : "Display"} Cords`
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

export class CustomWinConditionBoard extends Board {
	constructor(players, width, height, winRowLength) {
		super(players, width, height)

		this.minWinPicesesToWin = winRowLength
		this.winCheckForWinAfter = (this.minWinPicesesToWin - 1) * this.players.length

		this.usedWinChecker = []

		let checkVertical = this.minWinPicesesToWin <= this.height
		let checkHorizontal = this.minWinPicesesToWin <= this.width

		if (checkVertical) this.usedWinChecker.push(this.winCheckers.vertical)
		if (checkHorizontal) this.usedWinChecker.push(this.winCheckers.horizontal)

		let checkDiagnal = checkVertical && checkHorizontal
		if (checkDiagnal) {
			this.usedWinChecker.push(...this.winCheckers.diagonals)
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