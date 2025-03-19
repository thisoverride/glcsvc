# Geolocation Service

## Overview
This project provides a Flask-based API for retrieving a device's geolocation using Selenium and a local HTML file.

## Features
- Retrieves geolocation data (latitude, longitude, accuracy)
- Uses Selenium to interact with a local HTML file
- Provides a REST API endpoint for location retrieval

## Requirements
- Python 3.x
- Flask
- Selenium
- Google Chrome & ChromeDriver

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/glcsvc/geolocation-service.git
   cd geolocation-service
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
1. Ensure you have Google Chrome installed and the appropriate ChromeDriver version.
2. Run the application:
   ```sh
   python app.py
   ```
3. Access the geolocation API endpoint:
   ```
   GET /device/position
   ```

## Project Structure
```
├── controllers
│   ├── LocationController.py
├── services
│   ├── LocationService.py
├── template
│   ├── index.html
├── app.py
├── requirements.txt
├── README.md
```

## API Endpoints
- **GET /device/position**: Returns the current geolocation data in JSON format.

## Example Response
```json
{
  "timestamp": "2025-03-19T12:00:00Z",
  "geolocation": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "accuracy": 10
  }
}
```

## Logging
The application logs errors and status messages to help with debugging.

## License
This project is licensed under the MIT License. Feel free to modify and use it as needed.

