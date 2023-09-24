function deleteContent(contentID){
    fetch("/delete-content", {
        method: "POST",
        body: JSON.stringify({contentID: contentID})
    }) .then((_res) => {
        window.location.href = "/media";
    });
}

function confirmDelete(contentId) {
    if (confirm("Are you sure you want to delete this content?")) {
        // If the user confirms, call your deleteContent function
        deleteContent(contentId);
    } else {
        // If the user cancels, do nothing or provide feedback
    }
}
