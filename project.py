#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project.py -- Python module for Restaurant Menu project.
# Server on Python based on Flask framework
# Used flask module DOCUMENTATION ## http://flask.pocoo.org/ ##
# Used sqlalchemy module to interact with database. DOCUMENTATION ## http://docs.sqlalchemy.org/en/latest ##
# master branch

#import framework
from flask import Flask, render_template, request, redirect, url_for, flash

'''Interaction with database'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
#Create engine and session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

'''Server'''

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New item successfully created!")
		return redirect(url_for(restaurantMenu, restaurant_id = restaurant_id))
    else:
    	return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	itemToEdit = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['newname']:
			itemToEdit.name = request.form['newname']
			session.add(itemToEdit)
			session.commit()
			flash("Menu item has been successfully edited!")
			return redirect(url_for(restaurantMenu, restaurant_id = restaurant_id))
    else:
    	return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = itemToEdit)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("Menu item has been successfully deleted!")
		return redirect(url_for(restaurantMenu, restaurant_id = restaurant_id))
    else:
    	return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = itemToDelete)





if __name__ == '__main__':
	app.secret_key = super_secret_key
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)