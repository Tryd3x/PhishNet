//This script is used to fetch URL results from content.js and display it in popup.html as UI
console.log("Running popup.js");

//red, yellow, green
const colors = ["FF0000", "FFD600", "05EE00"];
var feature_values;

//data isnt storing, need fix

//fetch from chrome.storage.local to render data in popup.html
chrome.storage.local.get("results", ({ results }) => {
  console.log("Value key1 from storage: ", results.url);
  console.log("Value key2 from storage: ", results.prediction);
  console.log("Value key3 from storage: ", results.msg);
});
