from flask import Flask, render_template
from database_setup import Restaurant, MenuItem
from CRUD import RestaurantHandler, MenuItemHandler

rh = RestaurantHandler()
mh = MenuItemHandler()

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants')
def listRestaurant():
    restaurants = rh.getall()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/create')
def createRestaurant():
    output = "<a href='/restaurants'>< Back to restaurants</a>"
    
    output += "<h2>Create a new restaurant</h2>"
    output += "<form method = 'POST' enctype = 'multipart/form-data' action='/restaurants/create'>"
    output += "<input name='name' type='text' placeholder = 'Name'>"
    output += "<input type='submit' value='Create'></form>"
    output += "</body></html>"
    return output

@app.route('/restaurants/<int:restaurant_id>/view')
def viewRestaurant(restaurant_id):
    restaurant = rh.get(restaurant_id)
    output = "<a href='/restaurants'>< Back to restaurants</a>"
    output += "<h2>%s</h2>" % restaurant.name
    output += "<a href ='/restaurants/%d/edit'>Edit</a> | " % restaurant.id
    output += "<a href ='/restaurants/%d/delete'>Delete</a> | " % restaurant.id
    output += "<a href='/restaurants/%d/create'>Create a new menu</a>" % restaurant.id
    output += "<h2>List of menus of the restaurant</h2>"

    menus = mh.getbyrestaurant(restaurant_id)
    for m in menus:
        output += "<strong>%s</strong><br/>" % m.name
        output += "%s<br/>" % m.course
        output += "%s<br/>" % m.description
        output += "%s<br/>" % m.price
        output += "<a href ='/restaurants/%d/%d/edit'>Edit</a> |" % (restaurant.id, m.id)
        output += "<a href ='/restaurants/%d/%d/delete'>Delete</a>" % (restaurant.id, m.id)
        output += "<br/></br>"
    return output

@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    restaurant = rh.get(restaurant_id)
    output = "<a href='/restaurants'>< Back to restaurants</a>"
    output += "<h2>%s</h2>" % restaurant.name
    
    output += "<form method = 'POST' enctype = 'multipart/form-data' action='/restaurants/%d/edit'>"%restaurant.id
    output += "<input name='name' type='text' placeholder = 'Name' value='%s'>"%restaurant.name
    output += "<input type='submit' value='Update'></form>"
    return output

@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    restaurant = rh.get(restaurant_id)
    output = "<a href='/restaurants'>< Back to restaurants</a>"
    output += "<h2>%s</h2>" % restaurant.name
    
    output += "<h2>Do you really want to delete '%s' ?</h2>"%restaurant.name
    output += "<form method = 'POST' enctype = 'multipart/form-data' action='/restaurants/%d/delete'>"%restaurant.id
    output += "<input type='submit' value='Delete'></form>"
    return output

@app.route('/restaurants/<int:restaurant_id>/create')
def createMenu(restaurant_id):
    restaurant = rh.get(restaurant_id)
    output = ""
    output += "<a href='/restaurants'>< Back to restaurants</a> < "
    output += "<a href='/restaurants/%d/view'>< Back to menus</a>" % restaurant.id
    output += "<h2>%s</h2>" % restaurant.name
    
    output += "<h2>Create a new menu</h2>"
    output += "<form method = 'POST' enctype = 'multipart/form-data' action='/restaurants/create'>"
    output += "<input name='name' type='text' placeholder = 'Name'></br>"
    output += "<input name='course' type='text' placeholder = 'Course'></br>"
    output += "<input name='price' type='text' placeholder = 'Price'></br>"
    output += "<textarea name='description' placeholder = 'Description'></textarea></br>"
    output += "<input type='submit' value='Create menu'></form>"
    return output

@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/edit')
def editMenu(restaurant_id, menuitem_id):
    restaurant = rh.get(restaurant_id)
    menuitem = mh.get(menuitem_id)
    output = ""
    output += "<a href='/restaurants'>< Back to restaurants</a> < "
    output += "<a href='/restaurants/%d/view'>< Back to menus</a>" % restaurant.id
    output += "<h2>%s</h2>" % restaurant.name
    output += "<h3>%s</h3>" % menuitem.name
    
    output += "<form method = 'POST' enctype = 'multipart/form-data' action='/restaurants/%d/%d/create'>" % (restaurant.id, menuitem.id)
    output += "<input name='name' type='text' placeholder = 'Name' value='%s'></br>" % menuitem.name
    output += "<input name='name' type='text' placeholder = 'Course' value='%s'></br>" % menuitem.course
    output += "<input name='price' type='text' placeholder = 'Price' value='%s'></br>" % menuitem.price
    output += "<textarea name='description' placeholder = 'Description'>%s</textarea></br>" % menuitem.description
    output += "<input type='submit' value='Update menu'></form>"
    return output

@app.route('/restaurants/<int:restaurant_id>/<int:menuitem_id>/delete')
def deleteMenu(restaurant_id, menuitem_id):
    restaurant = rh.get(restaurant_id)
    menuitem = mh.get(menuitem_id)
    output = ""
    output += "<a href='/restaurants'>< Back to restaurants</a> < "
    output += "<a href='/restaurants/%d/view'>< Back to menus</a>" % restaurant.id
    
    output += "<h2>Do you really want to delete the menu '%s' of '%s' ?</h2>" % (menuitem.name, restaurant.name)
    output += "<form method = 'POST' enctype = 'multipart/form-data' action='/restaurants/%d/%d/delete'>" % (menuitem.id, restaurant.id)
    output += "<input type='submit' value='Delete'></form>"
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host= '0.0.0.0', port=5000)