#This example uses a simple Python application use boto3 to check new data in dynamodb.
#If there is new data, it will send a http post request to a url with the data.

import boto3
import requests
import dotenv
import os
import sys

if __name__ == '__main__':

    print("Loading environment variables from .env file\n")

    dotenv.load_dotenv()
    
    print("Environment variables loaded\n")

    # Get the service resource.
    print("Connecting to dynamodb\n")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv('TABLE_NAME'))
    print("Connected to dynamodb\n")

    # Get the last item in the table
    print("Getting last item from table\n")
    response = table.scan()
    items = response['Items']
    last_item = items[-1]
    text = last_item['message_text']
    print("Last item: " + text + "\n")

    # send post request to url
    print("Sending post request to url\n")
    url = "https://notify-api.line.me/api/notify"
    token = os.getenv('LINE_NOTIFY_TOKEN')
    r = requests.post(
        url,
        headers={'Authorization': 'Bearer ' + token},
        data={'message': text}
    )
    if r.status_code == 200:
        print("Post request sent\n")

    else:
        print("Error sending post request\n")
