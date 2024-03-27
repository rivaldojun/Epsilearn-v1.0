function afficherConfirmation() {
    var modal = document.getElementById('modals');
    modal.style.display = 'block';
     // Événement popstate pour détecter les changements dans l'historique
    
  }
  
  function cacherConfirmation() {
    var modal = document.getElementById('modals');
    modal.style.display = 'none';
     // Événement popstate pour détecter les changements dans l'historique
    
  }

// Add an event listener to the delete buttons
const deleteButtons = document.querySelectorAll('.cancel-btn');
deleteButtons.forEach((button) => {
  button.addEventListener('click', function() {
    // Get the demand ID from the data attribute
    const demandId = this.dataset.demandId;
    // Send a DELETE request to the Flask route to delete the demand
    fetch(`/refuse_demande/${demandId}`, {
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

// Add an event listener to the delete buttons
// const accepteButtons = document.querySelectorAll('.confirm-btn');
// accepteButtons.forEach((button) => {
//   button.addEventListener('click', function() {
//   afficherConfirmation()
//   });
// });
const panelContainers = document.querySelectorAll('.pan');

panelContainers.forEach(function(panelContainer) {
const demandId = panelContainer.dataset.demandId;


panelContainer.addEventListener('click', function() {
  window.location.href = `/details_dmd/${demandId}`;
});
});


const dat1 = document.querySelectorAll('.dat1');
dat1.forEach((button) => {
  button.addEventListener('click', function() {
    // Get the demand ID from the data attribute
    const demandId = this.dataset.demandId;
    const dateId = this.dataset.dateId;
    const cd=`${uuidv4()}`
    // Send a DELETE request to the Flask route to delete the demand
    fetch(`/accepte_demande/date1/${demandId}/${cd}`, {
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

const dat2 = document.querySelectorAll('.dat2');
dat2.forEach((button) => {
  button.addEventListener('click', function() {
    // Get the demand ID from the data attribute
    const demandId = this.dataset.demandId;
    const dateId = this.dataset.dateId;
    const cd=`${uuidv4()}`
    // Send a DELETE request to the Flask route to delete the demand
    fetch(`/accepte_demande/date2/${demandId}/${cd}`, {
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

function uuidv4() {
return 'xxyxyxxyx'.replace(/[xy]/g, function (c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
});
}
function date1(demandId) {
const deleteButtons = document.querySelectorAll('.cancel-btn');
// const demandId = deleteButtons.dataset.demandId;

// Replace the current URL in the browser's history with '/connexion'
history.replaceState({}, '', '/');
// Redirect to the 'connexion' page
window.location.href = `/accepte_demande/${demandId}/1/${cd}`;

}

function date2(demandId) {
const date2Id =2;
window.location.href = `/accepte_demande/${demandId}/2`;

}

