from http.server import BaseHTTPRequestHandler, HTTPServer
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
                    output += "<a href ='/restaurants/%d/edit' >Edit </a> "%restaurant.id
                    output += "</br>"
                    output += "<a href ='/restaurants/%d/delete'> Delete </a>"%restaurant.id
                    output += "</br></br>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            
            if self.path.endswith("/edit") and self.path.split('/')[-3] == "restaurants" and self.path.split('/')[-1] == "edit":
                id = self.path.split('/')[-2]
                restaurant = rh.get(id)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body><h2>%s</h2>"%restaurant.name
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action='/restaurants/%d/edit'>"%restaurant.id
                    output += "<input name='name' type='text' placeholder = 'Name' value='%s'>"%restaurant.name
                    output += "<input type='submit' value='Update'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                else:
                    raise IOError
                return
            
            if self.path.endswith("/delete") and self.path.split('/')[-3] == "restaurants" and self.path.split('/')[-1] == "delete":
                id = self.path.split('/')[-2]
                restaurant = rh.get(id)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body><h2>Do you really want to delete '%s' ?</h2>"%restaurant.name
                    output += "<form method = 'POST' enctype = 'multipart/form-data' action='/restaurants/%d/delete'>"%restaurant.id
                    output += "<input type='submit' value='Delete'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                else:
                    raise IOError
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

            if self.path.endswith("/edit") and self.path.split('/')[-3] == "restaurants" and self.path.split('/')[-1] == "edit":
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                    
                    id = self.path.split('/')[-2]
                    restaurant = rh.get(id)
                    restaurant.name = messagecontent[0]
                    rh.update(restaurant)

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            
            if self.path.endswith("/delete") and self.path.split('/')[-3] == "restaurants" and self.path.split('/')[-1] == "delete":
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    
                    id = self.path.split('/')[-2]
                    rh.delete(id)

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except Exception as e:
            print(e)
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