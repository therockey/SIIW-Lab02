import socket
import threading
import json
import gamelib

BOARD_ROWS = 5
BOARD_COLS = 5


def create_initial_board():
    board = []
    for r in range(BOARD_ROWS):
        row = []
        for c in range(BOARD_COLS):
            if (r + c) % 2 == 0:
                row.append('W')
            else:
                row.append('B')
        board.append(row)
    return board


class ClobberServer:
    def __init__(self, host='localhost', port=5555):
        self.board = create_initial_board()
        self.current_player = 'W'
        self.connections = {}  # {'W': conn1, 'B': conn2}
        self.host = host
        self.port = port
        self.lock = threading.Lock()
        self.game_over = False

    def start(self):
        print("Starting Clobber server...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(2)
        print("Waiting for two players...")

        players = ['W', 'B']
        for player in players:
            conn, addr = server.accept()
            print(f"Player {player} connected from {addr}")
            self.connections[player] = conn

            # Send player assignment
            conn.sendall(json.dumps({
                "type": "assign",
                "player": player
            }).encode() + b'\n')

        print("Both players connected. Game starting...")
        self.send_state_to_all()

        self.run_game_loop()

    def send_state_to_all(self):
        state_msg = json.dumps({
            "type": "state",
            "data": {
                "board": self.board,
                "current_player": self.current_player,
                "game_over": self.game_over
            }
        }).encode() + b'\n'
        for conn in self.connections.values():
            conn.sendall(state_msg)

    def send_to_player(self, player, msg):
        self.connections[player].sendall(json.dumps(msg).encode() + b'\n')

    def receive_from_player(self, player):
        conn = self.connections[player]
        buffer = ''
        while True:
            chunk = conn.recv(4096).decode()
            if not chunk:
                return None
            buffer += chunk
            if '\n' in buffer:
                break
        data = buffer.strip().split('\n')[0]
        return json.loads(data)

    def run_game_loop(self):
        while not self.game_over:
            current_conn = self.connections[self.current_player]
            opponent = 'B' if self.current_player == 'W' else 'W'

            valid_moves = gamelib.get_valid_moves(self.board, self.current_player)
            if not valid_moves:
                self.game_over = True
                self.send_state_to_all()
                winner = opponent
                for conn in self.connections.values():
                    conn.sendall(json.dumps({
                        "type": "game_over",
                        "winner": winner
                    }).encode() + b'\n')
                print(f"Game over! Winner is {winner}")
                break

            self.send_to_player(self.current_player, {"type": "your_turn"})

            move_data = self.receive_from_player(self.current_player)
            if move_data is None:
                print(f"Player {self.current_player} disconnected.")
                break

            if move_data['type'] == 'move':
                move = (tuple(move_data['from']), tuple(move_data['to']))
                if move in valid_moves:
                    self.board = gamelib.apply_move(self.board, move, self.current_player)
                    self.current_player = opponent
                    self.send_state_to_all()
                else:
                    self.send_to_player(self.current_player, {
                        "type": "invalid_move",
                        "reason": "Invalid move"
                    })


if __name__ == "__main__":
    server = ClobberServer()
    server.start()
