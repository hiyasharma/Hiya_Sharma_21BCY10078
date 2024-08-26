import asyncio
import websockets
import json

class GameServer:
    def __init__(self):
        self.clients = {}  # Dictionary to map player IDs to WebSocket objects
        self.board = [
            ["A-P1", "A-H1", "A-H1", "A-H2", "A-H2"],
            [None, None, None, None, None],
            [None, None, None, None, None],
            [None, None, None, None, None],
            ["B-P1", "B-H1", "B-H1", "B-H2", "B-H2"]
        ]
        self.move_history = []
        self.current_turn = 0  # 0 for Player A, 1 for Player B
        self.game_over = False
    async def broadcast_game_state(self):
        game_state = {
            "board": self.board,
            "turn": self.current_turn,
            "is_over": self.game_over,
            "move_history": self.move_history  # Include move history in the game state
        }
        if self.clients:  # Send to all clients
            tasks = [asyncio.create_task(client.send(json.dumps(game_state))) for client in self.clients.values()]
            await asyncio.gather(*tasks)



    async def handle_move(self, move, player):
        if self.game_over:
            return

        # Check if it's the player's turn
        if (player == "A" and self.current_turn != 0) or (player == "B" and self.current_turn != 1):
            await self.send_error(player, "It's not your turn!")
            return

        try:
            if not self.validate_move(player, move):
                await self.send_error(player, "Invalid move format.")
                return

            character, direction = move.split(":")
            player_prefix = f"{player}-"
            move_made = False

            # Find the character on the board and move it
            for i, row in enumerate(self.board):
                for j, cell in enumerate(row):
                    if cell and cell.startswith(player_prefix) and cell.split("-")[1] == character:
                        move_made = self.apply_move(i, j, direction, player_prefix + character)
                        if move_made:
                            break
                if move_made:
                    break

            if move_made:
                # Switch turns
                self.current_turn = 1 if self.current_turn == 0 else 0
                self.move_history.append(f"{player}:{character}:{direction}")
                self.check_game_over()
                await self.broadcast_game_state()
            else:
                await self.send_error(player, "Move failed. Either character not found or invalid move.")
        except Exception as e:
            print(f"Error handling move: {e}")
            await self.send_error(player, "An error occurred while processing the move.")



    def apply_move(self, start_i, start_j, direction, character):
        direction_map = {
            "L": (0, -1), "R": (0, 1), "F": (1, 0), "B": (-1, 0),
            "FL": (-1, -1), "FR": (-1, 1), "BL": (1, -1), "BR": (1, 1)
        }

        if direction not in direction_map:
            print(f"Invalid direction: {direction}")
            return False

        di, dj = direction_map[direction]

        if character.startswith("A-"):
            player_prefix = "A-"
        elif character.startswith("B-"):
            player_prefix = "B-"
        else:
            print(f"Invalid player prefix: {character}")
            return False

        if character == "A-P1" or character == "B-P1":
            # P1 moves 1 block and kills the destination player
            new_i, new_j = start_i + di, start_j + dj
            if self.is_valid_move(new_i, new_j) or self.is_enemy_piece(new_i, new_j, player_prefix):
                # Move P1 to the new position
                self.board[new_i][new_j] = self.board[start_i][start_j]
                self.board[start_i][start_j] = None
                return True

        elif character == "A-H1" or character == "B-H1":
            # H1 moves 2 blocks in the same direction and kills any opponent in its path
            new_i1, new_j1 = start_i + di, start_j + dj
            new_i2, new_j2 = start_i + 2 * di, start_j + 2 * dj
            if self.is_valid_move(new_i2, new_j2):
                if self.board[new_i1][new_j1] is None or self.is_enemy_piece(new_i1, new_j1, player_prefix):
                    # Kill any opponent in the path and move H1
                    self.board[new_i2][new_j2] = self.board[start_i][start_j]
                    self.board[start_i][start_j] = None
                    return True

        elif character == "A-H2" or character == "B-H2":
            # H2 moves 2 blocks diagonally and kills any opponent in its path
            new_i1, new_j1 = start_i + di, start_j + dj
            new_i2, new_j2 = start_i + 2 * di, start_j + 2 * dj
            if self.is_valid_move(new_i2, new_j2):
                if self.board[new_i1][new_j1] is None or self.is_enemy_piece(new_i1, new_j1, player_prefix):
                    # Kill any opponent in the path and move H2
                    self.board[new_i2][new_j2] = self.board[start_i][start_j]
                    self.board[start_i][start_j] = None
                    return True

        print(f"Move failed for {character} at ({start_i}, {start_j}) with direction {direction}")
        return False

    def is_valid_move(self, i, j):
        return 0 <= i < 5 and 0 <= j < 5

    def is_enemy_piece(self, i, j, player_prefix):
        return self.board[i][j] and not self.board[i][j].startswith(player_prefix)




    async def send_error(self, player, error_message):
        if player in self.clients:
            await self.clients[player].send(json.dumps({"error": error_message}))

    def check_game_over(self):
        player_a_pieces = any(cell and cell.startswith("A") for row in self.board for cell in row)
        player_b_pieces = any(cell and cell.startswith("B") for row in self.board for cell in row)

        if not player_a_pieces or not player_b_pieces:
            self.game_over = True

    async def handler(self, websocket, path):
        player_id = path.split("/")[-1]  # Extract player ID from URL
        self.clients[player_id] = websocket

        await self.broadcast_game_state()  # Send initial state to the new client

        try:
            async for message in websocket:
                print(f"Message received: {message}")  # Log incoming messages
                try:
                    data = json.loads(message)
                    player = data.get('player')
                    move = data.get('move')

                    if player != player_id:
                        await self.send_error(player_id, "Invalid player ID.")
                        continue

                    if self.validate_move(player, move):
                        await self.handle_move(move, player)
                    else:
                        await self.send_error(player_id, "Invalid move format.")
                except json.JSONDecodeError:
                    await self.send_error(player_id, "Invalid JSON format.")
        except websockets.ConnectionClosed:
            print("Client disconnected")
        finally:
            if player_id in self.clients:
                del self.clients[player_id]

    def validate_move(self, player, move):
        if not isinstance(move, str) or ":" not in move:
            return False
        character, direction = move.split(":")
        direction_map = {"L", "R", "F", "B", "FL", "FR", "BL", "BR"}
        return player in ["A", "B"] and character.isalnum() and direction in direction_map

async def main():
    server = GameServer()
    async with websockets.serve(server.handler, "localhost", 8000):
        print("Server started on ws://localhost:8000")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
