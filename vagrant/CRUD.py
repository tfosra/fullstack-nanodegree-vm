from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class RestaurantHandler():

    def getall(self):
        print("Getting all restaurants")
        return session.query(Restaurant).all()
    
    def get(self, id):
        return session.query(Restaurant).filter_by(id = id).one() 
    
    def delete(self, id):
        restaurant = session.query(Restaurant).filter_by(id = id).one()
        session.delete(restaurant)
        session.commit()
    
    def create(self, restaurant):
        session.add(restaurant)
        session.commit()
        return restaurant
    
    def update(self, restaurant):
        session.add(restaurant)
        session.commit()
        