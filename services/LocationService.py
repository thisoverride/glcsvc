from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class LocationService:
    def __init__(self):
        self.last_location = None
        self.last_fetch_time = None
        self.driver = self._init_driver()
        self._load_html_page()

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new") 
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=300,300")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.geolocation": 1
        })

        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def _load_html_page(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(script_dir, "..", "template", "index.html")
        file_url = f"file:///{html_path.replace(os.sep, '/')}"
        self.driver.get(file_url)

    def _refresh_page(self):
        self.driver.refresh()

    def getLocation(self):
        if self.last_location and self.last_fetch_time:
            if datetime.now() - self.last_fetch_time < timedelta(seconds=10):
                return self.last_location  

        self._refresh_page()

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#geolocResult[data-ready='true']"))
            )

            geoloc_result = self.driver.find_element(By.ID, "geolocResult").text
            geoloc_data = json.loads(geoloc_result)

            response_data = {
                "timestamp": datetime.now().isoformat(),
                "geolocation": {
                    "latitude": geoloc_data["latitude"],
                    "longitude": geoloc_data["longitude"],
                    "accuracy": geoloc_data["accuracy"]
                }
            }

            self.last_location = json.dumps(response_data).encode('utf-8')
            self.last_fetch_time = datetime.now()

            return self.last_location

        except Exception as e:
            logger.error(f"Error retrieving geolocation: {str(e)}")
            return json.dumps({
                "type": "error",
                "error": str(e)
            }).encode('utf-8')

    def close(self):
        if self.driver:
            self.driver.quit()
