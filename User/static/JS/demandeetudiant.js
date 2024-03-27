// Add an event listener to the delete buttons
const deleteButtons = document.querySelectorAll('.cancel-btn');
deleteButtons.forEach((button) => {
  button.addEventListener('click', function() {
    // Get the demand ID from the data attribute
    const demandId = this.dataset.demandId;

    // Send a DELETE request to the Flask route to delete the demand
    fetch(`/delete_demande/${demandId}`, {
      method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
      // Reload the page after successful deletion
      if (data.success) {
        window.location.reload();
      }
    })
    .catch(error => {
      console.error('Error deleting demand:', error);
    });
  });
});
document.addEventListener('DOMContentLoaded', function() {
const panelContainers = document.querySelectorAll('.pan');

panelContainers.forEach(function(panelContainer) {
const demandId = panelContainer.dataset.demandId;

panelContainer.addEventListener('click', function() {
  window.location.href = `/details_dmd/${demandId}`;
});
});
});