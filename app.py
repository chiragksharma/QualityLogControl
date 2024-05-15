from flask import Flask,jsonify,request
import logging
import os
import json
import requests
from datetime import datetime
from resources.logging_blueprint import logging_bp, logger1, logger2, logger3, log_response
from ElasticSearch.elasticsearch_client import es,create_index,index_log


app = Flask(__name__)
app.register_blueprint(logging_bp)

create_index("logs")


@app.get('/test')
def test_connection():
    response = requests.get("https://reqres.in/api/users/")
    return jsonify({
        "status_code": response.status_code,
        "text": response.text
    })

@app.get('/api1')
def get_api1():
    response = requests.get("https://reqres.in/api/users/")
    log_response(logger1, response)
    if response.status_code != 200:
        return jsonify({"error": "Failed to get valid response from the server"}), response.status_code
    
    return jsonify(response.json())
    

@app.post('/api2')
def post_api2():
    data={
    "email": "eve.holt@reqres.in",
    "password": "pistol"
    }
    response = requests.post("https://reqres.in/api/register",data=data)
    log_response(logger2, response)
    if response.status_code != 200:
        return jsonify({"error": "Failed to get valid response from the server"}), response.status_code
    
    return jsonify(response.json())

@app.route('/api3')
def get_api3():
    response = requests.get("https://reqres.in/api/users/2")
    log_response(logger3, response)
    if response.status_code != 200:
        return jsonify({"error": "Failed to get valid response from the server"}), response.status_code
    
    return jsonify(response.json())

@app.route('/search', methods=['GET'])
def search_logs():

    # Define a basic Elasticsearch query that matches all documents
    # Get query parameters
    query = request.args.get('query', '')
    level = request.args.get('level', '')
    start_time = request.args.get('start_time', '')
    end_time = request.args.get('end_time', '')

    # Construct the Elasticsearch query
    es_query = {
        "query": {
            "bool": {
                "must": [],
                "filter": [],
            }
        }
    }

    # Add full-text search query
    if query:
        es_query["query"]["bool"]["must"].append({
            "bool": {
                "should": [
                    {"match_phrase": {"log_message": query}},
                    {"match_phrase": {"log_string": query}}
                ]
            }
        })

    # Add level filter
    if level:
        es_query["query"]["bool"]["filter"].append({
            "term": {
                "level": level
            }
        })

    # Add timestamp range filter
    if start_time and end_time:
        es_query["query"]["bool"]["filter"].append({
            "range": {
                "timestamp": {
                    "gte": start_time,
                    "lte": end_time
                }
            }
        })


    try:
        # Execute the search query on the "logs" index
        response = es.search(index="logs", body=es_query)
        # Return the search results as a JSON response
        return jsonify(response['hits']['hits'])
    except Exception as e:
        # Return an error message if the search fails
        return jsonify({"error": str(e)}), 500


def parse_log_line(line):
    """
    Parse a single log line to extract the JSON part.
    """
    try:
        log_entry = line.split('INFO ')[1]
        log_entry = log_entry.replace("'", '"')
        return json.loads(log_entry)
    except (IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing line: {line}")
        print(f"Exception: {e}")
        return None

def insert_log_to_es(index_name, log_data):
    """
    Insert a single log entry into Elasticsearch.
    """
    try:
        index_log(index_name, log_data)
    except Exception as e:
        print(f"Error inserting log to Elasticsearch: {log_data}")
        print(f"Exception: {e}")
        if hasattr(e, 'info'):
            print(f"Elasticsearch error info: {e.info}")

def process_log_file(index_name, file_path):
    """
    Process a single log file and insert its entries into Elasticsearch.
    """
    with open(file_path, 'r') as file:
        for line in file:
            log_data = parse_log_line(line)
            if log_data:
                insert_log_to_es(index_name, log_data)

def process_log_files(index_name, log_files):
    """
    Process multiple log files.
    """
    for file_path in log_files:
        if os.path.exists(file_path):
            print(f"Processing file: {file_path}")
            process_log_file(index_name, file_path)
        else:
            print(f"File not found: {file_path}")

@app.route('/insert_logs', methods=['POST'])
def insert_logs():
    log_files = ['log1.log', 'log2.log', 'log3.log']
    process_log_files('logs', log_files)
    return jsonify({"message": "Logs inserted successfully."})


if __name__ == "__main__":    
    app.run(debug=True)
