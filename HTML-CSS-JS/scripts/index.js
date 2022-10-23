import { MIN_SIZE, MAX_SIZE, DEFAULT_SIZE } from "./consts.js"

const max_input_len = MAX_SIZE.toString().length

const sizeInputs = document.querySelectorAll("input.size")
const BoardSizeInputs = document.querySelectorAll("input.board-size")
const winConstionInput = document.querySelector("input#win-condition")

sizeInputs.forEach((el) => {
	el.min = MIN_SIZE
	el.max = MAX_SIZE
	el.oninput = () => {
		el.value = el.value.replace("-", "")
		if (el.value.length > max_input_len) el.value = el.value.slice(0, max_input_len)
	}
})

BoardSizeInputs.forEach((el) => {
	el.setAttribute("value", DEFAULT_SIZE);  // must use setAttribute for value otherwise built in reset to default does not funtion
})

const winConstionExplanation = document.getElementById("explanation")
function displayCaption() {
	winConstionExplanation.innerText = "Get " + ((winConstionInput.value == "") ? "all the way accros" : `${winConstionInput.value} in a row`) + " to win"
}

displayCaption()
winConstionInput.oninput = displayCaption
console.log(winConstionInput)
