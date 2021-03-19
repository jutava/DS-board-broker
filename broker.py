from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
from urllib.parse import urlparse

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
        state = (urlparse(self.path).query)
        print("GET request received", self.path,"with params:", state,"From:", self.client_address)
        board = get_board(state)
        global latest_state # DO THIS PART
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
            return get_board(message["state"])
    else:
        return 401 #Unauthorized
        

# Send request to server to get board status
def get_board(state):   
    r = requests.get(url = ServerURL)
    print("GET returned:", r.text)
    return r.text

def update_board(message):
    print("Sending post request to:", ServerURL)
    r = requests.post(url = ServerURL, data = message)
    return r.text

# Ensure that request is coming from application
def authenticate_user():
    return True

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    webServer.serve_forever()

    webServer.server_close()
	
