import { MIN_SIZE, MAX_SIZE, DEFAULT_SIZE } from "./consts.js"

document.querySelectorAll("input.size").forEach((el) => {
	el.setAttribute("value", DEFAULT_SIZE)
	el.setAttribute("min", MIN_SIZE)
	el.setAttribute("max", MAX_SIZE)
})
