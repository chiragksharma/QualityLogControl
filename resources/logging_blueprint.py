from flask import Blueprint
import logging
from datetime import datetime
import json
import os
from concurrent.futures import ThreadPoolExecutor
from ElasticSearch.elasticsearch_client import create_index, index_log


logging_bp = Blueprint('logging_bp', __name__)

# ThreadPoolExecutor for asynchronous logging
executor = ThreadPoolExecutor(max_workers=5)

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Load logging configuration
with open('resources/logging_config.json') as config_file:
    config = json.load(config_file)

# Create loggers based on configuration
loggers = {}
for logger_name, logger_config in config['loggers'].items():
    loggers[logger_name] = setup_logger(
        logger_name,
        logger_config['file'],
        getattr(logging, logger_config['level'].upper(), logging.INFO)
    )

logger1 = loggers['logger1']
logger2 = loggers['logger2']
logger3 = loggers['logger3']

def log_response(logger, response):
    try:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "level": "success" if response.ok else "error",
            "source": logger.name,
            "log_message": "API Response",
            "status_code": response.status_code,
            "response_text": response.text
        }
        # Asynchronous logging
        executor.submit(logger.info, json.dumps(log_entry))
    except Exception as e:
        # Handle logging error, e.g., log to a fallback logger or print to console
        print(f"Logging error: {e}")