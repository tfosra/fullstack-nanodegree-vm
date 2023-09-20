from flask import Flask
from database_setup import Restaurant, MenuItem
from CRUD import RestaurantHandler, MenuItemHandler

rh = RestaurantHandler()
mh = MenuItemHandler()

app = Flask(__name__)

@app.route('/')
@app.route('/menus')
def helloWorld():
    restaurant = rh.get(2)
    menuitems = mh.getbyrestaurant(restaurant)
    output = ""
    output += "<h2>%s</h2>"%restaurant.name
    output += "<ul>"
    for m in menuitems:
        output += "<li>%s (%s)</li>"%(m.name, m.price)
    output += "</ul>"
    return output

if __name__ == '__main__':
    app.debug = True
    app.run(host= '0.0.0.0', port=5000)