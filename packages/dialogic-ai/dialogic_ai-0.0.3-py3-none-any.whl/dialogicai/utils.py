from datetime import datetime
import uuid


def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_uuid():
    # TODO: customize the uuid with prefix for both messages and thread conversations
    return str(uuid.uuid4())