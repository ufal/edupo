#!/usr/bin/env python3
#coding: utf-8

print("Content-Type: text/html; charset=utf-8")
print()

import sys
import time
import logging
from collections import defaultdict
logging.basicConfig(
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=token)
logger = logging.getLogger(__name__)

def Unk():
    return "(unknown user)"

def get_users():
    try:
        users = client.users_list()
        result = defaultdict(Unk)
        for user in users["members"]:
            result[user["id"]] = user["name"]
        return result
    except SlackApiError as e:
        print(f"Error: {e}")
        return None
        
def get_channel_id(channel_name):
    try:
        # Call the conversations.list method using the WebClient
        for result in client.conversations_list(types="private_channel"):
            for channel in result["channels"]:
                if channel["name"] == channel_name:
                    return channel["id"]
    except SlackApiError as e:
        print(f"Error: {e}")
        return None

def get_messages(channel_id):

    try:
        # Call the conversations.history method using the WebClient
        # conversations.history returns the first 100 messages by default
        # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
        return client.conversations_history(channel=channel_id)["messages"]
    except SlackApiError as e:
        print(f"Error: {e}")
        return None

def replace_user_ids(text, users):
    for user_id, user_name in users.items():
        text = text.replace(user_id, user_name)
    return text

def get_message_texts(messages):
    result = list()
    for i, message in enumerate(messages[::-1]):
        if 'subtype' in message:
            header = f"{message['type']} {message['subtype']}"
        else:
            header = f"{message['type']} by {users[message['user']]}"
        t = time.localtime(int(message['ts'].split('.')[0]))
        ts = time.strftime("%A %d.%m.%Y %H:%M:%S", t)
        print(f"=== {i}. {header} at {ts} ===")
        text = replace_user_ids(message["text"], users)
        print(text)
        print()
    return result

def get_message_tuples(messages):
    # TODO emails sent here have empty text
    result = list()
    for message in messages[::-1]:
        if 'subtype' in message:
            author = message['subtype']
        else:
            author = users[message['user']]
        t = time.localtime(int(message['ts'].split('.')[0]))
        ts = time.strftime("%A %d.%m.%Y %H:%M:%S", t)
        text = replace_user_ids(message["text"], users)
        result.append( (author, ts, text) )
    return result


channel_name = "edupo"
channel_id = get_channel_id(channel_name)
messages = get_messages(channel_id)
users = get_users()
mt = get_message_tuples(messages)

css = """
<style>
pre {
    white-space: pre-wrap;
}
</style>
"""

print(f"<html><head><title>EduPo Slack Channel</title>{css}</head><body>")
for author, ts, text in mt:
    print(f"""<fieldset>
        <legend>{ts} <b>{author}</b></legend>
        <pre>{text}</pre>
    </fieldset>
    """)
print("</body></html>")
