export const MIN_SIZE = 1;
export const SUGGESTED_MAX_SIZE = 99;
export const DEFAULT_SIZE = 3;

const navContainer = document.querySelector(".fixed-container");
const navBar = document.querySelector(".fixed-content");

export function setNavContainer() {
	const navHeight = navBar.offsetHeight;
	navContainer.style.height = `${navHeight}px`;
}
