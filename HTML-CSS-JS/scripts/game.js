import { MIN_SIZE, SUGGESTED_MAX_SIZE, DEFAULT_SIZE } from "./consts.js";

// sorry for this mess of a program, I was learning JavaScript as I went.

const resetBoardButton = document.getElementById("reset-button");

const infoSpan = document.querySelector("#info");
const displayInfo = (msg) => (infoSpan.innerText = msg);

const displayInfoPulse = () => {
	infoSpan.classList.add("tie");
	setTimeout(() => infoSpan.classList.remove("tie"), 1000);
};
const displayInfoPulseGreen = () => {
	infoSpan.classList.add("win");
	setTimeout(() => infoSpan.classList.remove("win"), 1000);
};

// TODO allow users to specify num of players and there letters in home page (index.html)
const players = ["x", "o"].map((element) => element.charAt(0).toUpperCase());

const OFFSET = 1;

class Cell {
	constructor(el, name) {
		this.name = "(" + name + ")";
		this.el = el;
		
		this.el.addEventListener("keydown", (event) => {
			let selectedEl;
			switch (event.key) {
				case " ":
					case "Enter":
						this.el.click();
						selectedEl = this.el;
						break;
						case "ArrowUp":
							selectedEl = this.el.parentElement?.previousElementSibling?.children[this.el.cellIndex];
							break;
							case "ArrowDown":
								selectedEl = this.el.parentElement?.nextElementSibling?.children[this.el.cellIndex];
					break;
				case "ArrowRight":
					selectedEl = this.el.nextElementSibling;
					break;
					case "ArrowLeft":
						selectedEl = this.el.previousElementSibling;
						break;
					}
					if (selectedEl) {
				// make function that selects and unselects element
				if (this.disabled) this.el.removeAttribute("tabIndex");
				selectedEl.setAttribute("tabIndex", 0);
				selectedEl.focus();
			}
		});
		
		this.reset();
	}
	
	set(text) {
		this.val = this.el.innerText = text;
		this.el.title = text + " " + this.name;
	}
	
	reset() {
		this.disabled = false;
		this.el.title = this.name;
		this.set("");
		this.el.classList.remove("disabled", "highlighted");
		this.el.setAttribute("tabIndex", 0);
	}

	disable() {
		this.disabled = true;
		this.el.onclick = () => {};
		this.el.classList.add("disabled");
		this.el.removeAttribute("tabIndex");
	}

	highlight() {
		this.el.classList.add("highlighted");
	}

	setOnClick(onclickFunc) {
		this.el.onclick = onclickFunc;
	}
}

class Board {
	constructor(width, height, piecesToWinHorizontal, piecesToWinVertical, piecesToWinDiagonal) {
		this.width = width;
		this.height = height;

		this.size = this.width * this.height;

		this.piecesToWinHorizontal = piecesToWinHorizontal;
		this.piecesToWinVertical = piecesToWinVertical;
		this.piecesToWinDiagonal = piecesToWinDiagonal;

		this.turnCount = 0;
		this.gameCount = 0;
		this.currentPlayerIndex = 0;
		this.isPlaying = true;

		this.boardArray = Array(this.height);
		this.boardBody = document.querySelector(".board-body");

		// create board on page and in array
		for (let y = 0; y < this.height; y++) {
			this.boardArray[y] = Array(this.width);
			let tableRow = this.boardBody.insertRow();
			for (let x = 0; x < this.width; x++) {
				const el = tableRow.insertCell();
				const coordName = x + OFFSET + "," + (y + OFFSET);

				let cell = new Cell(el, coordName);
				this.boardArray[y][x] = cell;
			}
		}
	}

	playerTurn(cell) {
		if (this.isPlaying) {
			resetBoardButton.classList.remove("fade-button");

			const currentPlayer = players[this.currentPlayerIndex];

			cell.set(currentPlayer);
			cell.disable();

			const winningArray = this.isPlayerWinner(currentPlayer);

			if (winningArray) {
				winningArray.forEach((cell) => cell.highlight());
				this.gameOver();
				displayInfo(currentPlayer + " Wins!");
				displayInfoPulseGreen();
			} else if (this.turnCount >= this.size) {
				this.gameOver();
				displayInfo("Tie!");
				displayInfoPulse();
			} else {
				this.turnCount++;

				this.currentPlayerIndex = (this.turnCount + this.gameCount) % players.length;

				const nextPlayer = players[this.currentPlayerIndex];
				displayInfo(nextPlayer + "s turn.");
				this.forEach((cell) => cell.el.setAttribute("next-player", nextPlayer));
			}
		}
	}

