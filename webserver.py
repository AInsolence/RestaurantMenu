'''Python file for Web Server'''

#Python 3.4
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This file created web server and HTTP request handler for it
#http.server module docs: https://docs.python.org/3.4/library/http.server.html

from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ""
                output += "<html><body>"
                output += "Hello from server!!!"
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?<h2><input name = 'message' type = 'text' ><input type = 'submit' value = 'Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                print (output)
                return
            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                output = ""
                output += "<html><body>"
                output += "&#161&#161&#161Hola-Hola!!!<a href = '/hello'>BAck to english!</a>"# '&#161' = upside-down exclamation point
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?<h2><input name = 'message' type = 'text' ><input type = 'submit' value = 'Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output.encode('utf-8'))
                print (output)
                return
        except:
            self.send_error(404, "File Not Found %s" % self.path)
            
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')[0].decode('utf-8')
            output = ''
            output += '<html><body>'
            output += '<h2> Okay, how about this: </h2>'
            output += '<h1> %s </h1>' % messagecontent
            output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
            output += '</html></body>'
            self.wfile.write(output.encode('utf-8'))
            print (output)
        except:
            pass
def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)#we instantiate HTTPServer, pointing to him, what address and handler use to work with http-queries
        print ("Web server running on port %s" % port)
        server.serve_forever()
        
    except KeyboardInterrupt:
        print (" entered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()