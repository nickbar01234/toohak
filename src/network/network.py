import socket 

# Thought: network only used by clients? since each client will have a network object and 
# server will implement its own message passing protocol => since it keeps the list of clients in its own class

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.0.0.137" # WARNING: hardcode & need to be consistenet with server.py
        self.port = 5555
        self.server_addr = (self.server, self.port)
        self.pos = self.connect()
    
    def connect(self):
        try: 
            self.client.connect(self.server_addr)
            return self.client.recv(2048).decode()
        except:
            pass 
    
    def send_name(self, name):
        try:
            self.client.send(str.encode(name))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
    
    def send_questions(questions):
        return
    def update_progress(name, ans):
        return
    def update_leaderboard(top5players):
        return
    def finish_game(time):
        return

# Testing 
n = Network()
print(n.send_name("Toffoli"))