	getContinuousCells(x, y, dx, dy, player) {
		let cells = [];
        while (this.isInBoard(x, y) && this.getCell(x, y).val === player) {
            cells.push(this.getCell(x, y))
            x += dx;
            y += dy;
        }
        return cells;
    }

    checkHorizontal(player) {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width - this.piecesToWinHorizontal + 1; x++) {
				const cells = this.getContinuousCells(x, y, 1, 0, player);
                if (cells.length >= this.piecesToWinHorizontal) return cells;
            }
        }
        return null;
    }

    checkVertical(player) {
        for (let y = 0; y < this.height - this.piecesToWinVertical + 1; y++) {
            for (let x = 0; x < this.width; x++) {
				const cells = this.getContinuousCells(x, y, 0, 1, player);
                if (cells.length >= this.piecesToWinVertical) return cells;
            }
        }
        return null;
    }

    checkDiagonal(player) {
        for (let y = 0; y < this.height - this.piecesToWinDiagonal + 1; y++) {
            for (let x = 0; x < this.width - this.piecesToWinDiagonal + 1; x++) {
				const cellsD = this.getContinuousCells(x, y, 1, 1, player);
				if (cellsD.length >= this.piecesToWinDiagonal) return cellsD
				
                const cellsU = this.getContinuousCells(x + this.piecesToWinDiagonal - 1, y, -1, 1, player);
				if (cellsU.length >= this.piecesToWinDiagonal) return cellsU;
            }
        }
        return null;
    }

    isPlayerWinner(player) {
        return (
            (this.isPossibleToWin(this.piecesToWinHorizontal) && this.checkHorizontal(player)) ||
            (this.isPossibleToWin(this.piecesToWinVertical) && this.checkVertical(player)) ||
            (this.isPossibleToWin(this.piecesToWinDiagonal) && this.checkDiagonal(player))
        );
    }

	newGame() {
		this.isPlaying = true;
		this.currentPlayerIndex = this.gameCount % players.length;

		displayInfo(`Starting with ${players[this.currentPlayerIndex]}s.`);
		this.forEach((cell) => cell.el.setAttribute("next-player", players[this.currentPlayerIndex]));

		this.turnCount = 1;

		this.reset();
		resetBoardButton.classList.add("fade-button");

		this.gameCount++;
	}

	isPossibleToWin(piecesToWin) {
		return this.turnCount > (piecesToWin - 1) * players.length;
	}

	isInBoard(x, y) {
		return x > -1 && x < this.width && y > -1 && y < this.height;
	}

	gameOver() {
		this.isPlaying = false;
		this.forEach((cell) => cell.disable());
	}

	reset() {
		this.forEach((cell) => {
			cell.reset();
			cell.setOnClick(() => {
				this.playerTurn(cell);
			});
		});
	}

	isMidGame() {
		return board.isPlaying && board.turnCount != 1;
	}

	isOverflowing() {
		return this.getCell(0, 0).el.getBoundingClientRect().left < 0 || this.getCell(this.width - 1, 0).el.getBoundingClientRect().right > (window.innerWidth || document.documentElement.clientWidth);
	}

	setCssVar(name, value) {
		this.boardBody.style.setProperty("--" + name, value);
	}

	getCssVar(name) {
		return getComputedStyle(this.boardBody).getPropertyValue("--" + name);
	}

	forEach(callback) {
		for (let y = 0; y < this.height; y++) {
			for (let x = 0; x < this.width; x++) {
				callback(this.getCell(x, y));
			}
		}
	}

	getCell(x, y) {
		return this.boardArray[y][x];
	}
}

const params = new URLSearchParams(location.search);

function getNumberParam(name) {
	return parseInt(params.get(name));
}

function validNumber(num, min, max, fallback = undefined) {
	return isNaN(num) ? fallback : Math.max(min, Math.min(max, num));
}

