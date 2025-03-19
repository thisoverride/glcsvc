from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class LocationController:
    def __init__(self, app, locationService):
        self.locationService = locationService
        self.register_routes(app)
        
    def register_routes(self, app):
        app.route('/device/position', methods=['GET'])(self.currentLocation)
        
    def currentLocation(self):
        try:
            geolocation_data = self.locationService.getLocation()
            return geolocation_data, 200
        except Exception as e:
            logger.error(f"Erreur lors du traitement de la requête: {str(e)}")
            return jsonify({
                "status": "error",
                "error": str(e)
            }), 500