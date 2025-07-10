(function () {
    const confirm_dialog = document.getElementById('confirm_dialog')
    if (confirm_dialog) {
      confirm_dialog.addEventListener('show.bs.modal', event => {
        // Button that triggered the modal
        const button = event.relatedTarget
        // Extract info from data-bs-* attributes
        const delete_message_url = button.getAttribute('data-bs-delete-message-url')
        const message_title = button.getAttribute('data-bs-message-title')
        // If necessary, you could initiate an Ajax request here
        // and then do the updating in a callback.

        // Update the modal's content.
        const modalBody = confirm_dialog.querySelector('.modal-body')
        modalBody.textContent = message_title

        confirm_dialog.querySelector('#delete_button').setAttribute('data-bs-delete-message-url', delete_message_url);
      })

      confirm_dialog.querySelector('#delete_button').addEventListener('click', event => {
        const button = event.target;
        const url = button.getAttribute('data-bs-delete-message-url');

        const request = new Request(url, { method: "DELETE" });
        fetch(request).then((response) => { location.reload() });
      })
    }

    const confirm_delete_reply_dialog = document.getElementById('confirm_delete_reply_dialog')
    if (confirm_delete_reply_dialog) {
      confirm_delete_reply_dialog.addEventListener('show.bs.modal', event => {
        // Button that triggered the modal
        const button = event.relatedTarget
        // Extract info from data-bs-* attributes
        const delete_reply_url = button.getAttribute('data-bs-delete-reply-url')
        const reply_content = button.getAttribute('data-bs-reply-content')
        // If necessary, you could initiate an Ajax request here
        // and then do the updating in a callback.

        // Update the modal's content.
        const modalBody = confirm_delete_reply_dialog.querySelector('.modal-body')
        modalBody.textContent = reply_content

        confirm_delete_reply_dialog.querySelector('#delete_reply_button').setAttribute('data-bs-delete-reply-url', delete_reply_url);
      })

      confirm_delete_reply_dialog.querySelector('#delete_reply_button').addEventListener('click', event => {
        const button = event.target;
        const url = button.getAttribute('data-bs-delete-reply-url');

        const request = new Request(url, { method: "DELETE" });
        fetch(request).then((response) => { location.reload() });
      })
    }

    document.querySelector('#post_message_button').addEventListener('click', event => {
      const button = event.target;
      const url = button.getAttribute('data-tmb-post-message-url');
      const message_title_element = document.querySelector('#message_title');
      const message_title = message_title_element.value;
      const message_content = document.querySelector('#message_content').value;

      if (message_title == '') {
        message_title_element.classList.add('is-invalid');
        message_title_element.nextElementSibling.innerHTML = 'A title is required';
      }
      else {
        message_title_element.classList.remove('is_invalid')
        message_title_element.nextElementSibling.innerHTML = '';

        const formData = new FormData();
        formData.append('message_title', message_title);
        formData.append('message_content', message_content);

        fetch(url, { method: "POST", body: formData }).then((response) => { location.reload() });
      }
    })

    replies = document.querySelectorAll('.reply-button');
    for (reply_button of replies) {
      reply_button.addEventListener('click', event => {
        const button = event.target;
        const url = button.getAttribute('data-tmb-reply-url');
        const message_id = button.getAttribute('data-tmb-message-id');
        const reply_content_element = button.parentElement.firstElementChild.firstElementChild;
        const reply_content = reply_content_element.value;

        if (reply_content != '') {
            reply_content_element.value = '';
            reply_content_element.classList.remove('is-invalid');

            const formData = new FormData();
            formData.append('message_id', message_id);
            formData.append('reply_content', reply_content);

            fetch(url, { method: "POST", body: formData }).then((response) => { location.replace('/#message_' + message_id); location.reload() });
        }
        else {
            reply_content_element.classList.add('is-invalid');
        }
      })
    }
  })()