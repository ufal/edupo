#!/usr/bin/env python3
# coding: utf-8

import logging

from openai import OpenAI
from wolker_prompts import get_prompt


with open("apikey.txt") as infile:
    apikey = infile.read().strip()


logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

client = OpenAI(api_key=apikey)

MODEL = "gpt-5.6-sol"
DEFAULT_INSTRUCTIONS = "Jsi básník Jiří Wolker."
VECTOR_STORE_ID = 'vs_6a61231f72348191a9aeb53931c0ee4f'


def get_thread_messages(conversation_id):
    """Return text messages and roles in chronological order."""
    items = client.conversations.items.list(
        conversation_id=conversation_id,
        order="asc",
        limit=100,
    )

    result = []
    roles = []
    for item in items.data:
        if item.type != "message":
            continue
        if item.role not in ("user", "assistant"):
            continue

        text_parts = [
            content.text
            for content in item.content
            if content.type in ("input_text", "output_text")
        ]
        if text_parts:
            result.append("".join(text_parts))
            roles.append(item.role)

    return result, roles

REQUEST_BASE = {
    "model": MODEL,
    "tools": [
        {
            "type": "file_search",
            "vector_store_ids": [VECTOR_STORE_ID],
        }
    ],
    "tool_choice": {"type": "file_search"},
}

def talk_threaded(
    message="Napište báseň o přírodě ve městě.",
    typ="chat",
    conversation_id=None,
):
    if not conversation_id:
        conversation = client.conversations.create(
            items=[
                {
                    "type": "message",
                    "role": "developer",
                    "content": get_prompt(typ)
                }
            ])
        conversation_id = conversation.id

    request = {
        **REQUEST_BASE,
        "conversation": conversation_id,
        "input": message,
    }

    response = client.responses.create(**request)

    result, roles = get_thread_messages(conversation_id)
    return result, roles, conversation_id


def talk_simple(prompt, system_message=DEFAULT_INSTRUCTIONS):
    response = client.responses.create(
        model=MODEL,
        instructions=system_message,
        input=prompt,
        reasoning={"effort": "low"},
        max_output_tokens=5000,
    )
    return response.output_text


if __name__ == "__main__":
    while True:
        message = input()
        print("SIMPLE:")
        print(talk_simple(message))
        print("FULL:")
        result, _, _ = talk_threaded(message)
        print(result[-1])
