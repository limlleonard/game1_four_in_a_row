const C = 7;
const R = 6;
const size = 100; // size of a cell
const diameter = 80;
const root = document.documentElement;
root.style.setProperty("--diameter", "80px");
const board = document.getElementById("board");
let gameOn = false;

function brettErstellen() {
    board.innerHTML = "";
    for (let r = 0; r < R; r++) {
        for (let c = 0; c < C; c++) {
            const circle = document.createElement("div");
            circle.classList.add("circle");
            circle.style.left = `${c * size + size / 2 - diameter / 2}px`;
            circle.style.top = `${r * size + size / 2 - diameter / 2}px`;
            board.appendChild(circle);
            if (r === 0) {
                const spalte = document.createElement("div");
                spalte.classList.add("spalte");
                // spalte.setAttribute("id", `spalte${c}`);
                spalte.setAttribute("onclick", `klicken(${c});`);
                board.appendChild(spalte);
            }
        }
    }
}
function figurZeichnen(pos1, turn) {
    const figur = document.createElement("div");
    if (!turn) {
        // turn if from the last move, therefore reverse
        figur.classList.add("p1");
    } else {
        figur.classList.add("p2");
    }
    figur.style.left = `${pos1[1] * size + size / 2 - diameter / 2}px`;
    figur.style.top = `${pos1[0] * size + size / 2 - diameter / 2}px`;
    board.appendChild(figur);
}
function start() {
    const mode = document.getElementById("mode").value;
    fetch("/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode: mode }), // Send the direction as JSON
    }).catch((err) => console.error("Error start", err));
}
function reset() {
    const elements = document.querySelectorAll(".p1, .p2");
    elements.forEach((element) => element.remove());
    board.innerHTML = "";
    brettErstellen();

    fetch("/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({}), // Send the direction as JSON
    }).catch((err) => console.error("Error reset", err));
}
function klicken(pos1) {
    fetch("/klicken", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pos1: pos1 }), // Send the direction as JSON
    }).catch((err) => console.error("Error start", err));
}
document.addEventListener("DOMContentLoaded", () => {
    // Establish WebSocket connection to Flask-SocketIO
    const socket = io();
    // Listen for 'snake_info' events
    socket.on("drop_info", (data) => {
        if (data.message) {
            alert(data.message);
        } else if (data.pos1) {
            figurZeichnen(data.pos1, data.turn);
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    brettErstellen();
});
