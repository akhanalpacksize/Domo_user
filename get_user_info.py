import json

import requests
from config.env import *
from utils import get_access_token
from get_user_id import get_domo_id

access_token = get_access_token()
domo_id = get_domo_id()


def get_user_data():
    domo_user_info = {}
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        # Construct the SQL query
        user_ids_string = ', '.join(map(str, domo_id))
        sql_query = f"SELECT * FROM `User ID` WHERE `User ID` IN ({user_ids_string})"

        payload = {
            "sql": sql_query,
        }
        response = requests.post(f'{BASE_URL}/datasets/query/execute/{DATASET_PULL}', headers=headers, json=payload)
        response_json = json.loads(response.text)['rows']

        for rows in response_json:
            user_id = rows[65]
            email = rows[54]
            p_department = rows[23]
            profile_organization = rows[21]
            department = rows[64]
            p_title = rows[14]
            title = rows[53]
            # manager_id = rows[78]

            if email not in ['qualityassurance.us@packsize.com', 'infosys.us@packsize.com']:
                domo_user_info[user_id] = {
                    'user_id': user_id,
                    'p_department': p_department if p_department else profile_organization,
                    'p_title': p_title,
                    'email': email,
                }
        return domo_user_info

    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred during the request: {e}"
        # logger.error(f"An error occurred during the request: {e}")
        # send_email_error(error_message)
    except KeyError as e:
        error_message = f"An error occurred while processing the response: {e}"
        # logger.error(f"An error occurred while processing the response: {e}")
        # send_email_error(error_message)
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        # logger.error(f"An unexpected error occurred: {e}")
        # send_email_error(error_message)
