function deleteNote(noteid) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteid: noteid }),
  }).then((res) => {
    window.location.href = "/";
  });
}
