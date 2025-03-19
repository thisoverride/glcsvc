import os
from flask import Flask
from services.LocationService import LocationService
from controllers.LocationController import LocationController

app = Flask(__name__)

location_service = LocationService()
location_controller = LocationController(app, location_service)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)