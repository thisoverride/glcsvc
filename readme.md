# Geolocation Service with Unix Socket Interface

This project provides a reliable geolocation service that retrieves user location data through a browser-based approach and exposes it via a Unix domain socket interface. It combines Selenium WebDriver automation with socket-based IPC to deliver accurate geolocation information to local system components.

The service uses Chrome in headless mode to access the browser's Geolocation API, providing high-accuracy location data including latitude, longitude, and accuracy metrics. It implements intelligent caching to minimize resource usage while maintaining data freshness, and exposes a robust Unix socket interface with proper error handling and validation. The service is designed for integration with local system components that require reliable geolocation data.

## Repository Structure
```
.
├── controllers/
│   └── LocationController.py     # Handles Unix socket communication and request validation
├── services/
│   └── LocationService.py        # Core geolocation functionality using Selenium WebDriver
├── template/
│   └── index.html               # HTML template for browser geolocation access
├── tests/
│   ├── __init__.py             # Python package marker for tests
│   └── test_location_service.py # Unit tests for LocationService
├── main.py                      # Application entry point
└── requirements.txt             # Python package dependencies
```

## Usage Instructions
### Prerequisites
- Python 3.6 or higher
- Chrome browser installed
- Unix-like operating system (Linux/MacOS) for Unix socket support
- The following Python packages:
  - selenium==4.30.0
  - webdriver_manager==4.0.2

### Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/MacOS
# or
.venv\Scripts\activate     # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Quick Start
1. Start the geolocation service:
```bash
python main.py
```

2. The service will create a Unix socket at `/tmp/sme-glcsvc.sock`

3. Connect to the service using a Unix socket client:
```python
import socket
import json

client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect('/tmp/sme-glcsvc.sock')

request = {
    "source": "CTL_LOCAL_SYS",
    "version": 1.0,
    "request": {
        "type": "GET_LOC"
    }
}

client.send(json.dumps(request).encode('utf-8'))
response = client.recv(1024)
print(json.loads(response.decode('utf-8')))
```

### More Detailed Examples
Example response format:
```json
{
    "location": {
        "timestamp": "2023-09-20T14:30:00.123456",
        "geolocation": {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "accuracy": 10
        }
    }
}
```

### Troubleshooting
Common issues and solutions:

1. Socket file already exists:
   - Error: `RuntimeError: The socket file /tmp/sme-glcsvc.sock already exists`
   - Solution: Remove the existing socket file:
     ```bash
     rm /tmp/sme-glcsvc.sock
     ```

2. Chrome driver issues:
   - Error: `WebDriver not initialized`
   - Solution: Ensure Chrome is installed and up to date:
     ```bash
     # On Ubuntu/Debian
     sudo apt update && sudo apt install google-chrome-stable
     ```

3. Permission issues:
   - Error: `Permission denied: '/tmp/sme-glcsvc.sock'`
   - Solution: Check socket file permissions:
     ```bash
     sudo chmod 777 /tmp/sme-glcsvc.sock
     ```

## Data Flow
The service uses a browser-based approach to access the Geolocation API, processes the data through Selenium WebDriver, and serves it via a Unix domain socket.

```ascii
[Browser Geolocation API] -> [Selenium WebDriver] -> [LocationService]
           |                                                |
           v                                                v
    [HTML Template]                                 [Location Cache]
           |                                                |
           |                                                v
           +-------------> [LocationController] <-----------+
                                   |
                                   v
                         [Unix Domain Socket]
                                   |
                                   v
                         [Client Applications]
```

Component interactions:
1. LocationService initializes Chrome in headless mode with Selenium WebDriver
2. HTML template accesses browser's Geolocation API
3. LocationService caches location data for 10 seconds
4. LocationController validates incoming socket requests
5. Valid requests trigger location retrieval from LocationService
6. Location data is returned to clients in JSON format
7. Error responses include specific error types and messages