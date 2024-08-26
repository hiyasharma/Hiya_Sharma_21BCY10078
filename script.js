let socket;
let playerId = prompt("Enter your player ID (A or B):");
const gameId = "game1"; // Static game ID for simplicity
const boardElement = document.getElementById("board");
const statusElement = document.getElementById("status");
const characterOptions = document.getElementById("character-options");
const moveHistoryElement = document.getElementById("moveHistory");
const removedCharactersElement = document.getElementById("removedList");
let selectedCharacter = null;
let currentTurn = "A"; // Initialize with Player A's turn

function createWebSocket() {
    // Connect to WebSocket server
    socket = new WebSocket(`ws://localhost:8000/ws/${gameId}/${playerId}`);

    socket.onopen = () => {
        console.log("Connected to the WebSocket server");
    };

    socket.onmessage = (event) => {
        console.log("Message received from server:", event.data);
        const data = JSON.parse(event.data);

        if (data.error) {
            statusElement.textContent = `Error: ${data.error}`;
        } else {
            updateBoard(data.board);
            updateStatus(data);
            populateCharacterOptions(data.board);

            // Update the current turn based on server state
            currentTurn = data.turn === 0 ? "A" : "B";

            // Update the move history
            updateMoveHistory(data.move_history);

            // Ensure removed_characters is an array and update
            updateRemovedCharacters(Array.isArray(data.removed_characters) ? data.removed_characters : []);
        }
    };

    socket.onerror = (error) => {
        console.log("WebSocket error:", error);
    };

    socket.onclose = () => {
        console.log("Disconnected from the WebSocket server");
    };
}

function updateBoard(board) {
    boardElement.innerHTML = ''; // Clear existing board

    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 5; j++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            if (board[i][j]) {
                const [player, char] = board[i][j].split('-');
                cell.textContent = char;
                cell.dataset.player = player; // Add data attribute for styling
            }
            boardElement.appendChild(cell);
        }
    }
}

function updateStatus(gameState) {
    if (gameState.is_over) {
        statusElement.textContent = "Game Over!";
    } else {
        statusElement.textContent = `Player ${gameState.turn === 0 ? 'A' : 'B'}'s Turn`;
    }
}

function populateCharacterOptions(board) {
    characterOptions.innerHTML = ''; // Clear existing options
    const playerCharacters = [];

    // Find all characters belonging to the current player
    board.flat().forEach(cell => {
        if (cell && cell.startsWith(playerId)) {
            playerCharacters.push(cell);
        }
    });

    // Populate character options
    playerCharacters.forEach(char => {
        const charName = char.split('-')[1];
        const option = document.createElement("div");
        option.classList.add("character-option");
        option.textContent = charName;
        option.onclick = () => selectCharacter(char);
        characterOptions.appendChild(option);
    });
}

function selectCharacter(char) {
    selectedCharacter = char;

    // Remove 'selected' class from all character options
    document.querySelectorAll(".character-option").forEach(option => {
        option.classList.remove("selected");
    });

    // Find and add 'selected' class to the clicked character option
    const charName = char.split('-')[1];
    const options = document.querySelectorAll(".character-option");

    options.forEach(option => {
        if (option.textContent === charName) {
            option.classList.add("selected");
        }
    });

    console.log(`Selected character: ${char}`);
}

function updateMoveHistory(moveHistory) {
    moveHistoryElement.innerHTML = `<h2>Move History</h2><ul>${moveHistory.map(move => `<li>${move}</li>`).join('')}</ul>`;
}

function updateRemovedCharacters(removedChars) {
    removedCharactersElement.innerHTML = removedChars.map(char => `<li>${char}</li>`).join('');
}

function sendMove(direction) {
    if (!selectedCharacter) {
        alert("Please select a character first!");
        return;
    }

    // Extract the character type (e.g., 'H1') from the selectedCharacter
    const characterType = selectedCharacter.split('-')[1];

    // Construct the move string in the format 'Character:Direction'
    const moveCommand = `${characterType}:${direction}`;

    // Construct the message to be sent to the server
    const message = {
        player: playerId,
        move: moveCommand
    };

    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify(message));
        console.log("Sent message to server:", message);
    } else {
        statusElement.textContent = "Unable to send move. Connection is not open.";
    }
}


// Initialize WebSocket connection
createWebSocket();
