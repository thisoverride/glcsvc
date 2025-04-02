import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import json
from services.LocationService import LocationService

class TestLocationService(unittest.TestCase):
    def setUp(self):
        # Mock the webdriver
        self.driver_patcher = patch('services.LocationService.webdriver')
        self.mock_webdriver = self.driver_patcher.start()
        
        # Setup mock driver instance
        self.mock_driver = MagicMock()
        self.mock_webdriver.Chrome.return_value = self.mock_driver
        
        # Create service instance
        self.location_service = LocationService()
        
    def tearDown(self):
        self.driver_patcher.stop()
        
    def test_init_creates_driver(self):
        """Test that the service initializes with a webdriver"""
        self.assertIsNotNone(self.location_service.driver)
        self.mock_webdriver.Chrome.assert_called_once()
        
    def test_get_location_cache(self):
        """Test that location is cached and returned if recent"""
        # Set up mock data
        test_location = {
            "timestamp": datetime.now(timezone.utc).isoformat(), # from datetime import timezone
            "geolocation": {
                "latitude": 12.34,
                "longitude": 56.78,
                "accuracy": 10
            }
        }
        
        # Set cached data
        self.location_service.last_location = json.dumps(test_location).encode('utf-8')
        self.location_service.last_fetch_time = datetime.now(timezone.utc) # from datetime import timezone
        
        # Get location
        result = self.location_service.getLocation()
        
        # Verify cache was used (page not refreshed)
        self.mock_driver.refresh.assert_not_called()
        self.assertEqual(result, self.location_service.last_location)
        
    def test_get_location_fresh(self):
        """Test getting a fresh location when cache is expired"""
        # Mock the element and its text
        mock_element = MagicMock()
        mock_element.text = json.dumps({
            "latitude": 12.34,
            "longitude": 56.78,
            "accuracy": 10
        })
        self.mock_driver.find_element.return_value = mock_element
        
        # Set expired cache
        self.location_service.last_fetch_time = datetime.now() - timedelta(seconds=11)
        
        # Get location
        result = self.location_service.getLocation()
        
        # Verify page was refreshed
        self.mock_driver.refresh.assert_called_once()
        
        # Parse and verify result
        result_data = json.loads(result.decode('utf-8'))
        self.assertEqual(result_data["geolocation"]["latitude"], 12.34)
        self.assertEqual(result_data["geolocation"]["longitude"], 56.78)
        self.assertEqual(result_data["geolocation"]["accuracy"], 10)
        
    def test_get_location_error(self):
        """Test error handling when getting location fails"""
        # Make driver.find_element raise an exception
        self.mock_driver.find_element.side_effect = Exception("Test error")
        
        # Get location
        result = self.location_service.getLocation()
        
        # Verify error response
        result_data = json.loads(result.decode('utf-8'))
        self.assertEqual(result_data["type"], "error")
        self.assertEqual(result_data["error"], "Test error")

if __name__ == '__main__':
    unittest.main()