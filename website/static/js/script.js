
function deleteContent(contentID){
    fetch("/delete-content", {
        method: "POST",
        body: JSON.stringify({contentID: contentID})
    }) .then((_res) => {
        window.location.href = "/media";
    });
}

function confirmDelete(screenID) {
    if (confirm("Are you sure you want to delete this content?")) {
        // If the user confirms, call your deleteContent function
        deleteContent(screenID)
    } else {
        // If the user cancels, do nothing or provide feedback
    }   
}

function deleteScreen(screenID){
    if (confirm("Are you sure you want to remove this screen?")) {
        // If the user confirms, call your deleteContent function
        fetch("/delete-screen", {
            method: "POST",
            body: JSON.stringify({screenID:screenID})
        }) .then((_res) => {
            window.location.href = "/screens";
        });
    } else {
        // If the user cancels, do nothing or provide feedback
    }

}

// function confirmDelete(contentId) {

// }

// Get the modal and buttons
const openFormButton = document.getElementById("openFormButton");
const closeFormButton = document.getElementById("closeFormButton");
const popupForm = document.getElementById("popupForm");
const nextButton = document.getElementById("nextButton");

// Show the popup form when the open button is clicked
openFormButton.addEventListener("click", function() {
    popupForm.style.display = "block";
});

// Close the popup form when the close button is clicked
closeFormButton.addEventListener("click", function() {
    popupForm.style.display = "none";
});

// Close the popup form when clicking outside the form
window.addEventListener("click", function(event) {
    if (event.target === popupForm) {
        popupForm.style.display = "none";
    }
});

// Handle the "Next" button click (you can add your logic here)
nextButton.addEventListener("click", function() {
    // Add your logic for handling the "Next" button click here
    // For example, you can access the input field value like this:
    const inputValue = document.getElementById("code").value;



    // Close the popup form (you can modify this behavior)
    popupForm.style.display = "none";
});

/**
     * Handle the submission of screen code.
     * @param {Object} e - The event object.
*/

// Add an event listener to the form for form submission
document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Handle the code submission
    const screenCode = document.getElementById('screenCode').value;
    handleCodeSubmit(screenCode);
});
document.getElementById('compDetails').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Handle the code submission
    const screenCode = document.getElementById('na').value;
    console.log(screenCode)
});
async function handleCodeSubmit(screenCode) {
    try {
        const url = '/verify_code'; // Assuming the endpoint is on the same domain
        const data = { code: screenCode };

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const responseData = await response.json();
            if (responseData.status === 'success') {
                // Code is valid, perform actions here
                openModal(screenCode);
                //window.alert('Advancing');
            }
        } else {
            // Handle non-2xx status codes (e.g., 404, 500, etc.)
            window.alert('Error verifying the code. Status: ' + response.status);
        }
    } catch (error) {
        console.error('Error verifying the code:', error);
        window.alert('Error verifying the code: ' + error.message);
    }
}



//Addition of a new Screen details
// Function to show the modal
function openModal(screenCode) {
    const modal = document.getElementById('myModal');
    modal.style.display = 'block';
  
    // When the user clicks on the close button, close the modal
    const closeModalBtn = document.getElementById('closeModal');
    closeModalBtn.addEventListener('click', function() {
      modal.style.display = 'none';
    });
  
    // When the user submits the form, you can access the input values
    const detailsForm = document.getElementById('screenDetails');
    detailsForm.addEventListener('submit', function(event) {
      event.preventDefault();
      
      const name = document.getElementById('name').value;
      const location = document.getElementById('location').value;
      const status = document.getElementById('status').value;
        
      // Do something with the submitted data, e.g., send it to the server or process it

      addScreen(screenCode, name, location, status);
  
      // Close the modal
      modal.style.display = 'none';
    });
  }

//Add Screen to Database
  function addScreen(screenCode, name, location, status){
    // const name = document.getElementById('name').value;
    // const location = document.getElementById('location').value;
    // const status = document.getElementById('status').value;
    const data = {code: screenCode, name: name, location:location, status:status }
    fetch("/add-screen", {
        method: "POST",
        body: JSON.stringify(data)
    }) .then((_res) => {
        window.location.href = "/screens";
    });
}
  



