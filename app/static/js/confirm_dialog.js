( () => {

document.querySelectorAll('.vms-modal-dialog').forEach((vmsDialog) => {
    vmsDialog.addEventListener('show.bs.modal', event => {
        // Button that triggered the modal
        const button = event.relatedTarget;
        // Extract info from data-vms-* attributes
        const url = button.getAttribute('data-vms-url');
        const id_data = button.getAttribute('data-vms-url-id');
        const modalTitleValue = button.getAttribute('data-vms-modal-title');
        const modalBodyValue = button.getAttribute('data-vms-modal-body');
        // Update the modal's content.
        const modalTitle = vmsDialog.querySelector('.modal-title');
        modalTitle.textContent = modalTitleValue;
        const modalBody = vmsDialog.querySelector('.modal-body-description');
        modalBody.textContent = modalBodyValue;
        const confirmButton = vmsDialog.querySelector('.vms-confirm-button');
        confirmButton.setAttribute('data-vms-url', url);
        confirmButton.setAttribute('data-vms-url-id', id_data);
        confirmButton.textContent = button.getAttribute('data-vms-action-text');

        
        const validation = vmsDialog.querySelector('.vms-modal-validation');
        validation.style.display = 'none';
        const textArea = vmsDialog.querySelector('.modal-text-area');
        if (button.getAttribute('data-vms-modal-need-reason') == 'yes') {
            textArea.style.display = 'block';
            textArea.value = '';
        }
        else {
            textArea.style.display = 'none';
        }
    });
});

document.querySelectorAll('.vms-confirm-button').forEach((button) => {
    button.addEventListener('click', event => {
        const button = event.target;
        const url = button.getAttribute('data-vms-url');

        const modalContent = button.parentElement.parentElement;
        const textArea = modalContent.querySelector('.modal-text-area');
        const bodyData = {'id_data': button.getAttribute('data-vms-url-id')};
        if (textArea.style.display != 'none') {
            if (textArea.value.trim() == '') {
                const validation = modalContent.querySelector('.vms-modal-validation');
                validation.textContent = "Please provide a reason";
                validation.style.display = "block";
                return;
            }
            bodyData['reason'] = textArea.value.trim();
        }

        // Fetch url, then reload
        const request = new Request(url, { method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(bodyData)});
        fetch(request).then((response) => { location.reload() });
    });
});

}) ();