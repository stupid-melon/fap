const checkbox = document.querySelector('.theme-switch__checkbox');
checkbox.addEventListener('change', function() {switchTheme(this);});
// Switch theme onload
document.addEventListener('DOMContentLoaded', function() {initialiseSetTheme();});



function initialiseSetTheme() {
    // If its the first time the user visits the site
    if (localStorage.getItem('theme') === null) {
        checkbox.checked = true;
        localStorage.setItem('theme', 'dark');
        console.log('First visit detected, setting default theme to dark');
    }
    else {checkbox.checked = localStorage.getItem('theme') === 'dark';}

    switchTheme();
}



// Theme switching functionality
function switchTheme() {
    const isDark = checkbox.checked;
    console.log('Theme switch toggled:', isDark ? 'Dark' : 'Light');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    
    // Remove existing theme classes
    document.documentElement.classList.remove('light-theme', 'dark-theme');
    
    // Add appropriate theme class
    if (isDark) {
        document.documentElement.classList.add('dark-theme');
        setCalPlotsTheme('dark');
        Array.from(document.getElementsByClassName('dark-charts')) .forEach(el => {el.style.display = 'block';});
        Array.from(document.getElementsByClassName('light-charts')).forEach(el => {el.style.display = 'none';});
    } else {
        document.documentElement.classList.add('light-theme');
        setCalPlotsTheme('light');
        Array.from(document.getElementsByClassName('dark-charts')) .forEach(el => {el.style.display = 'none';});
        Array.from(document.getElementsByClassName('light-charts')).forEach(el => {el.style.display = 'block';});
    }

    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}



// Function to change the color of unfilled cells
function setCalPlotsTheme(theme = null) {
    // If no theme is provided, check localStorage or default to checkbox state
    if (!theme) {
        if (localStorage.getItem('theme') !== null) {theme = localStorage.getItem('theme');}
        else {theme = checkbox.checked ? 'dark' : 'light';}
    }

    // For every svg in a .cal-plot-container, set the data-theme attribute
    document.querySelectorAll('.cal-plot-container svg').forEach(svg => {svg.setAttribute('data-theme', theme);});
}




