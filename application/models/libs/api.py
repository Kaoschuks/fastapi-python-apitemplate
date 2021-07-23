from application.models.core import req
import datetime
from functools import wraps

def curl(config, payload):
    response = req.request(config['method'], config['url'], headers=config['headers'], data = payload)
    return response.json()
