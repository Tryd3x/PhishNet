console.log("Running...");

async function getData(url_address) {
  try {
    const res = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url: url_address }),
    });

    const data = await res.json();
    console.log(data[0])
    let prediction = data[0]

    //launch alerts to user
    if (prediction == 1) alert("Phishing Detected!! This website may be harmful");
  } catch (err) {
    console.log(err.message);
  }
}

var url = window.location.href;
console.log(url);
getData(url);
