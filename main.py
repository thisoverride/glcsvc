from services.LocationService import LocationService
from controllers.LocationController import LocationController

class Main: 
  def __init__(self):
    LocationController(LocationService())

if __name__ == '__main__':
  Main()