import requests
import json
from datetime import datetime
URL = 'https://swapi.dev/api/films/'


#print(data)
class Swapi:

    def get_list(self, response):
        data = json.loads(response.text)
        data_list = []
        for data in data['results']:
            new_data = {}
            new_data['title'] = data['title']
            new_data['episode_id'] = data['episode_id']
            date_string = data['release_date']
            date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
            new_data['release_date'] = date_obj
            data_list.append(new_data)
        return data_list



