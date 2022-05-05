console.log("Running...");

let prediction;

async function fetchData(url_address) {
  try {
    //https://phish-model.herokuapp.com/
    //http://127.0.0.1:5000/
    const res = await fetch("https://phish-model.herokuapp.com/predict", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: url_address }),
    });

    const data = await res.json();
    console.log("Prediction: "+data[0])
    prediction = data[0]

    //launch alerts to user
    if (prediction == 1) alert("Phishing Detected!! This website may be harmful");
  } catch (err) {
    console.log(err.message);
  }
}


function parseData() {
}

var url = window.location.href;
console.log(url);
fetchData(url);
parseData();

