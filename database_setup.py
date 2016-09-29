#!/usr/bin/env python
# -*- coding: utf-8 -*-
# database_setup.py -- Python module for Restaurant Menu project.
# Module create, read, update and delete information on sqlite databases used for that web site.
# Used sqlite module DOCUMENTATION ## https://www.sqlite.org/docs.html ##
# Used sqlalchemy module to work with database. DOCUMENTATION ## http://docs.sqlalchemy.org/en/latest ##
# master branch

#imports
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    '''Class for create objects which will represent restaurants'''
    __tablename__ = 'restaurant' #table info
    #mapper
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    logo_url = Column(String(100))
    id = Column(Integer, primary_key = True)
    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):
            return {
                'name': self.name,
                'description': self.description,
                'id': self.id,
            }    
    
class MenuItem(Base):
    '''Class for create objects which will represent menu items'''
    __tablename__ = 'menu_item' #table info
    #mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    image_url = Column(String(150))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):
            return {
                'name': self.name,
                'description': self.description,
                'id': self.id,
                'price': self.price,
                'course': self.course,
                'image_url': self.image_url,
            }    

        
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)