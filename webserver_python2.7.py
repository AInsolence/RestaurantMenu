'''Python file for Web Server'''

#Python 2.7
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This file created web server and HTTP request handler for it
#http.server module docs: https://docs.python.org/3.4/library/http.server.html

from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

'''Interaction with database'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
#Create engine and session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()
#get all restaurants query
restaurants = session.query(Restaurant.name).order_by(Restaurant.name.asc()).all()

'''Server'''

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                #get all restaurants names query
                restaurants = session.query(Restaurant.name).order_by(Restaurant.name.asc()).all()
                output = ""
                output += "<html><body>"
                for restaurant in restaurants:
                    output += "<h1> %s <h1>" % restaurant
                    output += "</br>"
                    output += "<h2><a href = "/id/edit">Edit</a><h2>"
                    output += "</br>"
                    output += "<h2><a href = "/delete">Delete</a><h2>"
                    output += "</br></br></br>"
                output += "<h2><a href = "restaurants/new">Make a New Restaurant</a><h2>"
                output += "</br></br>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:          
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    self.wfile.write(output)
                    print output
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