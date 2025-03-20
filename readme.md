# Geolocation Service

## Overview
This project provides a Unix socket-based service for retrieving a device's geolocation using Selenium and a local HTML file. The service maintains a socket at `/tmp/smx-glc-service.sock` that clients can connect to for requesting location data.

## Features
- Retrieves geolocation data (latitude, longitude, accuracy)
- Uses Selenium with headless Chrome to interact with a local HTML file
- Provides location data via Unix socket communication
- Caches location data for 10 seconds to reduce resource usage
- Handles JSON-based communication protocol

## Requirements
- Python 3.x
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
source venv/bin/activate # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

## Usage
1. Ensure you have Google Chrome installed and the appropriate ChromeDriver version.
2. Run the application:
```sh
python Main.py
```
3. The service will create a Unix socket at `/tmp/smx-glc-service.sock`
4. Connect to the socket and send a JSON request with the following format:
```json
{
  "type": "GET_LOCATION"
}
```

## Project Structure
```
├── controllers
│   ├── LocationController.py
├── services
│   ├── LocationService.py
├── template
│   ├── index.html
├── Main.py
├── requirements.txt
├── README.md
```

## Communication Protocol
- **Request Format**: 
```json
{
  "type": "GET_LOCATION"
}
```

- **Response Format**:
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

- **Error Response Format**:
```json
{
  "type": "error",
  "error": "ERROR_MESSAGE"
}
```

## Error Codes
- `UNKNOWN_CONTEXT`: Request type is not recognized
- `UNEXPECTED_FORMAT`: Request JSON does not contain the required fields
- `INVALID_JSON_FORMAT`: Request could not be parsed as valid JSON

## Logging
The application logs errors and status messages to help with debugging.

## License
This project is licensed under the MIT License. Feel free to modify and use it as needed.