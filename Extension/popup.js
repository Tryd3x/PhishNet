console.log("Running popup.js");

chrome.storage.sync.get("prediction", ({ prediction }) => {
  console.log("Storage data: ", prediction);
});
