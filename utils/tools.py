from enum import Enum
import sys
import subprocess
from json import loads
from typing import Dict, List
from subprocess import CompletedProcess


class Tools(Enum):
    READ = {
        "type": "function",
        "function": {
            "name": "Read",
            "description": "Read and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read",
                    }
                },
                "required": ["file_path"],
            },
        },
    }
    WRITE = (
        {
            "type": "function",
            "function": {
                "name": "Write",
                "description": "Write content to a file",
                "parameters": {
                    "type": "object",
                    "required": ["file_path", "content"],
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path of the file to write to",
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write to the file",
                        },
                    },
                },
            },
        },
    )
    BASH = {
        "type": "function",
        "function": {
            "name": "Bash",
            "description": "Execute a shell command",
            "parameters": {
                "type": "object",
                "required": ["command"],
                "properties": {
                    "command": {"type": "string", "description": "The command to execute"}
                },
            },
        },
    }


def read_file(file_path: str) -> str:

    try:
        with open(file_path, "r") as f:
            file_content = f.read()

        return file_content

    except FileNotFoundError as e:
        print(e, file=sys.stderr)

        return e


def write_file(file_path: str, content: str) -> str:

    try:
        with open(file_path, "w+") as f:
            f.write(content)

        return f"Successful write to {file_path}"

    except Exception as e:
        print(e, file=sys.stderr)

        return e


def execute_bash(command: str) -> str:

    try:
        command_list: List[str] = command.split(" ")
        result: CompletedProcess = subprocess.run(command_list)

        return result.stdout

    except Exception as e:
        print(e, file=sys.stderr)
        return e


def tool_map(name: str) -> callable:

    mapper = {
        "Read": read_file,
        "Write": write_file,
        "Bash": execute_bash,
    }

    return mapper[name]
