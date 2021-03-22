from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from urllib.parse import urlparse, parse_qs

#########
#VARIABLES:

hostName = "localhost"
serverPort = 8080
ServerURL = "http://localhost:8079"

##########

mutex = False
latest_state = 1

class MyServer(BaseHTTPRequestHandler):
    def _set_get_response(self, board):
        self.send_response(200, message=board)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(json.dumps(board).encode('utf_8'))

    def _set_post_response(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'POST succeeded')

    def do_GET(self):
        state = int(parse_qs(urlparse(self.path).query)["state"][0])
        print("GET request received", self.path,"with params:", state,"From:", self.client_address)
        board = get_board(state)
        update_latest_state(board)
        self._set_get_response(board)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        status = receive_post_from_client(post_data)
        
        self._set_post_response(status)
	
# Process request from client
def receive_post_from_client(message):
    global mutex
    if authenticate_user():
        print("State is:", message["state"])
        if message["state"] is latest_state:
            if not mutex:
                mutex = True
                update_board(message)
                mutex = False
                return 200 #OK
            else:
                return 409 #Conflict
        else:
            return 403 #Forbidden
    else:
        return 401 #Unauthorized
        

# Send request to server to get board status
def get_board(state):
    payload = {"state":state}
    r = requests.get(url = ServerURL, params=payload)
    print("GET returned:", r.text)
    return r.text

def update_board(message):
    print("Sending post request to:", ServerURL)
    r = requests.post(url = ServerURL, data=json.dumps(message))
    return r.status_code

def authenticate_user():
    return True
    
def update_latest_state(board):
    if board = {}:
        pass
    else:
        global latest_state
        length = len(list(board.keys()))
        if max(list(board.keys()))[0] = "is_whole_board":
            state = int(list(board.keys())[length - 2]
        else 
            state = int(list(board.keys())[length - 1])
        if state > latest_state:
            latest_state = state

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Broker started at http://%s:%s" % (hostName, serverPort))

    webServer.serve_forever()

    webServer.server_close()
	
