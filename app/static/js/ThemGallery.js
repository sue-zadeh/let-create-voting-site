// // ThemeGallery.jsx

// // Display the available themes with a preview image and "Choose Theme" button.
// // On clicking "Choose Theme", call the backend to save the theme selection.
// // Include a "Preview" button that temporarily applies the theme to the page before saving.

// document.addEventListener('DOMContentLoaded', function() {
//     const setThemeBtns = document.querySelectorAll('.setThemeBtn');
//     const deleteThemeBtns = document.querySelectorAll('.deleteThemeBtn');
  
//     setThemeBtns.forEach(btn => {
//       btn.addEventListener('click', function() {
//         const themeId = this.getAttribute('data-theme-id');
//         if (confirm('Do you want to set this theme for your competition pages?')) {
//           fetch(`/admin/set_theme/${themeId}`, {
//             method: 'POST'
//           })
//           .then(response => response.json())
//           .then(data => {
//             alert(data.message);
//             window.location.reload();
//           });
//         }
//       });
//     });
  
//     deleteThemeBtns.forEach(btn => {
//       btn.addEventListener('click', function() {
//         const themeId = this.getAttribute('data-theme-id');
//         if (confirm('Are you sure you want to delete this theme?')) {
//           fetch(`/admin/delete_theme/${themeId}`, {
//             method: 'POST'
//           })
//           .then(response => response.json())
//           .then(data => {
//             alert(data.message);
//             window.location.reload();
//           });
//         }
//       });
//     });
//   });
  