function makeBoard() {
	function getUpdateValidNumberParam(name, min, max, fallback = undefined, toLargeMessage = () => "") {
		const num = getNumberParam(name);

		if (num > max) {
			let warningMessage = toLargeMessage(name, num, max);
			if (warningMessage !== "") warningMessage += ". ";
			if (!confirm(warningMessage + `Do you want to use suggested max size of ${max}?`)) {
				console.warn(warningMessage);
				max = Infinity;
			}
		}

		const newNum = validNumber(num, min, max, fallback);

		params.set(name, newNum);

		return newNum;
	}

	function getUpdateValidNumberParamIfExists(name, min, max, toLargeMessage) {
		if (params.has(name)) {
			if (!isNaN(getNumberParam(name))) {
				return getUpdateValidNumberParam(name, min, max, undefined, toLargeMessage);
			}
			params.delete(name);
		}
		return undefined;
	}

	const oldParams = params.toString();

	const getUpdateValidSizeParam = (name) =>
		getUpdateValidNumberParam(name, MIN_SIZE, SUGGESTED_MAX_SIZE, DEFAULT_SIZE, (name, num, max) => `Board ${name} of ${num} is to larger than recomend max of ${max}`);

	const width = getUpdateValidSizeParam("width");
	const height = getUpdateValidSizeParam("height");

	const boardTitle = `${width}x${height}`;

	const winRowLength = getUpdateValidNumberParamIfExists(
		"win-condition",
		MIN_SIZE,
		Math.max(width, height),
		(name, num, max) => `Impossible to get ${num} in a row with current board sizes of ${boardTitle}`
	);

	const newParams = params.toString();
	if (oldParams !== newParams) {
		const newURL = new URL(location);
		newURL.search = newParams;
		history.pushState({}, null, newURL);
	}

	return [new Board(width, height, ...(winRowLength ? [winRowLength, winRowLength, winRowLength] : [width, height, width === height ? width : undefined])), boardTitle];
}

const [board, boardTitle] = makeBoard();
document.querySelector("head title").innerText += ` (${boardTitle})`;
board.newGame();

// nav buttons
resetBoardButton.onclick = () => board.newGame();

// fix overflow
const boardContainer = document.querySelector(".board-container");
const bodyStyle = document.body.style;
function fixOverflow() {
	if (board.isOverflowing()) {
		boardContainer.classList.remove("centered-container");
		bodyStyle.overflowX = "scroll";
	} else {
		boardContainer.classList.add("centered-container");
		bodyStyle.overflowX = "hidden";
	}
}

fixOverflow();
window.onresize = fixOverflow;

// zoom in / out
{
	const zoomScaleChangeAmount = 1;

	const RepeatDelayMs = 500;
	const repeatRateMs = 33;

	const maxScaleVal = 500;

	{
		const zoomScaleDisplay = document.getElementById("zoom-scale-display");

		const startingScale = parseInt(board.getCssVar("starting-zoom-scale"));

		let zoomScale = localStorage.getItem(`z-${boardTitle}`);
		if (zoomScale === null) {
			zoomScale = parseInt(board.getCssVar("zoom-scale"));
		}

		const maxScale = maxScaleVal + startingScale - 100;

		const zoomInBtn = document.getElementById("zoom-in");
		const zoomOutBtn = document.getElementById("zoom-out");

		function setZoomScale(x) {
			zoomScale = Math.min(Math.max(x, 1), maxScale);

			zoomScaleDisplay.innerText = 100 - startingScale + zoomScale;

			fixOverflow();
			localStorage.setItem(`z-${boardTitle}`, zoomScale);

			board.setCssVar("zoom-scale", x + "vmin");

			zoomOutBtn.disabled = zoomScale === 1;
			zoomInBtn.disabled = zoomScale === maxScale;

			fixOverflow();
		}

		function changeZoomScale(by) {
			setZoomScale(zoomScale + by);
		}

		function addHeldEventListener(btn, func) {
			let id;
			["mousedown", "touchstart"].forEach((event) => {
				btn.addEventListener(event, (e) => {
					e.stopPropagation();
					func();
					const startTime = new Date().getTime();
					let last = false;
					id = setInterval(() => {
						if (btn.disabled) clearInterval(id);
						if (last || startTime + RepeatDelayMs < new Date().getTime()) {
							last = true;
							func();
						}
					}, repeatRateMs);
				});
			});

			["mouseup", "touchend", "mouseleave"].forEach((event) => {
				btn.addEventListener(event, (e) => clearInterval(id));
			});
		}

		setZoomScale(zoomScale);

		addHeldEventListener(zoomInBtn, () => changeZoomScale(zoomScaleChangeAmount));
		addHeldEventListener(zoomOutBtn, () => changeZoomScale(-zoomScaleChangeAmount));
	}
}

window.onbeforeunload = () => {
	if (board.isMidGame()) return `Are you sure you want to leave? All game progges will be lossed.`;
};
