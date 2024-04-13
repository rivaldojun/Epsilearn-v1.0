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
        const accepteButtons = document.querySelectorAll('.confirm-btn');
    accepteButtons.forEach((button) => {
      button.addEventListener('click', function() {
        // Get the demand ID from the data attribute
        const demandId = this.dataset.demandId;
        const liveId = this.dataset.liveId;
        // Send a DELETE request to the Flask route to delete the demand
    if(this.textContent.trim()==="Reporter"){
      window.location.href = `/report/${demandId}`;
    }
    else{
      window.location.href=`room/${liveId}`
    }
        
        
      });
    });

    const panelContainers = document.querySelectorAll('.pan');
  
  panelContainers.forEach(function(panelContainer) {
    const demandId = panelContainer.dataset.demandId;
    
    panelContainer.addEventListener('click', function() {
      window.location.href = `/details_dmd/${demandId}`;
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
    const secondsElement = countdownTimer.querySelector("#seconds");

    setInterval(() => {
      const now = new Date().getTime();
      const difference = t1 - now;

      const days = Math.floor(difference / (1000 * 60 * 60 * 24));
      const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((difference % (1000 * 60)) / 1000);

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

