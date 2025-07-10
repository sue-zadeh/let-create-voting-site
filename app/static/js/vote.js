(() => {
const invalidButton = document.querySelectorAll('.vms-invalidate');
invalidButton.forEach((button) => {
    const invalidUrl = button.getAttribute('invalid-url');
    button.addEventListener('click', () => {
        console.log(invalidUrl);

        // Window confirm
        const confirm = window.confirm('Are you sure you want to mark votes from this IP as invalid?');
        if (!confirm) {
            return;
        }

        formData = new FormData();
        formData.append('invalid_url', invalidUrl);
        fetch("/invalid_url", {
            method: 'POST',
            body: formData,
        })
        .then((response) => {
            if (response.ok) {
                location.reload();
            }
        });
    });
});

const clearSearchButton = document.querySelector('.vms-clear-search');
if (clearSearchButton) {
    clearSearchButton.addEventListener('click', (event) => {
        document.querySelector('.vms-search-competitor-name').value = '';
        document.querySelector('.vms-search-ip-addr').value = '';
        document.querySelector('.vms-search-start-date').value = '';
        document.querySelector('.vms-search-end-date').value = '';

        document.querySelector('.vms-search-btn').click();
    });
}

})();
