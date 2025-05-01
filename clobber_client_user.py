import socket
import json

class ClobberUserClient:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player = None  # Will be set on "assign"

    def connect(self):
        self.sock.connect((self.host, self.port))
        print("Connected to server.")
        self.receive_assignment()

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

    def receive_assignment(self):
        msg = self.receive()
        if msg['type'] == 'assign':
            self.player = msg['player']
            print(f"You are player {self.player}")

    def print_board(self, board):
        for row in board:
            print(' '.join(row))
        print()

    def run(self):
        while True:
            msg = self.receive()
            if msg is None:
                print("Disconnected from server.")
                break

            msg_type = msg['type']

            if msg_type == 'state':
                state = msg['data']
                self.print_board(state['board'])
                print(f"Current turn: {state['current_player']}")
                if state['game_over']:
                    print("Game over.")
                continue

            elif msg_type == 'your_turn':
                print("Your move.")
                from_r = int(input("From row: "))
                from_c = int(input("From col: "))
                to_r = int(input("To row: "))
                to_c = int(input("To col: "))
                self.send({
                    "type": "move",
                    "from": [from_r, from_c],
                    "to": [to_r, to_c]
                })

            elif msg_type == 'invalid_move':
                print("Invalid move:", msg.get('reason', 'Unknown reason'))

            elif msg_type == 'game_over':
                winner = msg['winner']
                if winner == self.player:
                    print(f"✅ You win! (You were {self.player})")
                else:
                    print(f"❌ You lose. You were {self.player}, winner was {winner}")
                break

if __name__ == "__main__":
    client = ClobberUserClient()
    client.connect()
    client.run()
