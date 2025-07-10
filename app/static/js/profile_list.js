(function () {
    const clearButton = document.querySelector('.clear-button');
    if (clearButton) {
      clearButton.addEventListener("click", (event) => {
        document.querySelector('#username').value = '';
        document.querySelector('#firstname').value = '';
        document.querySelector('#lastname').value = '';
        document.querySelector('#email').value = '';

        document.querySelector('.search-button').click();
      })
    }
})()