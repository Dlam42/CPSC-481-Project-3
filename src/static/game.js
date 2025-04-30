const boardElement = document.getElementById('board');
const statusElement = document.getElementById('status');
const resetButton = document.getElementById('reset-button');
const HUMAN_PLAYER = 'X';
const AI_PLAYER = 'O';
let currentPlayer = HUMAN_PLAYER; // Human starts
let gameOver = false;

// --- Create Board Cells ---
function createBoard() {
    boardElement.innerHTML = ''; // Clear previous board
    for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = r;
            cell.dataset.col = c;
            cell.addEventListener('click', handleCellClick);
            boardElement.appendChild(cell);
        }
    }
}

// --- Update Visual Board ---
function updateBoard(fullBoard, currentTurn) {
    const cells = boardElement.querySelectorAll('.cell');

    // Count how many moves each player has made
    let moveCounts = { 'X': 0, 'O': 0 };
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
        cell.classList.remove('X', 'O', 'visible', 'fading');

        if (cellData && Array.isArray(cellData)) {
            const [player, turnPlaced, moveNumber] = cellData;
            const playerMovesSoFar = moveCounts[player];

            const isVisible = playerMovesSoFar < moveNumber + 3;
            const isFading = playerMovesSoFar === moveNumber + 2;

            if (isVisible) {
                cell.textContent = player;
                cell.classList.add(player);
                if (isFading) {
                    cell.classList.add('fading');
                } else {
                    cell.classList.add('visible');
                }
            }
        }
    });
}


// --- Handle Cell Click (Human Move) ---
async function handleCellClick(event) {
    if (gameOver || currentPlayer !== HUMAN_PLAYER) {
        return; // Ignore clicks if game over or not human's turn
    }

    const cell = event.target;
    const row = parseInt(cell.dataset.row);
    const col = parseInt(cell.dataset.col);

   
    try {
        statusElement.textContent = `Sending move (${row},${col})... AI thinking...`;
        boardElement.style.pointerEvents = 'none'; // Disable board during AI turn

        const response = await fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ row: row, col: col, player: HUMAN_PLAYER }),
        });

        // REMOVED: boardElement.style.pointerEvents = 'auto'; // DO NOT re-enable here

        if (!response.ok) {
            const errorData = await response.json();
             boardElement.style.pointerEvents = 'auto'; // Re-enable on error
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }

        const gameState = await response.json();
        // Pass received gameState to the update function
        handleGameStateUpdate(gameState);

    } catch (error) {
        console.error('Error making move:', error);
        statusElement.textContent = `Error: ${error.message}. Try again.`;
        boardElement.style.pointerEvents = 'auto'; // Re-enable board on error
    }
}

// --- Handle Game State Update from Backend ---
// Modify this function in static/game.js
function handleGameStateUpdate(gameState) {
    console.log("Received game state from backend:", gameState);

    // Check if needed keys exist before using them
    if (gameState.full_board === undefined || gameState.current_turn === undefined) {
        console.error("Error: full_board or current_turn missing from backend response!");
        statusElement.textContent = "Error: Invalid data from server.";
        // Potentially reset board or show error state
        return; // Stop processing if data is missing
    }

    // Use full_board and current_turn from gameState
    updateBoard(gameState.full_board, gameState.current_turn);
    statusElement.textContent = gameState.message || `Turn ${gameState.current_turn}`;

    gameOver = gameState.game_over;
    console.log("JS gameOver variable set to:", gameOver);

    if (gameOver) {
        statusElement.textContent = gameState.message || `Game Over! Winner: ${gameState.winner}`;
        console.log("Setting pointerEvents to 'none' (Game Over)");
        boardElement.style.pointerEvents = 'none';
    } else {
        // Set player based on backend state
        currentPlayer = gameState.current_player; // Use backend value
        console.log(`JS currentPlayer variable set to: ${currentPlayer} (from backend)`);

        let pointerEventsValue = (currentPlayer === HUMAN_PLAYER) ? 'auto' : 'none';
        console.log(`Setting pointerEvents to: '${pointerEventsValue}'`);
        boardElement.style.pointerEvents = pointerEventsValue; // Correctly enables/disables
    }
}


// --- Reset Game ---
async function resetGame() {
    try {
       const response = await fetch('/reset', { method: 'POST' });
       if (!response.ok) {
           throw new Error(`HTTP error! status: ${response.status}`);
       }
       const gameState = await response.json();

       // Check if response contains the expected fields after reset
       if (gameState.full_board === undefined || gameState.current_turn === undefined || gameState.current_player === undefined) {
            console.error("Error: Reset response missing required fields!");
            // Handle error - maybe just create a default empty board visually?
            createBoard(); // Recreate empty visual board
            statusElement.textContent = "Error resetting game. Please refresh.";
            return;
       }

       currentPlayer = HUMAN_PLAYER; // Reset starting player
       gameOver = false;
       // Pass received gameState to the update function
       handleGameStateUpdate(gameState);
       boardElement.style.pointerEvents = 'auto'; // Ensure board is enabled
       statusElement.textContent = "Game Reset! Player X's Turn";


   } catch (error) {
       console.error('Error resetting game:', error);
       statusElement.textContent = "Error resetting game.";
   }
}

// --- Initial Setup ---
resetButton.addEventListener('click', resetGame);
createBoard(); // Create the initial empty board display
statusElement.textContent = "Player X's Turn"; // Initial status