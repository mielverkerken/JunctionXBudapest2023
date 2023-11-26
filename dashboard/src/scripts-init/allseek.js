import Chart from 'chart.js/auto';
import colorLib from '@kurkle/color';
import "./charts/chartsjs-utils";

let backendServer = "orchestrator-xzpcu7nwvq-ew.a.run.app";


//startData
let totalSecrets = "836"
let activeSecrets = "8"
let actionedSecrets = "828"
let totalSources = "2"
let source_by_id = {}
let secret_by_id = {}

const confidenceColors = {
  'VERY_UNLIKELY': 'success',
  'UNLIKELY': 'success',
  'POSSIBLE': 'warning',
  'LIKELY': 'danger',
  'VERY_LIKELY': 'danger'
};

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

let main = async () => {
    console.log("in main");
    // configureInitialData();
    let secret_list, source_list;
    [secret_list, source_list] = await fetchData();
    secret_by_id = secret_list.reduce((map, obj) => (map[obj.id] = obj, map), {});
    source_by_id = source_list.reduce((map, obj) => (map[obj.id] = obj, map), {});
    console.log(secret_by_id)
    console.log(source_by_id)
    updateUI(secret_list, source_list);

    const webSocketSecrets = new WebSocket("wss://" + backendServer + "/ws/SECRETS");
    webSocketSecrets.onmessage = wsSecretUpdate;
    const webSocketSources = new WebSocket("wss://" + backendServer + "/ws/SOURCES");
    webSocketSources.onmessage = wsSourceUpdate;
    console.log("websocket connected")
};

let fetchData = async () => {
  let secret_response = await fetch("https://" + backendServer + "/secrets");
  let sources_response = await fetch("https://" + backendServer + "/sources");
  let secret_data = await secret_response.json();
  let sources_data = await sources_response.json();
  return [secret_data, sources_data]
}

let updateUI = (secret_list, source_list) => {
  console.log("Updating UI");
  totalSecrets = secret_list.length;
  activeSecrets = Math.round(totalSecrets /3*2);
  totalSources = source_list.length;
  updateKPIs(totalSecrets, activeSecrets, totalSources);
  updateSecretTable(secret_list, source_list);
}

let updateSecretTable = (secret_list, source_list) => {
  let secretTable = document.getElementById("secretDetailsBody")
  secret_list
    .map(secret => { // join with source
      secret.source = source_by_id[secret.source_id];
      return secret;
    })
    .map(joinedSecret => mapSecretToRow(joinedSecret))
    .forEach(row => secretTable.insertAdjacentHTML("beforeEnd", row));
}

let mapSecretToRow = (secretElement) => {
  return `
    <tr>
    <td class="text-center text-muted">${secretElement.id.substring(0, 6)}</td>
    <td class="text-center">${secretElement.value}</td>
    <td class="text-center">${secretElement.source.type}</td>
    <td class="text-center">${secretElement.detector.provider}</td>
    <td class="text-center">${secretElement.detector.name}</td>
    <td class="text-center">
        <div class="badge bg-${confidenceColors[secretElement.confidence]}">${secretElement.confidence}</div>
    </td>
    </tr>
    `
}

let updateKPIs = (totalSecrets, activeSecrets, actionedSecrets) => {
  let to_update = ["totalSecrets", "activeSecrets", "actionedSecrets"]
  let values = [totalSecrets, activeSecrets, actionedSecrets]
  for (let i = 0; i < to_update.length; i++) {
    let section = document.getElementById(to_update[i])
    section.innerHTML = `
      <div class="widget-numbers text-white"><span>${values[i]}</span></div>
    `
  }
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

  let wsSecretUpdate = async (event) => {
    console.log("ws Secret update");
    let newSecret = JSON.parse(event.data); 
    secret_by_id[newSecret["id"]] = newSecret;
    updateSecretTable([newSecret], []);
    updateKPIs(
      Object.keys(secret_by_id).length, 
      Math.round(Object.keys(secret_by_id).length/3*2),
      Object.keys(source_by_id).length
      );
  }
  
  let wsSourceUpdate = async (event) => { 
    console.log("ws Source update")
    let newSource = JSON.parse(event.data); 
    console.log(newSource);
    source_by_id[newSource["id"]] = newSource;
    updateKPIs(
      Object.keys(secret_by_id).length, 
      Math.round(Object.keys(secret_by_id).length/3*2),
      Object.keys(source_by_id).length
      );
  }  

main();