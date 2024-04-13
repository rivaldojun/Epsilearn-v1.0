    // Add an event listener to the delete buttons
    const deleteButtons = document.querySelectorAll('.cancel-btn');
    const confButtons = document.querySelectorAll('.confirm-btn');
    deleteButtons.forEach((button) => {
      button.addEventListener('click', function() {
        // Get the demand ID from the data attribute
        const demandId = this.dataset.demandId;
        // Send a DELETE request to the Flask route to delete the demand
    if(this.textContent.trim()==="Annuler"){

      $("#confirmationModal").modal("show");
      const cancelButton = document.getElementById("cancelReload");
      // Ajoutez un gestionnaire d'événements pour le clic sur le bouton "Annuler"
      cancelButton.addEventListener("click", function () {
        // Rechargez la page actuelle
        window.location.reload();
      
      });
      document.getElementById("confirmCancellation").addEventListener("click", function () {
        const enteredCode = document.getElementById("confirmationCode").value;
    
        // Remplacez "codeGeneréAléatoirement" par le code généré réel
        const generatedCode =demandId ;
    
        if (enteredCode === generatedCode) {
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
        } else {
          // Affichez un message d'erreur si le code est incorrect
          alert("Code incorrect. Veuillez réessayer.");
        }
    
        // Fermez le modal
        $("#confirmationModal").modal("hide");
      });
     
    }
    else{
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
    }
      });
    
    });

    confButtons.forEach((button) => {
      button.addEventListener('click', function() {
        // Get the demand ID from the data attribute
        const demandId = this.dataset.demandId;
        const liveId = this.dataset.liveId;
        // Send a DELETE request to the Flask route to delete the demand
    if(this.textContent.trim()==="Payer"){
        window.location.href=`/checkoutdemande/${demandId}`
    }
    else if(this.textContent.trim()==="Commencer")
    {window.location.href=`room/${liveId}`}
    else{
        fetch(`/accepte_report/${demandId}`, {
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
    }
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
  function updateCountdown() {
  const countdownPanels = document.querySelectorAll(".countdown-panel");

  countdownPanels.forEach(countdownPanel => {
    const dt = countdownPanel.dataset.demandId;
    const t1 = new Date(`${dt}`).getTime();

    const countdownTimer = countdownPanel.querySelector("#countdown-timer");
    const daysElement = countdownTimer.querySelector("#days");
    const hoursElement = countdownTimer.querySelector("#hours");
    const minutesElement = countdownTimer.querySelector("#minutes");


    setInterval(() => {
      const now = new Date().getTime();
      const difference = t1 - now;

      const days = Math.floor(difference / (1000 * 60 * 60 * 24));
      const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));


      daysElement.innerText = formatTime(days);
      hoursElement.innerText = formatTime(hours);
      minutesElement.innerText = formatTime(minutes);
    }, 1000);
  });
}

function formatTime(time) {
  return time < 10 ? `0${time}` : time;
}

updateCountdown();

