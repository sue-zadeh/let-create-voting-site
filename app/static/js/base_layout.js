
(() => {

    const competitionOptions = document.querySelectorAll('.vms-competition-select-option');
    const competitionChangeUrl = document.querySelector('.vms-competition-change');
    var afterChangeUrl = null;
    if (competitionChangeUrl) {
        afterChangeUrl = competitionChangeUrl.getAttribute('data-vms-url');
    }
    competitionOptions.forEach((option) => {
        option.addEventListener('click', (event) => {
            bodyData = JSON.stringify({competition_id: event.target.getAttribute('data-vms-competition-id') });

            fetch('/change_competition', { method: 'PUT', headers: {"Content-Type": "application/json"}, body: bodyData })
            .then(() => {
                if (afterChangeUrl) {
                    location.href = afterChangeUrl;
                }
                else {
                    location.reload()
                }
            })
        })
    })

    const currentUserId = document.getElementById("current_user_id").value;
    if (currentUserId != null) {
    setInterval(() => {
        fetch('/check_new_messages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: currentUserId })
        })
        .then(response => response.json())
        .then(data => {
            const newMessageCount = data.new_message_count;
            const indicator = document.getElementById('new-message-indicator');

            // Update message indicator
            if (newMessageCount > 0) {
                indicator.style.display = 'inline';
                indicator.textContent = parseInt(indicator.textContent) + newMessageCount;
            }

            // Add new messages to the message box
            data.new_messages.forEach(message => {
                const li = document.createElement('li');
                li.classList.add('text-start');
                li.innerHTML = `
                    ${message['message']}
                    <small style="font-size: 0.85em; float: right;">${new Date().toLocaleString()}</small>
                `;
                
                const messageBody = document.getElementById('message_body' + message['from_user']);
                if (messageBody) {
                    messageBody.appendChild(li);
                }

                // Highlight the corresponding accordion button
                const userAccordionButton = document.querySelector(`button[data-bs-target="#collapse-${message['from_user']}"]`);
                if (userAccordionButton) {
                    userAccordionButton.classList.add('new-message-highlight');

                    // Add click event listener to remove highlight
                    userAccordionButton.onclick = () => {
                        userAccordionButton.classList.remove('new-message-highlight');
                    };
                }
            });
        })
        .catch(error => console.error('Error fetching new messages:', error));
    }, 5000); // Check every 5 seconds 
    
    }
})();