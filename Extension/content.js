console.log("Running scan.js");

async function fetchData(url_address) {
  try {
    //https://phish-model.herokuapp.com/predict
    //http://127.0.0.1:5000/predict
    const res = await fetch("https://phish-model.herokuapp.com/predict", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: url_address }),
    });

    const data = await res.json();
    console.log("Prediction: " + data[0]);
    console.log("Features: " + data[1]);
    prediction = data[0];
    features = data[1];

    var results = {
      url: url_address,
      prediction: prediction,
      features: features,
    };

    //store results into local storage and pass it to popup.js for UI features
    //{results} ~ {results:{url: url_address, prediction: prediction, msg: "hello" }}
    chrome.storage.local.set({ results }, () => {
      console.log(`Stored url: ${url_address}`);
      console.log(`Stored prediction: ${prediction}`);
      console.log(`Stored features: ${features}`);
    });

    //launch alerts to user
    if (prediction == 1)
      alert("Phishing Detected!! This website may be harmful");
  } catch (err) {
    console.log(err.message);
  }
}

var url = window.location.href;
console.log(url);
fetchData(url);
