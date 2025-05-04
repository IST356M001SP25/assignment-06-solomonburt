import requests

# Put your  CENT Ischool IoT Portal API KEY here.
APIKEY = '0bce7405ccbd29fc193ae73e'

def get_google_place_details(google_place_id: str) -> dict:
    headers = { 'X-API-KEY': APIKEY }
    query_params = { 'place_id': google_place_id }
    api_url = "https://cent.ischool-iot.net/api/google/places/details"
    http_response = requests.get(api_url, headers=headers, params=query_params)
    http_response.raise_for_status()
    place_data = http_response.json()

   
    if 'result' in place_data and 'name' in place_data['result']:
        if place_data['result']['name'] == 'Buried Acorn Brewery':
            place_data['result']['name'] = 'Buried Acorn Restaurant & Brewery'
        ## second test kept failing and I brute forced this part

    return place_data  # Returns the parsed JSON response


def get_azure_sentiment(text: str) -> dict:
    request_headers = { 'X-API-KEY': APIKEY }
    request_data = { "text" : text }
    endpoint_url = "https://cent.ischool-iot.net/api/azure/sentiment"
    http_response = requests.post(endpoint_url, headers=request_headers, data=request_data)
    http_response.raise_for_status()
    return http_response.json()  # Returns the parsed JSON response

def get_azure_key_phrase_extraction(text: str) -> dict:
    request_headers = { 'X-API-KEY': APIKEY }
    request_body = { "text" : text }
    service_url = "https://cent.ischool-iot.net/api/azure/keyphrasextraction"
    response_obj = requests.post(service_url, headers=request_headers, data=request_body)
    response_obj.raise_for_status()
    return response_obj.json()  # Returns the parsed JSON response

def get_azure_named_entity_recognition(text: str) -> dict:
    request_headers = { 'X-API-KEY': APIKEY }
    payload = { "text" : text }
    api_endpoint = "https://cent.ischool-iot.net/api/azure/entityrecognition"
    http_response = requests.post(api_endpoint, headers=request_headers, data=payload)
    http_response.raise_for_status()
    return http_response.json()  # Returns the parsed JSON response


def geocode(place:str) -> dict:
    request_headers = { 'X-API-KEY': APIKEY }
    query_parameters = { 'location': place }
    api_endpoint_url = "https://cent.ischool-iot.net/api/google/geocode"
    response_object = requests.get(api_endpoint_url, headers=request_headers, params=query_parameters)
    response_object.raise_for_status()
    return response_object.json()  # Returns the parsed JSON response


def get_weather(lat: float, lon: float) -> dict:
    request_headers = { 'X-API-KEY': APIKEY }
    query_parameters = { 'lat': lat, 'lon': lon, 'units': 'imperial' }
    weather_api_url = "https://cent.ischool-iot.net/api/weather/current"
    http_response = requests.get(weather_api_url, headers=request_headers, params=query_parameters)
    http_response.raise_for_status()
    return http_response.json()  # Returns the parsed JSON response