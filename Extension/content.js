console.log("Running...");

let container = [];
async function getData() {
  const res = await fetch("https://jsonplaceholder.typicode.com/users");
  const data = await res.json();
  data.forEach((item) => {
    container.push(item);
  });
  printData();
}

function printData() {
  container.forEach((item) => {
    console.log(`${item.id} : ${item.name}\n`);
  });
}

getData();