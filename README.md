## Flask Logging and Elasticsearch Integration

This Flask project demonstrates how to implement logging functionalities, including asynchronous logging, and integrate Elasticsearch for log storage and retrieval. The project provides API endpoints for making requests, logging responses, searching logs, and inserting logs into Elasticsearch.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Docker Desktop (for Elasticsearch)
- Docker CLI

### Setup
## 1. Set up Elasticsearch
First, pull the Elasticsearch Docker image and run a container:
```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.10.1
docker run -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.1 
```
## 2. Run the Flask Application

Install the required Python dependencies:

```
pip install -r requirements.txt
```
Run the Flask application:

```
python app.py
```
## 3. Access the Application
Once the Flask application is running, you can access it via the streamlit app 
- The Streamlit application for interacting with the APIs is available at: https://qualitylogcontrol.streamlit.app
  
⚠️**NOTE**: Make sure the python app ise running and docker is running then only the streamlit app will work

## Usage APIs

The application provides the following APIs:

- **GET /test**: Sends a test request to https://reqres.in/api/users/ and returns the response status code and text.

- **GET /api1:** Sends a request to https://reqres.in/api/users/ and logs the response asynchronously using logger1.

- **POST /api2**: Sends a POST request to https://reqres.in/api/register with predefined data and logs the response asynchronously using logger2.

- **GET /api3:** Sends a request to https://reqres.in/api/users/2 and logs the response asynchronously using logger3.

**Elasticsearch Integration**
- **GET /search:** Allows searching through logs stored in Elasticsearch. You can specify query parameters like query text, log level, start time, and end time to filter logs.

- **POST /insert_logs:** Inserts predefined log entries from log files into Elasticsearch.

## Contributors
Chirag Sharma - Project Lead & Developer

## License
This project is licensed under the MIT License - see the LICENSE file for details.
