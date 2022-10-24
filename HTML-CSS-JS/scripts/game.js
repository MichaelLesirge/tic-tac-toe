import { MIN_SIZE, MAX_SIZE, DEFAULT_SIZE } from "./consts.js"
import { Board, CustomWinConditionBoard } from "./board.js"

// TODO allow users to specify num of players and there letters in home page (index.html)
const players = ["x", "o"].map((element) => element.charAt(0).toUpperCase())

const params = new URLSearchParams(location.search)
const oldParems = params.toString()

const infoSpan = document.querySelector("#info")
const displayInfo = (msg) => (infoSpan.innerText = msg)

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

const board = new (winRowLength === undefined ? Board : CustomWinConditionBoard) (players, width, height, winRowLength)
board.displayInfoTo = displayInfo


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
