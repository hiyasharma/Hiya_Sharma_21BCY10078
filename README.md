*Battle Of The Grid*


Battle Of The Grid is a web-based, turn-based strategy game similar to chess, but played on a 5x5 grid. Players can choose from different characters and move them around the grid to battle opponents. The game features real-time updates and a dynamic interface for character selection and move execution.

*Table of Contents*


-Features
-Installation
-Usage
-How It Works
-Technologies Used
-Contributing
-License

*Features*


-5x5 Grid: A chess-like board where players can move their characters.
-Character Selection: Players can choose their characters by clicking on them.
-Real-Time Updates: Move updates and game status are synchronized via WebSocket.
-Move History: Displays a history of moves made during the game.
-Removed Characters: Shows characters that have been removed from play.

![image](https://github.com/user-attachments/assets/54885386-084a-4bc5-b7b3-cd6e1e5e5044)
![image](https://github.com/user-attachments/assets/5c56b895-682a-43c3-95f4-e118c7c0e4dc)

*Installation*


1.Clone the Repository

Code-
-git clone https://github.com/yourusername/battle-of-the-grid.git
-cd battle-of-the-grid

2.Install Dependencies

You need to have Node.js installed to run the WebSocket server. Install the necessary packages:
Code-
-npm install

3.Run the WebSocket Server

Navigate to the server directory and start the server:
Code-
-cd server
-node server.js

4.Open the Game in Your Browser

Open index.html in your web browser to start playing the game.

*Usage*


1.Select Characters: Click on the character options to select and place them on the board.
2.Move Characters: Use the directional buttons to move your selected character around the grid.
3.View Move History: Check the move history section to see all the moves made during the game.
4.View Removed Characters: See which characters have been removed from play.

*How It Works*


-Game Setup: Players connect to the WebSocket server and choose their characters.
-Game Play: Players make moves using the UI, and the game state is updated in real-time.
-Move Execution: Moves are sent to the server, which updates the game state and notifies both players.
-Move History: The server maintains a log of moves which is displayed to the players.

*Technologies Used*


HTML: Markup for the game interface.
CSS: Styling for the game layout.
JavaScript: Game logic and WebSocket communication.
WebSocket: Real-time communication between the client and server.
Python: Server-side logic and WebSocket handling.

*Contributing*


Contributions are welcome! Please fork the repository and submit a pull request with your changes.
Fork the Repository
Create a Branch: git checkout -b feature/your-feature
Commit Your Changes: git commit -am 'Add new feature'
Push to the Branch: git push origin feature/your-feature
Create a New Pull Request

*License*


This project is licensed under the MIT License - see the LICENSE file for details.
