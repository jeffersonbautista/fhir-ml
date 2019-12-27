from datetime import datetime

DISABLE = False

def current_time():
    return str(datetime.now())

def error(message):
    print(current_time(), " ERROR: ", message ) if not DISABLE else ""

def info(message):
    print(current_time(), " INFO: ", message ) if not DISABLE else ""

def warning(message):
    print(current_time(), " WARNING: ", message ) if not DISABLE else ""