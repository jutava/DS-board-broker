from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        pass
	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
		receive_request_from_client(post_data)
	
# Process request from client
def receive_request_from_client(message):
	authenticate_user(message)
	if is_update(message):
		update_board(message)
	else:
		get_board()
	
	pass

# Send request to server to get board status
def get_board():
	pass
	
def update_board(message):
	
# Ensure that request is coming from application
def authenticate_user():
	pass

# Check that client message is a request to update board
def is_update(message):
	pass
		
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
	
	
