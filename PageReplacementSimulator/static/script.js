function runSimulation() {
    const pages = document.getElementById("pages").value;
    const capacity = document.getElementById("capacity").value;
    const algorithm = document.getElementById("algorithm").value;

    fetch("/simulate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            pages: pages,
            capacity: capacity,
            algorithm: algorithm
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Debug (optional)

        // ✅ Update top cards
        document.getElementById("faults").innerText = "Faults: " + data.faults;
        document.getElementById("hits").innerText = "Hits: " + data.hits;

        let total = data.hits + data.faults;
        let ratio = total === 0 ? 0 : ((data.hits / total) * 100).toFixed(2);

        document.getElementById("ratio").innerText = "Hit Ratio: " + ratio + "%";

        // ✅ Build table
        let tableHTML = "<table>";

        // Header row (steps)
        tableHTML += "<tr><th>Step</th>";
        for (let i = 0; i < data.history.length; i++) {
            tableHTML += `<th>${i + 1}</th>`;
        }
        tableHTML += "</tr>";

        // Determine max frames (important fix)
        let maxFrames = 0;
        data.history.forEach(step => {
            if (step.length > maxFrames) {
                maxFrames = step.length;
            }
        });

        // Frame rows
        for (let f = 0; f < maxFrames; f++) {
            tableHTML += `<tr><th>Frame ${f + 1}</th>`;

            for (let i = 0; i < data.history.length; i++) {
                let val = data.history[i][f] !== undefined ? data.history[i][f] : "-";

                let cls = data.status[i] === "hit" ? "hit" : "miss";

                tableHTML += `<td class="${cls}">${val}</td>`;
            }

            tableHTML += "</tr>";
        }

        // Status row
        tableHTML += "<tr><th>Status</th>";
        for (let i = 0; i < data.status.length; i++) {
            let text = data.status[i].toUpperCase();
            let cls = data.status[i] === "hit" ? "hit" : "miss";

            tableHTML += `<td class="${cls}">${text}</td>`;
        }
        tableHTML += "</tr>";

        tableHTML += "</table>";

        document.getElementById("tableContainer").innerHTML = tableHTML;
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong. Check console.");
    });
}