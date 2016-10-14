#!/usr/bin/env python
# -*- coding: utf-8 -*-
# project.py -- Python module for Restaurant Menu project.
# Server on Python based on Flask framework
# Used flask module DOCUMENTATION ## http://flask.pocoo.org/ ##
# Used sqlalchemy module to interact with database. DOCUMENTATION ## http://docs.sqlalchemy.org/en/latest ##
# master branch

#imports
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask import session as login_session # to avoid confusion with DB session
import random, string
import httplib2
import json
import requests

# oAuth2 imports

from oauth2client.client import flow_from_client_secrets
from oauth2client.client import FlowExchangeError

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

#JSON request RESTful API

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    itemsToJSON = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in itemsToJSON])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def MenuItemJSON(restaurant_id, menu_id):
    itemToJSON = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItems=itemToJSON.serialize)

'''WEB SITE'''

# Login/Logout/Profile block
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', title = 'LogIn')


# Restaurant block
# Main page with list of all restaurants

@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants, title = 'Restaurants')

# Create route for newRestaurant function

@app.route('/restaurants/new/', methods = ['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		newRestaurant = Restaurant(name = request.form['name'], description = request.form['description'], logo_url = request.form['logo_url'])
		session.add(newRestaurant)
		session.commit()
		flash("New restaurant successfully created! Please add some items to menu!")
		return redirect(url_for('restaurants'))
	else:
		return render_template('newrestaurant.html', title = 'New restaurant')

# Create route for editRestaurant function

@app.route('/restaurants/<int:restaurant_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(restaurant_id):
	restaurantToEdit = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		if request.form['newname']:
			restaurantToEdit.name = request.form['newname']
		if request.form['description']:
			restaurantToEdit.description = request.form['description']
		if request.form['logo_url']:
			restaurantToEdit.logo_url = request.form['logo_url']
		session.add(restaurantToEdit)
		session.commit()
		flash("New item successfully edited!")
		return redirect(url_for('restaurants', restaurants = restaurants))
	else:
		return render_template('editrestaurant.html', restaurant_id=restaurant_id, restaurant = restaurantToEdit, title = 'Edit restaurant')

# Create route for deleteRestaurant function

@app.route('/restaurants/<int:restaurant_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == 'POST':
		session.delete(restaurantToDelete)
		session.commit()
		flash("New item successfully deleted!")
		return redirect(url_for('restaurants', restaurants = restaurants))
	else:
		return render_template('deleterestaurant.html', restaurant_id=restaurant_id, restaurant = restaurantToDelete, title = 'Delete restaurant')

# Menu block
# Main menu page

@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, restaurant_id = restaurant_id, items = items, title = restaurant.name)

# Create route for newMenuItem function

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New item successfully created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id, title = 'New menu item')

# Create route for editMenuItem function

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    itemToEdit = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        if request.form['newname']:
            itemToEdit.name = request.form['newname']
        if request.form['description']:
            itemToEdit.description = request.form['description']
        if request.form['price']:
            itemToEdit.price = request.form['price']
        if request.form['course']:
            itemToEdit.course = request.form['course']
        session.add(itemToEdit)
        session.commit()
        flash("Menu item has been successfully edited!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = itemToEdit, title = 'Edit menu item')

# Create a route for deleteMenuItem function

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu item has been successfully deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = itemToDelete, title = 'Delete menu item')






if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)