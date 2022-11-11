import { MIN_SIZE, SUGGESTED_MAX_SIZE, DEFAULT_SIZE } from "./consts.js";

const navContainer = document.querySelector(".fixed-container")
const navBar = document.querySelector(".fixed-content")

const navHeight = navBar.offsetHeight

navContainer.style.height = `${navHeight}px`

const maxInputLen = SUGGESTED_MAX_SIZE.toString().length;

const sizeInputs = document.querySelectorAll("input.size");
const boardSizeInputs = document.querySelectorAll("input.board-size");
const winConstionInput = document.querySelector("input#win-condition");
const form = document.getElementById("create-game-form");


let max = -1;
function updateMax() {
	max = -1;
	boardSizeInputs.forEach((el) => {
		if (el.value > max) max = el.value;
	});
	winConstionInput.max = max;
	displayCaption();
}

function validInput(input) {
	input.value = input.value.replace("-", "");
	if (input.value.length > maxInputLen)
		input.value = input.value.slice(0, maxInputLen);
}

sizeInputs.forEach((el) => {
	el.min = MIN_SIZE;
	el.max = SUGGESTED_MAX_SIZE;
});

boardSizeInputs.forEach((el) => {
	el.setAttribute("value", DEFAULT_SIZE); // must use setAttribute for value otherwise built in reset to default does not function
	el.oninput = () => {
		validInput(el);
		updateMax();
	};
});

const winConstionExplanation = document.getElementById("explanation");
function displayCaption() {
	if (max < winConstionInput.value) {
		winConstionExplanation.innerText = `Impossible to get ${winConstionInput.value} in a row with current board sizes.`;
	} else {
		winConstionExplanation.innerText =
			"Get " +
			(winConstionInput.value == ""
				? "all the way accros"
				: `${winConstionInput.value} in a row`) +
			" to win.";
	}
}

winConstionInput.oninput = () => {
	validInput(winConstionInput);
	displayCaption();
};

updateMax();
displayCaption();
form.onreset = () => {
	updateMax();
	displayCaption();
};
