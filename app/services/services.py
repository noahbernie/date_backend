# app/services/services.py
import os
from urllib.parse import urlparse
import time
import requests 
import urllib.request
from collections import Counter

TESTING_MODE = False
APITOKEN = 'uXfDEJnPDTFB/riggN9gZvhnmwaYtMTEV6e8Kce9cwjNKvIs/+CvGgN4agdwhqbJYaIjIHQsmXo=' # Your API Token

def get_image_results(image_file):
    if TESTING_MODE:
        print('****** TESTING MODE search, results are inacurate, and queue wait is long, but credits are NOT deducted ******')

    site='https://facecheck.id'
    headers = {'accept': 'application/json', 'Authorization': APITOKEN}
    files = {'images': open(image_file, 'rb'), 'id_search': None}
    response = requests.post(site+'/api/upload_pic', headers=headers, files=files).json()

    if response['error']:
        return f"{response['error']} ({response['code']})", None

    id_search = response['id_search']
    print(response['message'] + ' id_search='+id_search)
    json_data = {'id_search': id_search, 'with_progress': True, 'status_only': False, 'demo': TESTING_MODE}

    while True:
        response = requests.post(site+'/api/search', headers=headers, json=json_data).json()
        if response['error']:
            return f"{response['error']} ({response['code']})", None
        if response['output']:
            return None, response['output']['items']
        print(f'{response["message"]} progress: {response["progress"]}%')
        time.sleep(1)

def get_image_path():
    """
    Prompts the user for an image path or URL, validates it, and returns the value.
    Returns:
        str: A valid image path or URL.
    """
    while True:
        # Prompt user for input
        image_path = input("Please provide the image path or URL: ").strip()
        
        # Validate as URL
        if is_valid_url(image_path):
            print("Valid URL provided.")
            return image_path
        
        # Validate as file path
        elif os.path.isfile(image_path):
            print("Valid file path provided.")
            return image_path
        
        else:
            print("Invalid input. Please provide a valid image URL or file path.")

def filter_results(results):
    instagram_usernames = []
    linkedin_usernames = []
    twitter_usernames = []
    facebook_usernames = [] 
    # random_links = [] Need to finish

    for img in results:
        score_threshold = 70
        score = img['score']
        url = img['url']
        image_base64 = img['base64'] 

        if score > score_threshold and 'instagram.com' in url:
            # Extract the username from the URL
            print(url)
            username = url.split("instagram.com/")[1].split('/')[0]
            instagram_usernames.append(username)

        if score > score_threshold and 'linkedin.com/in/' in url:
            # Extract the username from the URL
            username = url.split("linkedin.com/in/")[1].split('/')[0]
            linkedin_usernames.append(username)

        if score > score_threshold and 'facebook.com/' in url:
            # Extract the username from the URL
            username = url.split("facebook.com/")[1].split('/')[0]
            facebook_usernames.append(username)

        if score > score_threshold and 'x.com/' in url:
            # Extract the username from the URL
            username = url.split("x.com/")[1].split('/')[0]
            twitter_usernames.append(username)

    return instagram_usernames, linkedin_usernames, twitter_usernames, facebook_usernames

def is_valid_url(url):
    """
    Validates if the input string is a well-formed URL.
    Args:
        url (str): The URL to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
