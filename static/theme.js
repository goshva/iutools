function setTheme(theme) {
		localStorage.setItem('theme', theme);
		document.documentElement.className = theme;
}

function toggleTheme() {
	setTheme(
		localStorage.getItem('theme') === 'theme-light'?'theme-dark':'theme-light'
	)
}

(() => 
	setTheme(
		localStorage.getItem('theme') === 'theme-dark'?'theme-dark':'theme-light'
	)
)();