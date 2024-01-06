#!/usr/bin/env python3
#coding: utf-8

import sys

import logging
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
print(token)
client = WebClient(token=token)
logger = logging.getLogger(__name__)

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

channel_name = "edupo"
channel_id = get_channel_id(channel_name)
messages = get_messages(channel_id)

print(f"{len(messages)} messages in {channel_name}")

