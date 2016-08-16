'''Restaurant menu python file'''

#imports#
import sys
from sqlalchemy import Column, ForegnKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm importrelationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant():
    '''Class for create objects which will representing restaurants'''
    __tablename__ = 'restaurant' #table info#
    
    '''Mapper'''
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    
    
class MenuItem():
    '''Class for create objects which will representing restaurants'''
    __tablename__ = 'menu_item' #table info#
    
    '''Mapper'''
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    prise = Column(String(8))
    restaurant_id = Column(Integer, ForegnKey('restaurant.id'))
    restaurant = relationship(Restaurant)
    
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)