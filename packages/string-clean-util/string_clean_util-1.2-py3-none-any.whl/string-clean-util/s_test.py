from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_url = urlparse(self.path)
        
        # Check if the request is for the /check_key path
        if parsed_url.path == '/check_key':
            # Parse the query parameters from the URL
            query_params = parse_qs(parsed_url.query)
            
            # Extract 'e' (email) and 'k' (key) parameters
            email = query_params.get('e', [None])[0]
            key = query_params.get('k', [None])[0]
            
            # If both email and key are present, save them to a file
            if email and key:
                with open('saved_data.txt', 'a') as file:
                    file.write(f'Email: {email}, Key: {key}\n')
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'Success: Email and key saved.\n')
            else:
                # If parameters are missing, return a 400 Bad Request
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Error: Missing email or key.\n')
        else:
            # If the path is not /check_key, return a 404 Not Found
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Error: Not Found.\n')

def run_server():
    # Define server address and port
    server_address = ('', 5050)  # '' means listen on all available interfaces
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Server running on port 5050...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()