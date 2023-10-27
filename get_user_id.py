import json
import pandas as pd

import requests
from config.env import BASE_URL, DATASET_PULL
from utils import get_access_token

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_row', None)  # Show all rows

pd.set_option('display.expand_frame_repr', False)

token = get_access_token()


def get_domo_id():
    domo_user_id = []
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "sql": "SELECT * FROM table",
        }
        response = requests.post(f'{BASE_URL}/datasets/query/execute/{DATASET_PULL}', headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception if the response status code is not successful

        response_json = json.loads(response.text)['rows']

        for row in response_json:
            user_id = row[65]
            email = row[54]
            title = row[53]
            department = row[64]
            manager = row[78]
            if email.endswith('@packsize.com') and (not title or not department):
                domo_user_id.append(user_id)
        return domo_user_id

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {str(e)}")


