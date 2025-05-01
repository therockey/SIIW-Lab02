import socket
import json
import argparse
import importlib
import sys

class ClobberAIClient:
    def __init__(self, host='localhost', port=5555, depth=2, heuristic_module="heuristics.simple_heuristic"):
        self.host = host
        self.port = port
        self.depth = depth
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player = None
        self.last_state = None

        # Dynamically load the heuristic module
        try:
            self.heuristic = importlib.import_module(heuristic_module)
        except ModuleNotFoundError as e:
            print(f"Error loading heuristic module '{heuristic_module}': {e}")
            sys.exit(1)

    def connect(self):
        self.sock.connect((self.host, self.port))
        print("Connected to server.")
        self.receive_assignment()

    def receive_assignment(self):
        msg = self.receive()
        if msg['type'] == 'assign':
            self.player = msg['player']
            print(f"Assigned as player: {self.player}")

    def receive(self):
        buffer = ''
        while True:
            chunk = self.sock.recv(4096).decode()
            if not chunk:
                return None
            buffer += chunk
            if '\n' in buffer:
                break
        return json.loads(buffer.strip())

    def send(self, message):
        self.sock.sendall(json.dumps(message).encode() + b'\n')

    def run(self):
        while True:
            msg = self.receive()
            if msg is None:
                print("Disconnected from server.")
                break

            msg_type = msg['type']

            if msg_type == 'state':
                self.last_state = msg['data']

            elif msg_type == 'your_turn':
                self.handle_turn()

            elif msg_type == 'invalid_move':
                print("Invalid move sent:", msg.get("reason", "Unknown"))

            elif msg_type == 'game_over':
                winner = msg['winner']
                if winner == self.player:
                    print(f"✅ I won! (Player {self.player})")
                else:
                    print(f"❌ I lost. I was {self.player}, winner was {winner}")
                break

    def handle_turn(self):
        print("AI thinking...")
        move = self.minimax_root(self.last_state, self.depth)
        if move:
            from_pos, to_pos = move
            self.send({
                "type": "move",
                "from": list(from_pos),
                "to": list(to_pos)
            })
        else:
            print("No valid move found.")

    def minimax_root(self, state, depth):
        moves = self.heuristic.get_valid_moves(state['board'], self.player)
        best_score = float('-inf')
        best_move = None
        for move in moves:
            new_board = self.heuristic.apply_move(state['board'], move, self.player)
            score = self.minimax(new_board, depth - 1, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, board, depth, is_maximizing):
        current = self.player if is_maximizing else self.opponent()
        moves = self.heuristic.get_valid_moves(board, current)
        if depth == 0 or not moves:
            return self.heuristic.evaluate_board(board, self.player)

        scores = []
        for move in moves:
            new_board = self.heuristic.apply_move(board, move, current)
            score = self.minimax(new_board, depth - 1, not is_maximizing)
            scores.append(score)

        return max(scores) if is_maximizing else min(scores)

    def opponent(self):
        return 'B' if self.player == 'W' else 'W'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=5555)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--heuristic", default="heuristics.simple_heuristic")
    args = parser.parse_args()

    client = ClobberAIClient(
        host=args.host,
        port=args.port,
        depth=args.depth,
        heuristic_module=args.heuristic
    )
    client.connect()
    client.run()
