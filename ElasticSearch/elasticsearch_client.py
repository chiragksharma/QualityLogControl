from elasticsearch import Elasticsearch

es = Elasticsearch(
    [{'host': 'localhost', 'port': 9200, 'scheme': 'http'}],
    headers={"Content-Type": "application/json"}
)
def create_index(index_name):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

def index_log(index_name, log_entry):
    es.index(index=index_name, body=log_entry)