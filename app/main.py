import argparse
import os
import sys
from dotenv import load_dotenv

from openai import OpenAI

from utils.tools import tool_map, Tools, read_file

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def _tool_call_handler(tool_calls):

    for call in tool_calls:
        tool_function: callable = tool_map(call.function.name)
        tool_function(**eval(call.function.arguments))


def response(choices) -> None:

    print(choices[0].message.content, end=None)

    tool_calls = choices[0].message.tool_calls

    if tool_calls:
        _tool_call_handler(tool_calls)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    load_dotenv()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    chat = client.chat.completions.create(
        model="anthropic/claude-haiku-4.5",
        messages=[{"role": "user", "content": args.p}],
        tools=[Tools.READ.value]
    )

    if not chat.choices or len(chat.choices) == 0:
        raise RuntimeError("no choices in response")

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    response(chat.choices)


if __name__ == "__main__":
    main()
