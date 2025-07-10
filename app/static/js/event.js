(function () {
  // Javascript stuff e.g.
  /*
 
  function sayHello() {
    alert('Hello World');
  }
  
  sayHello();
  
  */
  const competitorDetails = document.getElementById('competitor-details')
  if (competitorDetails) {
    competitorDetails.addEventListener('show.bs.modal', event => 
    {
      var button = event.relatedTarget;

      var competitorName = button.getAttribute("data-bs-name");

      var competitorDescription = button.getAttribute("data-bs-description");

      var modalTitle = competitorDetails.querySelector("#competitor-name");

      var modalContent = competitorDetails.querySelector('#competitor-description');

      var competitorImage = button.getAttribute("data-vms-image");
      var imgCompetitor = competitorDetails.querySelector('.vms-competitor-image');

      modalTitle.textContent = competitorName;
      modalContent.textContent = competitorDescription;
      imgCompetitor.src = competitorImage;
    }
    )
  }

  const editCompetitorDetails = document.getElementById('edit-competitor-details')
  if (editCompetitorDetails) {
    var imgSelect = editCompetitorDetails.querySelector('.vms-img-select');

    editCompetitorDetails.addEventListener('show.bs.modal', event => 
    {
      var button = event.relatedTarget;
      const saveCompetitorUrl = button.getAttribute('data-vms-save-competitor-url');

      var competitorName = button.getAttribute("data-bs-name");
      var competitorDescription = button.getAttribute("data-bs-description");
      var nameInput = editCompetitorDetails.querySelector(".vms-edit-competitor-name");
      var descriptionTextArea = editCompetitorDetails.querySelector('.vms-edit-competitor-desc');
      var competitorImage = button.getAttribute("data-vms-image");
      var imgCompetitor = editCompetitorDetails.querySelector('.vms-edit-competitor-image');
      
      editCompetitorDetails.querySelector('.vms-img-filename').value = button.getAttribute('data-vms-image-name');

      nameInput.value = competitorName;
      descriptionTextArea.value = competitorDescription;
      imgSelect.style.display = 'none';
      imgCompetitor.src = competitorImage;

      nameInput.classList.remove('is-invalid');
      document.querySelector('.vms-edit-name-feedback').textContent = '';
      document.querySelector('.vms-img-select').value = '';

      editCompetitorDetails.querySelector('.save-button').setAttribute('data-vms-save-competitor-url', saveCompetitorUrl);
    })

    imgSelect.addEventListener("change", updateImageDisplay);
    editCompetitorDetails.querySelector('.edit-image-overlay').addEventListener('click', event => {
      imgSelect.click();
    })

    editCompetitorDetails.querySelector('.save-button').addEventListener('click', event => {
      const button = event.target;
      const saveCompetitorUrl = button.getAttribute('data-vms-save-competitor-url');

      const competitorNameElement = document.querySelector('.vms-edit-competitor-name');
      const competitorName = competitorNameElement.value;
      const competitorDescription = document.querySelector('.vms-edit-competitor-desc').value;
      const competitorImage = document.querySelector('.vms-img-select').files[0];
      const competitorImageName = document.querySelector('.vms-img-filename').value;
      const event_id = document.querySelector('.vms-event-id').value;

      competitorNameElement.classList.remove('is-invalid');

      const formData = new FormData();
      formData.append('competitor_name', competitorName);
      formData.append('competitor_description', competitorDescription);
      formData.append('competitor_image', competitorImage);
      formData.append('event_id', event_id);
      formData.append('competitor_image_name', competitorImageName);

      fetch(saveCompetitorUrl, { method: "PUT", body: formData })
        .then((response) => {
          if (response.status == 400) {
            response.text().then(data => {
              if (data != '') {
                competitorNameElement.classList.add('is-invalid');
                document.querySelector('.vms-edit-name-feedback').textContent = data;
              }
            })
          }
          else {
            document.querySelector('.vms-img-select').value = '';
            location.reload();
          }
        })
    });
  }



  confirmDialog = document.getElementById('confirm-dialog');
  if (confirmDialog) {
    confirmDialog.addEventListener('show.bs.modal', event => {
      // Button that triggered the modal
      const button = event.relatedTarget;
      // Extract info from data-vms-* attributes
      const deleteCompetitorUrl = button.getAttribute('data-vms-delete-competitor-url');
      const competitorName = button.getAttribute('data-vms-competitor-name');

      // Update the modal's content.
      const modalBody = confirmDialog.querySelector('.modal-body');
      modalBody.textContent = competitorName;

      confirmDialog.querySelector('.delete-button').setAttribute('data-vms-delete-competitor-url', deleteCompetitorUrl);
    });

    confirmDialog.querySelector('.delete-button').addEventListener('click', event => {
      const button = event.target;
      const deleteCompetitorUrl = button.getAttribute('data-vms-delete-competitor-url');

      // Delete competitor
      const request = new Request(deleteCompetitorUrl, { method: "DELETE" });
      fetch(request).then((response) => { location.reload() });
    });
  }



  function updateImageDisplay() {
    const preview = document.querySelector(".vms-edit-competitor-image");
    var imgSelect = editCompetitorDetails.querySelector('.vms-img-select');
    var filenameHolder = editCompetitorDetails.querySelector('.vms-img-filename');

    const curFiles = imgSelect.files;
    if (curFiles.length === 0) {
      // Unsure it's possible for it to be 0
    } else {
      for (const file of curFiles) {
        if (validFileType(file)) {
          preview.src = URL.createObjectURL(file);
          preview.alt = preview.title = file.name;
          filenameHolder.value = file.name;
        } else {
          // This isn't important enough to fix
        }
      }
    }
  }

  // https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types
  const fileTypes = [
    "image/apng",
    "image/bmp",
    "image/gif",
    "image/jpeg",
    "image/pjpeg",
    "image/png",
    "image/svg+xml",
    "image/tiff",
    "image/webp",
    "image/x-icon",
  ];

  function validFileType(file) {
    return fileTypes.includes(file.type);
  }
  
  document.querySelectorAll('.redirect-home').forEach((button) => {button.addEventListener('click', (event) => {
      window.location.href = '/login';
    });
  });

  const voteModal = document.getElementById('confirmModal');
  if (voteModal) {
    voteModal.addEventListener('show.bs.modal', event => {
      const button = event.relatedTarget;
      const competitorId = button.getAttribute('data-vms-competitor-id');
      const logged_in_role = button.getAttribute('data-vms-logged-in-role');

      voteModal.querySelector('#confirmVote').setAttribute('data-vms-competitor-id', competitorId);
    });

    // add button click event
    voteModal.querySelector('#confirmVote').addEventListener('click', event => {
      const button = event.target;
      document.querySelector('#voting-for').value = button.getAttribute('data-vms-competitor-id');
      document.getElementById('voteForm').submit();
    });
  }

  function setButtonActive(name, active) {
    // Displays the named button as active (btn-primary) or inactive (btn-secondary)
    const buttonClass = document.querySelector(name).classList;
    if (active) {  
      buttonClass.add('btn-primary');
      buttonClass.remove('btn-secondary');
    }
    else {  
      buttonClass.remove('btn-primary');
      buttonClass.add('btn-secondary');
    }
  }

  const btnSortDate = document.querySelector('.vms-btn-sort-date');
  if (btnSortDate) {
    btnSortDate.addEventListener('click', (event) => {
      setButtonActive('.vms-btn-sort-votes', false);
      setButtonActive('.vms-btn-sort-date', true);
      // Hide the sorted by votes table
      document.querySelector('.vms-sort-by-votes').classList.add('d-none');
      // Show the sorted by date table
      document.querySelector('.vms-sort-by-date').classList.remove('d-none');
    });

    document.querySelector('.vms-btn-sort-votes').addEventListener('click', (event) => {
      setButtonActive('.vms-btn-sort-date', false);
      setButtonActive('.vms-btn-sort-votes', true);
      // Hide the sorted by date table
      document.querySelector('.vms-sort-by-date').classList.add('d-none');
      // Show the sorted by votes table
      document.querySelector('.vms-sort-by-votes').classList.remove('d-none');
    });
  }
})()





