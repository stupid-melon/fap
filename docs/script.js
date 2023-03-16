function change_content(content) {
    let pre       = document.getElementById('raw_data');
    pre.innerHTML = content;
}


function main() {
    fetch('data.txt')
        .then(response => response.text())
        .then(data => {
            change_content(data);
        });
}



main();