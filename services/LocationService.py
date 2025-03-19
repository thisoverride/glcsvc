from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

class LocationService:
    def getLocation(self):
        driver = None
        try:
            chrome_options = Options()
            # chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=300,300")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.geolocation": 1
            })
            
            driver = webdriver.Chrome(options=chrome_options)
            logger.info("Navigateur Chrome initialisé en mode headless")
            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            html_path = os.path.join(script_dir, "..", "template", "index.html")
            file_url = f"file:///{html_path.replace(os.sep, '/')}"
            
            driver.get(file_url)
            logger.info(f"Fichier HTML chargé: {file_url}")
            
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#geolocResult[data-ready='true']"))
            )
            
            geoloc_result = driver.find_element(By.ID, "geolocResult").text
            geoloc_data = json.loads(geoloc_result)


            response_data = {
                "timestamp": datetime.now().isoformat(),
                "geolocation": {
                    "latitude": geoloc_data["latitude"],
                    "longitude": geoloc_data["longitude"],
                    "accuracy": geoloc_data["accuracy"]
                }
            }
            
            return response_data
            
        except Exception as e:
            logger.error(f"Error retrieving geolocation: {str(e)}")
            if driver:
                driver.quit()
            return {"status": "error", "error": str(e)}