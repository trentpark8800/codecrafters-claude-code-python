from enum import Enum
import sys
from typing import Dict


class Tools(Enum):
    READ = {
        "type": "function",
        "function": {
            "name": "Read",
            "description": "Read and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "The path to the file to read"}
                },
                "required": ["file_path"],
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


def tool_map(name: str) -> callable:

    mapper = {
        "Read": read_file
    }

    return mapper[name]