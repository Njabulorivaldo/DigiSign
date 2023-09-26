document.addEventListener("DOMContentLoaded", function() {
    populateCompositions();
});

function populateCompositions() {
    const tableBody = document.querySelector("tbody");
    const compositions = JSON.parse(localStorage.getItem("compositions") || "[]");

    compositions.forEach(composition => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${composition.name}</td>
            <td>${composition.dateAdded}</td>
            <td>${composition.duration}</td>
            <td>Actions</td>  <!-- Placeholder for actions, you can replace this -->
        `;

        tableBody.appendChild(row);
    });
}