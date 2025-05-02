const boardElement = document.getElementById("board");
const statusElement = document.getElementById("status");

function updateBoard(fullBoard, currentTurn) {
    const cells = boardElement.querySelectorAll(".cell");

    // Count how many moves each player has made
    let moveCounts = { "X": 0, "O": 0 };
    fullBoard.flat().forEach(cell => {
        if (cell && Array.isArray(cell)) {
            const [player] = cell;
            moveCounts[player]++;
        }
    });

    cells.forEach(cell => {
        const r = parseInt(cell.dataset.row);
        const c = parseInt(cell.dataset.col);
        const cellData = fullBoard[r][c];

        cell.textContent = '';
        cell.classList.remove("X", "O", "fading", "visible");

        if (cellData && Array.isArray(cellData)) {
            const [player, turnPlaced, moveNumber] = cellData;
            const playerMoveCount = moveCounts[player];

            const isVisible = playerMoveCount < moveNumber + 3;
            const isFading = playerMoveCount === moveNumber + 2;

            if (isVisible) {
                cell.textContent = player;
                cell.classList.add(player);
                cell.classList.add(isFading ? "fading" : "visible");
            }
        }
    });
}

function attachCellListeners() {
    const cells = boardElement.querySelectorAll(".cell");
    cells.forEach(cell => {
        cell.addEventListener("click", () => {
            const row = cell.dataset.row;
            const col = cell.dataset.col;

            fetch("/move", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ row, col })
            })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                updateBoard(data.board, data.turn);
                if (data.winner) {
                    if (data.winner === "X") {
                        statusElement.textContent = "You Win!";
                    } else if (data.winner === "O") {
                        statusElement.textContent = "Cat win!";
                    } else {
                        statusElement.textContent = `${data.winner} wins!`;
                    }
                } else {
                    statusElement.textContent = "";
                }
            });
        });
    });
}

function resetGame() {
    fetch("/reset", { method: "POST" })
        .then(() => {
            updateBoard([[null, null, null], [null, null, null], [null, null, null]], 0);
            statusElement.textContent = "";
        });
}

document.getElementById("reset-btn").addEventListener("click", resetGame);
attachCellListeners();
