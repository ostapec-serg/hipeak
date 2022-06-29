window.addEventListener('load', () => {
    let filtersButton = document.getElementById('filtersButton');
    let filtersContent = document.getElementById('filtersContent');

    filtersButton.onclick = () => {
        filtersContent.classList.toggle('open');
    }
})