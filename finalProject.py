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

CLIENT_ID = json.loads(open('clent_secrets.json', 'r').read())['web']['client_id']

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', title = 'LogIn')

@app.route('/gconnect', methods = ['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session('state'):
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content type'] = 'application json'
        return response
    # Obtain authorization code
    code = request.data

    try:
    # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope = '')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


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