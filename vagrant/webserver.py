from http.server import BaseHTTPRequestHandler, HTTPServer

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ""
                message += "<html><body>Hello!</body></html>"
                self.wfile.write(bytes(message, "utf-8"))
                print(message)
                return
            
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ""
                message += "<html><body> &#161 Hola ! <a href='/hello'>Back to hello</a></body></html>"
                self.wfile.write(bytes(message, 'utf-8'))
                print(message)
                return
        except IOError:
            self.send_error(404, "File not found %s" % self.path)

def main():
    try:
        port = 8080
        server = HTTPServer(("", port), webserverHandler)
        print("Webserver running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()
        print("Server stopped.")

if __name__ == '__main__':
    main()