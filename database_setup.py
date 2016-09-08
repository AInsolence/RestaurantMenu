#!/usr/bin/env python
# database_setup.py -- Python module for Restaurant Menu project.
# Module create, read, update and delete information on sqlite databases used for that web site.
# Use sqlite module DOCUMENTATION ## https://www.sqlite.org/docs.html ##
# Use sqlalchemy module to work with database. DOCUMENTATION ## http://docs.sqlalchemy.org/en/latest ##
# master branch

#imports#
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant():
    '''Class for create objects which will representing restaurants'''
    __tablename__ = 'restaurant' #table info
    #mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    
    
class MenuItem():
    '''Class for create objects which will representing restaurants'''
    __tablename__ = 'menu_item' #table info
    #mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    
    
    
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)