// static/script.js
async function loadCurrentMetrics() {
    const res = await fetch('/current_status_raw');
    const data = await res.json();

    const container = document.getElementById('current_data_container');
    container.innerHTML="" // Clear "Loading..., replace with table element"

    const table = document.createElement("table");
    table.setAttribute('id', 'status_table')
    container.appendChild(table);

    const head = document.createElement("tr")
    head.innerHTML = `
        <th>Job Name</th>
        <th>Status</th>
        <th>Detail</th>`;
    table.appendChild(head)

    for (const item of data) {
        const { instance, job } = item.metric;
        const status = item.value[1] === "1" ? "✅ UP" : "❌ DOWN";

        const entry = document.createElement('tr');

        const jobEntry = document.createElement("td")
        jobEntry.textContent = `${job}`

        const statusEntry = document.createElement("td")
        statusEntry.textContent = `${status}`

        const detailEntry = document.createElement("td")
        detailEntry.textContent = `${instance}`

        entry.appendChild(jobEntry);
        entry.appendChild(statusEntry);
        entry.appendChild(detailEntry);
        table.appendChild(entry)
    }
}

async function loadPastMetrics(){
    const res = await fetch('/range_status_raw');
    const json_data = await res.json();

    const container = document.getElementById('range_data_container');
    container.innerHTML="" // Clear "Loading...,

    const history = document.createElement("table");
    history.setAttribute('id', 'history_table')
    container.appendChild(history);

    const head = document.createElement("tr")
    head.setAttribute('id', 'range_headline')
    head.innerHTML = `
        <td>Prev. Day</td>
        <td> <------------ </td>
        <td>History of past 24 Hours</td>
        <td> ------------> </td>     
        <td>Now.</td>
    `;
    history.appendChild(head)

    for (const datapoint of json_data.data.result) {
        const { instance, job } = datapoint.metric;
        const entry = document.createElement('tr');
        // necessary to align the auto_padding
        const cell = document.createElement('td');

        const svgNS = "http://www.w3.org/2000/svg";
        //cell.textContent += job; //debug purposes
        let counter = 0; //calculate when to insert a separator
        for (const hour of datapoint.values){
            // block = document.createElementNS(svgNS,"rect")
            const status = hour[1] === "1" ? "✅" : "❌";
            cell.textContent += status;

            if (counter % 4 === 3){
                cell.textContent += " | "
            }
            counter ++;
        }

        entry.appendChild(cell)
        history.appendChild(entry)
    }


}
loadCurrentMetrics();
loadPastMetrics();
