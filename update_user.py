import json
import requests
from config.env import SESSION_TOKEN

from get_user_info import get_user_data
from utils import get_local_access_token, get_access_token

# token = SESSION_TOKEN

#Local instance Access token (instance is broken)
# access_token = get_local_access_token()

#Prod Instance access token
access_token = get_access_token()

user_data = get_user_data()
#Local instance Session_token for undoc api's
# session_token = '5596df7a0b659f339daf847eec120c6c61ef968257824344'


def update_data():
    # THIS URL BREAKS THE INSTANCE WHEN THE PAYLOADS IS Department and userTitle
    # url = 'https://ayush-dev-761592.domo.com/api/content/v2/users/684329826/profiles'


    header = {
        "Authorization": f"Bearer {access_token}",
        # 'x-domo-developer-token': session_token,
        "Content-Type": "application/json"
    }

    for user_id, data in user_data.items():
        p_department = data['p_department']
        p_title = data['p_title']
        email = data['email']
        id = user_id

        payload = {
            'email': email,
            'department': p_department,
            'title': p_title
        }

        # USE THIS API TO UPDATE THE USER'S value
        url = f'https://api.domo.com/v1/users/{id}'

        print(payload)


        # uncomment the below code to run Update code

        # try:
        #     response = requests.put(url, headers=header, json=payload)
        #     if response.status_code == 200:
        #         print(f"Profile for user {id} updated successfully.")
        #     elif response.status_code == 401:
        #         print(f"Unauthorized: Check your token and permissions for user {id}.")
        #     elif response.status_code == 404:
        #         print(f"Resource not found: Check the URL for user {id}.")
        #     else:
        #         print(f"Failed to update profile for user {id}. Status code: {response.status_code}")
        #         print(response.text)  # Log the response content for debugging
        # except requests.exceptions.RequestException as e:
        #     print(f"Request error for user {id}: {str(e)}")

update_data()
