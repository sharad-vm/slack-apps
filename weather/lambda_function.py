import json
import time
import re

from urllib.request import urlopen
from urllib.parse import urlencode, parse_qs, parse_qsl
from slackclient import SlackClient

# instantiate user's location
url = 'http://ipinfo.io/json'
urlresponse = urlopen(url)
data = json.load(urlresponse)
defaultzipcode = data['postal']


def get_weather(command_text):
    """
	Finds the weather of the user's location or other location(s) requested
    """
        
    #zipcode = defaultzipcode if len(zipcode) == 0 else zipcode
    command_text = "'" + command_text +"'"
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select location, item from weather.forecast where woeid in (select woeid from geo.places(1) where text = " + command_text+ ")"
    yql_url = baseurl + urlencode({'q':yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    ch = data['query']['results']['channel']
    response = """Current conditions for %s,%s: %s and %s
    High - %s; Low - %s""" %(ch['location']['city'],ch['location']['region'], ch['item']['condition']['temp'], ch['item']['condition']['text'], ch['item']['forecast'][0]['high'], ch['item']['forecast'][0]['low'])
    
    return response

            

def lambda_handler(event, context):
    # TODO implement
    params = parse_qs(event['body'])
    command = params['command'][0]
    channel = params['channel_name'][0]
    command_text = params.get('text', [None])[0]
    
    if command_text:
        weather = get_weather(command_text)
    else:
        weather = """Please provide a valid city or postalcode.
        Ex: /weather New York"""
    return {
        "statusCode": 200,
        "body": weather
    }
