import Chart from 'chart.js/auto';
import colorLib from '@kurkle/color';
import "./charts/chartsjs-utils";

let backendServer = "6561f2fcdcd355c083245fee.mockapi.io";

//startData
let totalSecrets = "836"
let activeSecrets = "8"
let actionedSecrets = "828"

// Verticle Bar Chart Data
const verticleBarChartData = {
    labels: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November","December"],
    datasets: [
      {
        label: "Number of secrets",
        backgroundColor: window.chartColors.red,
        data: [
          42,
          108,
          93,
          85,
          78,
          99,
          80,
          73,
          62,
          48,
          35,
        ],
      }
    ],
  };

let main = () => {
    console.log("in main");
    configureInitialData();
};

let configureInitialData = () => {
    console.log("Setting data in KPI's");    
    calcKPIs(totalSecrets,activeSecrets,actionedSecrets);
    console.log("Getting initial data from backend");
    fetch("https://" + backendServer + "/secrets")
        .then(response => response.json())
        .then(data => writeInitialData(data));
}

let writeInitialData = (secretsJson) => {
    secretsJson.forEach(secretElement => {
        let secretSnippet = calcSecretDetailSnippet(secretElement)
        addSecretDetail(secretSnippet);
    });
}

let calcKPIs = (totalSecrets,activeSecrets,actionedSecrets) => {
    let sectionTotalSecrets = document.getElementById("totalSecrets")
    let codeTotal = `
        <div class="widget-numbers text-white"><span>${totalSecrets}</span></div>
        `
    sectionTotalSecrets.insertAdjacentHTML("beforeEnd", codeTotal);

    let sectionActiveSecrets = document.getElementById("activeSecrets")
    let codeActive = `
        <div class="widget-numbers text-white"><span>${activeSecrets}</span></div>
        `
    sectionActiveSecrets.insertAdjacentHTML("beforeEnd", codeActive);

    let sectionActionedSecrets = document.getElementById("actionedSecrets")
    let codeActioned = `
        <div class="widget-numbers text-white"><span>${actionedSecrets}</span></div>
        `
    sectionActionedSecrets.insertAdjacentHTML("beforeEnd", codeActioned);
};

let calcSecretDetailSnippet = (secretElement) => {
    let color = ''
    switch (secretElement.confidence) {
    case 'VERY_UNLIKELY':
        color = 'success'
        break;
    case 'UNLIKELY':
        color = 'success'
        break;
    case 'POSSIBLE':
        color = 'warning'
        break;
    case 'LIKELY':
        color = 'danger'
        break;
    case 'VERY_LIKELY':
        color = 'danger'
    break;
    default:
        console.log(`confidence type ${secretElement.confidence} not recognized`);
    }

    let secretDetails = `
    <tr>
    <td class="text-center text-muted">${secretElement.id}</td>
    <td class="text-center">Teams</td>
    <td class="text-center">${secretElement.detector.provider}</td>
    <td class="text-center">${secretElement.detector.name}</td>
    <td class="text-center">${secretElement.value}</td>
    <td class="text-center">
        <div class="badge bg-${color}">${secretElement.confidence}</div>
    </td>
    </tr>
    `
    return secretDetails
}

let addSecretDetail = (secretSnippet) => {
    let sectionDetailedSecrets = document.getElementById("secretDetailsBody")
    sectionDetailedSecrets.insertAdjacentHTML("beforeEnd", secretSnippet);
};

  // Verticle Bar Chart
  setTimeout(function () {
    if (document.getElementById("chart-vert-bar")) {
      const ctx = document.getElementById("chart-vert-bar").getContext("2d");
      window.myVerticleBar = new Chart(ctx, {
        type: "bar",
        data: verticleBarChartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: false,
              text: "Chart.js Verticle Bar Chart",
            },
          },
        },
      });
    }
  }, 500);

const backendSocket = new WebSocket("wss://" + backendServer);

//   backendSocket.onmessage = (event) => {
//     console.log(event.data);
//     let secretDetail = calcSecretDetailSnippet(event.data)
//     addSecretDetail(secretDetail)
//   };

main();