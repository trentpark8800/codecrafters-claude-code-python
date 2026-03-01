import argparse
import os
import sys
from typing import Dict, List, Tuple
from dotenv import load_dotenv

from openai import OpenAI
from openai.types import Completion, CompletionChoice

from utils.tools import tool_map, Tools, read_file

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def _message_handler(choice: CompletionChoice) -> Dict:

    message = {
        "role": choice.message.role,
        "content": choice.message.content,
        "tool_calls": [],
    }

    if choice.message.tool_calls:
        for call in choice.message.tool_calls:
            message["tool_calls"].append(
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments,
                    },
                }
            )

    return message


def _tool_call_handler(tool_calls) -> List[Dict]:

    tool_responses: List[Dict] = []
    for call in tool_calls:
        tool_function: callable = tool_map(call.function.name)
        tool_result = tool_function(**eval(call.function.arguments))

        tool_responses.append({"role": "tool", "tool_call_id": call.id, "content": tool_result})

    return tool_responses


def parse_response(choices) -> Tuple[str, List[Dict]]:

    tool_calls = choices[0].message.tool_calls
    finish_reason = choices[0].finish_reason
    responses: List[Dict] = []
    responses.append(_message_handler(choices[0]))

    if tool_calls:
        responses.extend(_tool_call_handler(tool_calls))

    return finish_reason, responses


def agent_loop(client: OpenAI, prompt: str):

    execute_loop = True
    initial_message: Dict = {"role": "user", "content": prompt}
    messages: List[Dict] = [initial_message]

    while execute_loop:

        chat: Completion = client.chat.completions.create(
            model="anthropic/claude-haiku-4.5", messages=messages, tools=[Tools.READ.value]
        )

        choices: List[CompletionChoice] = chat.choices

        if not choices or len(choices) == 0:
            raise RuntimeError("no choices in response")

        finish_reason, responses = parse_response(choices)

        messages.extend(responses)
        if finish_reason == "stop":
            execute_loop = False

    return messages


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    load_dotenv()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    result_messages: List[Dict] = agent_loop(client, args.p)

    print(result_messages[-1]["content"])


if __name__ == "__main__":
    main()
