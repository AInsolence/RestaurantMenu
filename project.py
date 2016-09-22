#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project.py -- Python module for Restaurant Menu project.
# Description here
# Used flask module DOCUMENTATION ## http://flask.pocoo.org/ ##
# Used sqlalchemy module to interact with database. DOCUMENTATION ## http://docs.sqlalchemy.org/en/latest ##
# master branch

#imports
from flask import Flask

app = Flask(__name__)
@app.route('/')
@app.route('/hello')

def HelloWorld():
    return 'Hello World!!!'

    
if __name__ = '__main__':
    app.debug = True
    app.run(host = 0.0.0.0, port = 5000)
