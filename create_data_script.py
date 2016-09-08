'''Python script changed data in our DB'''

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
cheesepizza = MenuItem(name = 'Cheese Pizza', course = 'Entree', description = 'Made with all natural ingredients and fresh mozarella.', price = '$8.99',restaurant = myFirstRestaurant)
session.add(cheesepizza)
session.commit()
#Check result
session.query(MenuItem).all()

#Add second menu item in our menu of Pizza Palace
seafoodpizza = MenuItem(name = 'Seafood Pizza', course = 'Entree', description = 'Made with shrimps, salman and smokee anchovies.', price = '$11.50',restaurant = myFirstRestaurant)
session.add(seafoodpizza)
session.commit()
#Check first object and get it name attribute
firstResult = session.query(Restaurant).first()
firstResult.name

'''How to update info in SQL Alchemy'''
#find entries
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print '\n'

UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 8).one()
print UrbanVeggieBurger.price
#Update price for instance
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger) # add to session
session.commit() # commit updated data
