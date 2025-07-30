import json

def pretty_print_json(data):
    print(json.dumps(data, indent=4))

def create_log_row(data):
    return json.dumps(data, indent=4)