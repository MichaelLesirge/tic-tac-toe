import {MIN_SIZE, MAX_SIZE, DEFAULT_SIZE} from "./consts.js"

document.querySelectorAll(".size-input").forEach( el => {
    el.value = DEFAULT_SIZE
    el.min = MIN_SIZE
    el.max = MAX_SIZE
})