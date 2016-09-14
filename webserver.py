'''Python file for Web Server'''

#Python 3.4
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This file created web server and HTTP request handler for it
#http.server module docs: https://docs.python.org/3.4/library/http.server.html

from http.server import HTTPServer, BaseHTTPRequestHandler

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ""
                output += "<html><body>Hello from server!!!</body></html>"
                self.wfile.write(output)
                print output
                return
                
        except:
            self.send_error(404, "File Not Found %s" % self.path)
    
def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)#we instantiate HTTPServer, pointing to him, what address and handler use to work with http-queries
        print "Web server running on port %s" % port
        server.serve_forever()
        
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ = '__main__':
    main()