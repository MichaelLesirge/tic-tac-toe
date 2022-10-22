import { MIN_SIZE, MAX_SIZE, DEFAULT_SIZE } from "./consts.js"

const max_input_len = MAX_SIZE.toString().length

document.querySelectorAll("input.size").forEach((el) => {
	el.setAttribute("value", DEFAULT_SIZE);  // must use setAttribute for value otherwise built in reset to default does not funtion
	el.min = MIN_SIZE
	el.max = MAX_SIZE
	el.oninput = () => {
		el.value = el.value.replace("-", "")
		if (el.value.length > max_input_len) el.value = el.value.slice(0, max_input_len)
	}
	
})

