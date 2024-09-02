import os
import json
from tineye_python.tineye_python import TinEyeAPIRequest

tineye_api = TinEyeAPIRequest()
image = 'https://upload.wikimedia.org/wikipedia/commons/b/bf/Golden_Gate_Bridge_as_seen_from_Battery_East.jpg'
response = tineye_api.search_data(image, save_to_file='output.json')
