from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Restaurant, MenuItem
from CRUD import RestaurantHandler

rh = RestaurantHandler()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body><h2>Create a new restaurant</h2>"
                output += "<form method = 'POST' enctype = 'multipart/form-data' action='/restaurants/new'>"
                output += "<input name='name' type='text' placeholder = 'Name'>"
                output += "<input type='submit' value='Create'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""                
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Create a new restaurant</a></br></br>"
                output += "<h2>List of restaurants</h2>"

                restaurants = rh.getall()
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href ='#' >Edit </a> "
                    output += "</br>"
                    output += "<a href =' #'> Delete </a>"
                    output += "</br></br>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            
        except IOError:
            self.send_error(404, "File not found %s" % self.path)
    
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')

                    restaurant = Restaurant(name = messagecontent[0])
                    rh.create(restaurant)

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass

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