document.addEventListener("DOMContentLoaded", function() {
    populateMedia();
});
let ids = []

function populateMedia() {
    const mediaTable = document.getElementById("mediaTable").querySelector("tbody");
    //console.log(user)
    //const demoMedia = fetch"http://localhost:5000/getContent"
    let demoMedia=[];
    fetch("/getContent")
            .then(response => response.json())
            .then(data => {
                ids = []
                console.log(data);
                p(data);
            })
            .catch(error => {
                console.error("+++++++", error)
            });
            
}

function p(demoMedia){
    console.log(demoMedia)
    demoMedia.forEach(media => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${media.name}</td>
            <td>${media.file_type}</td>
        `;

        row.addEventListener("click", function() {
            addToSelected(media);
        });

        mediaTable.appendChild(row);
    });
}

function addToSelected(media) {
    
    const selectedMediaList = document.getElementById("selectedMediaList");
    const listItem = document.createElement("li");
    listItem.className = "list-group-item";
    listItem.innerText = media.name;
    ids.push(media.id)
    selectedMediaList.appendChild(listItem);
}

function navigateBack() {
    window.location.href = "/render";
}

function saveComp( name, descr, contentids){
    // const name = document.getElementById('name').value;
    // const location = document.getElementById('location').value;
    // const status = document.getElementById('status').value;
    const data = {name: name, description:descr, content_ids:contentids}
    fetch("/saveComposition", {
        method: "POST",
        body: JSON.stringify(data)
    }) .then((_res) => {
        window.location.href = "/render";
    });
}
  
const comp = document.getElementById("comDetails");
const modal = document.getElementById("compModal");
comp.addEventListener("click", function() {
    modal.style.display = "block";
});

const detailsForm = document.getElementById('compDetails');
    detailsForm.addEventListener('submit', function(event) {
      event.preventDefault();
      
      const name = document.getElementById('na').value;
      const dec = document.getElementById('description').value;
      //const selectedMediaList = document.getElementById("selectedMediaList").children;


      console.log(ids)
      saveComp(name,dec,ids)
      // Close the modal
      modal.style.display = 'none';
    });


function saveComposition() {

    modal.style.display ="block";
    const selectedMediaList = document.getElementById("selectedMediaList").children;
    let compositionName = '';
    
    for (let item of selectedMediaList) {
        compositionName += `${item.innerText}, `;
    }
    
    compositionName = compositionName.substring(0, compositionName.length - 2);  // To remove the trailing comma and space

    const composition = {
        name: compositionName,
        dateAdded: new Date().toLocaleDateString(),
        duration: "3:15"  // Placeholder, you can replace this
    };

    let compositions = localStorage.getItem("compositions");
    
    if (compositions) {
        compositions = JSON.parse(compositions);
    } else {
        compositions = [];
    }

    compositions.push(composition);
    localStorage.setItem("compositions", JSON.stringify(compositions));
    
    //navigateBack();
}