'''Python script added data in our DB'''

#Import our databases
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
#Create engine and session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession

#Add first new Restaurant in our menu
myFirstRestaurant = Restaurant(name = 'Pizza Palace')
session.add(myFirstRestaurant)
session.commit()
#Check result
session.query(Restaurant).all()

#Add first new menu item in our menu of Pizza Palace
cheesepizza = MenuItem(name = 'Cheese Pizza', course = 'Entree', description = 'Made with all natural ingredients and fresh mozarella.', prise = '8.99',restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()
#Check result
session.query(MenuItem).all()

#Add second menu item in our menu of Pizza Palace
seafoodpizza = MenuItem(name = 'Seafood Pizza', course = 'Entree', description = 'Made with shrimps, salman and smokee anchovies.', prise = '11.50',restaurant = myFirstRestaurant)
session.add(seafoodpizza)
session.commit()
#Check first object and get it name attribute
firstResult = session.query(Restaurant).first()
firstResult.name

