(function () {
  confirmDialog = document.getElementById('confirm-dialog');
  if (confirmDialog) {
    confirmDialog.addEventListener('show.bs.modal', event => {
      // Button that triggered the modal
      const button = event.relatedTarget;
      // Extract info from data-vms-* attributes
      const deleteEventUrl = button.getAttribute('data-vms-delete-event-url');
      const eventName = button.getAttribute('data-vms-event-name');

      // Update the modal's content.
      const modalBody = confirmDialog.querySelector('.modal-body');
      modalBody.textContent = eventName;

      confirmDialog.querySelector('.delete-button').setAttribute('data-vms-delete-event-url', deleteEventUrl);
    });

    // button to delete a event (id = delete_event)
    confirmDialog.querySelector('.delete-button').addEventListener('click', event => {
      const button = event.target;
      const deleteEventUrl = button.getAttribute('data-vms-delete-event-url');

      // Delete event
      const request = new Request(deleteEventUrl, { method: "DELETE" });
      fetch(request).then((response) => { location.reload() });
    });
  }

  // button to save a event
  const editEventDetails = document.getElementById('add-event');
  if (editEventDetails) {
    editEventDetails.addEventListener('show.bs.modal', event => {
      const button = event.relatedTarget;
      const saveEventUrl = button.getAttribute('data-vms-save-event-url');
      editEventDetails.querySelector('.save-button').setAttribute('data-vms-save-event-url', saveEventUrl);

      document.getElementById('event_name').value = '';
      document.getElementById('event_description').value = '';
      document.getElementById('event_start_date').value = '';
      document.getElementById('event_end_date').value = '';
      document.querySelector('.vms-add-event-feedback').textContent = '';
    });

    function checkValidEventDates(startDate, endDate) {
      // start date and end date must be in the future
      const currentDate = new Date();
      const startDateDate = new Date(startDate);
      const endDateDate = new Date(endDate);
      
      if (startDateDate <= currentDate) {
        document.getElementById('event_start_date').classList.add('is-invalid');
        window.alert('Start date must be in the future');
        return false;
      }
      if (endDateDate < currentDate) {
        document.getElementById('event_end_date').classList.add('is-invalid');
        window.alert('End date must be in the future');
        return false;
      }
      if (startDateDate > endDateDate) {
        document.getElementById('event_end_date').classList.add('is-invalid');
        window.alert('End date must be after start date');
        return false;
      }

      return true;
    }

    // add button click event
    editEventDetails.querySelector('.save-button').addEventListener('click', event => {
      const name = document.getElementById('event_name').value;
      const description = document.getElementById('event_description').value;
      const startDate = document.getElementById('event_start_date').value;
      const endDate = document.getElementById('event_end_date').value;
      const button = event.target;
      const saveEventUrl = button.getAttribute('data-vms-save-event-url');
      

      if (!checkValidEventDates(startDate, endDate)) {
        return;
      }

      // create form data
      const formData = new FormData();
      formData.append('name', name);
      formData.append('description', description);
      formData.append('start_date', startDate);
      formData.append('end_date', endDate);

      // send request
      fetch(saveEventUrl, { method: "PUT", body: formData })
        .then((response) => {
          if (response.status == 400) {
            response.text().then(data => {
              if (data != '') {
                document.querySelector('.vms-add-event-feedback').textContent = data;
              }
            })
          }
          else {
            location.reload();
          }
        });
    });
  }

  // button to update a event
  const updateEventDetails = document.getElementById('update-event');
  if (updateEventDetails) {
    updateEventDetails.addEventListener('show.bs.modal', event => {
      const button = event.relatedTarget;
      const saveEventUrl = button.getAttribute('data-vms-save-event-url');
      updateEventDetails.querySelector('.save-button').setAttribute('data-vms-save-event-url', saveEventUrl);
      
      document.getElementById('update_event_start_date').value = button.getAttribute('data-bs-start-date');
      document.getElementById('update_event_end_date').value = button.getAttribute('data-bs-end-date');
      document.querySelector('.vms-edit-event-feedback').textContent = '';
    });

    // add button click event
    updateEventDetails.querySelector('.save-button').addEventListener('click', event => {
      const startDate = document.getElementById('update_event_start_date').value;
      const endDate = document.getElementById('update_event_end_date').value;
      const button = event.target;
      const saveEventUrl = button.getAttribute('data-vms-save-event-url');

      if (!checkValidEventDates(startDate, endDate)) {
        return;
      }

      // create form data
      const formData = new FormData();
      formData.append('start_date', startDate);
      formData.append('end_date', endDate);
      console.log(formData);

      // send request
      fetch(saveEventUrl, { method: "PUT", body: formData })
        .then((response) => {
          if (response.status == 400) {
            response.text().then(data => {
              if (data != '') {
                document.querySelector('.vms-edit-event-feedback').textContent = data;
              }
            })
          }
          else {
            location.reload();
          }
        });
    });
  }

})()





