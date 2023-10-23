#This example uses a simple Python application use boto3 to check new data in dynamodb.
#If there is new data, it will send a http post request to a url with the data.
import openai
import boto3
import requests
import dotenv
import os
import sys
from datetime import datetime
import logging
import logging.config

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
# logging.basicConfig(level=logging.WARNING, filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

dotenv.load_dotenv()
if os.getenv('DEBUG') == 'True':
    logging.debug("Debug mode on")
    logging.getLogger().setLevel(logging.DEBUG)
    # log to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(console)



logging.debug("Environment variables loaded")

def main():
    # Get the service resource.
    logging.debug("Connecting to dynamodb")
    try:
        dynamodb = boto3.resource('dynamodb')
        table_input = dynamodb.Table(os.getenv('TABLE_INPUT'))
        table_output = dynamodb.Table(os.getenv('TABLE_OUTPUT'))
        logging.debug("Connected to dynamodb")
    except Exception as e:
        logging.error("Error connecting to dynamodb")
        logging.error(e)
        sys.exit(1)

    # Get the latest item from table_input (max timestamp)
    # print("Getting latest item from table_input")
    logging.debug("Getting latest item from table_input")
    try:
        response = table_input.scan()
        items = response['Items']
        last_item = max(items, key=lambda x: x['timestamp'])
        text = last_item['message_text']
        logging.debug("Last item: " + text + "")
    except Exception as e:
        logging.error("Error getting latest item from table_input")
        logging.error(e)
        sys.exit(1)
    # print("Last item: " + text + "")

    # if starts with RosaGary
    if text.startswith('RosaGary'):
        try:
            msg = text.split('RosaGary')[1].strip()
        except:
            logging.error("Error splitting message")
            sys.exit(0)
    else:
        # print("not RosaGary message, exiting")
        logging.warning(f"Not RosaGary message, message: {text}")
        sys.exit(0)
    response = table_output.get_item(
        Key={
            'UUID': last_item['UUID'],
            'timestamp': last_item['timestamp']
        }
    )
    if 'Item' in response:
        # print("Item already exists in table_output")
        logging.warning("Item already exists in table_output")
        sys.exit(0)
    # print("Message: " + msg + "")
    logging.debug("Message: " + msg + "")

    response_text = 'test' + msg

    # table_output.put_item(
    #     Item={
    #         'UUID': last_item['UUID'],
    #         'timestamp': last_item['timestamp'],
    #         'datetime': datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
    #         'member': 'Gary',
    #         'message': response_text,
    #         # 'reply_token': last_item['reply_token'],
    #         # empty for now
    #         'url': '',
    #     }
    # )    
    # sys.exit(0)

    # use openai to generate response
    # print("Using openai to generate response")
    logging.debug("Using openai to generate response")

    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "你是一位助手，請用台灣用語以正體中文回覆"
            },
            {
            "role": "user",
            "content": msg
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    # print("Response: " + response['choices'][0]['text'] + "")
    logging.debug("Response: " + str(response))
    try:
        response_text = response['choices'][0]['message']['content']
    except Exception as e:
        logging.error("Error getting response text")
        logging.error(e)
        sys.exit(1)
    # put to dynamodb
    # print("Putting item to table_output")
    logging.debug("Putting item to table_output")
    # check if item already exists
    table_output.put_item(
        Item={
            'UUID': last_item['UUID'],
            'timestamp': last_item['timestamp'],
            'datetime': datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
            'member': 'Gary',
            'message': response_text,
            # 'reply_token': last_item['reply_token'],
            # empty for now
            'url': '',
        }
    )
    # print("Item put to table_output")
    logging.debug("Item put to table_output")


    # # send post request to url
    # print("Sending post request to url")
    # url = "https://notify-api.line.me/api/notify"
    # token = os.getenv('LINE_NOTIFY_TOKEN')
    # r = requests.post(
    #     url,
    #     headers={'Authorization': 'Bearer ' + token},
    #     data={'message': text}
    # )
    # if r.status_code == 200:
    #     print("Post request sent")

    # else:
    #     print("Error sending post request")

if __name__ == '__main__':
    main()