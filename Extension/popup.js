//This script is used to fetch URL results from content.js and display it in popup.html as UI
console.log("Running popup.js");

//red, yellow, green
const colors = ["#FF0000", "#FFD600", "#05EE00"];
var url;
var prediction;
var feature_values;

//fetch from chrome.storage.local to render data in popup.html
chrome.storage.local.get("results", ({ results }) => {
  url = results.url;
  prediction = results.prediction[0];
  feature_values = results.features;

  //### Debug ###
  // console.log("URL: ", url);
  // console.log("Prediction: ", prediction);
  // console.log("Features: ", feature_values);

  //Display URL
  document.getElementById("url").innerHTML = url;
  let feature_names = [];

  //fetch and store tag elements into a list
  for (var i = 0; i < document.getElementsByClassName("tag").length; i++) {
    feature_names.push(
      document.getElementsByClassName("tag")[i].getAttribute("id")
    );
  }

  //check conditions for color
  var i = 0;
  while (i < feature_names.length) {
    switch (feature_values[i]) {
      case 1:
        console.log("Phishing: "+colors[0])
        document.getElementById(feature_names[i]).style.backgroundColor = colors[0];
        break;
      case 0:
        console.log("Suspicious: "+colors[1])
        document.getElementById(feature_names[i]).style.backgroundColor = colors[1];
        break;
      case -1:
        console.log("Legit: "+colors[2])
        document.getElementById(feature_names[i]).style.backgroundColor = colors[2];
        break;
      default:
        break;
    }
    i++;
  }
});
