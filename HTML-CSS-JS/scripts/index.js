const MIN_SIZE = 1;
const MAX_SIZE = 100;
const DEFAULT_SIZE = 3;

document.querySelectorAll(".size-input").forEach( el => {
    el.value = DEFAULT_SIZE
    el.min = MIN_SIZE
    el.max = MAX_SIZE
})