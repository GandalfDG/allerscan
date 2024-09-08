from dotenv import load_dotenv
import os
import json
import requests
import yaml

load_dotenv()

api_endpoint = os.getenv("READ_API_ENDPOINT")
api_key = os.getenv("READ_API_KEY")

def read_api_request(image_url):
    query_params = {
        "api-version": "2023-04-01-preview",
        "features": "read"
    }

    request_body = json.dumps({
        "url": image_url
    })

    request_header = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json"
    }
    response = requests.post(api_endpoint + "computervision/imageanalysis:analyze", params=query_params, headers=request_header, data=request_body)

    return response

def load_allergens(yaml_path: str)-> dict:
    pass

def match_allergens(response: requests.Response):
    ingredients = response.json()
    text: str = ingredients["readResult"]["content"]
    ingredient_list = text.split(",")

    for ingredient in ingredient_list:
        pass
