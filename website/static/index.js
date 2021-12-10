function deleteHistory(historyId) {
  fetch("/delete-history", {
    method: "POST",
    body: JSON.stringify({ historyId: historyId }),
  }).then((_res) => {
    window.location.href = "/history";
  });
}
