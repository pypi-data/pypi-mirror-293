# src/yatl/utils.py

import os
from typing import Any, Dict

from .compiler import YATLCompiler
from .parser import YATLParser
from .runtime import YATLRuntime
from .validator import YATLValidator


def is_valid_state_name(name: str) -> bool:
    """
    Check if a given string is a valid state name.
    """
    return name.isidentifier()


def is_valid_event_name(name: str) -> bool:
    """
    Check if a given string is a valid event name.
    """
    return name.isidentifier()


def load_yatl_file(file_path: str) -> str:
    """
    Load a YATL file from the given file path.

    :param file_path: Path to the YATL file
    :return: YATL content as a string
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"YATL file not found: {file_path}")

    with open(file_path, "r") as file:
        return file.read()


def process_yatl(yatl_content: str) -> Dict[str, Any]:
    """
    Process YATL content: parse, validate, and compile.

    :param yatl_content: YATL content as a string
    :return: Compiled YATL as a dictionary
    """
    parser = YATLParser()
    validator = YATLValidator()
    compiler = YATLCompiler()

    parsed_yatl = parser.parse(yatl_content)
    if not validator.validate(parsed_yatl):
        raise ValueError(f"YATL validation failed: {validator.errors}")

    return compiler.compile(parsed_yatl)


def execute_yatl(compiled_yatl: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute compiled YATL.

    :param compiled_yatl: Compiled YATL as a dictionary
    :return: The final context after execution
    """
    runtime = YATLRuntime(compiled_yatl)
    runtime.execute()
    return runtime.context


def load_and_execute_yatl(file_path: str) -> Dict[str, Any]:
    """
    Load a YATL file, process it, and execute it.

    :param file_path: Path to the YATL file
    :return: The final context after execution
    """
    yatl_content = load_yatl_file(file_path)
    compiled_yatl = process_yatl(yatl_content)
    return execute_yatl(compiled_yatl)


def yatl_from_string(yatl_content: str) -> Dict[str, Any]:
    """
    Process and execute YATL from a string.

    :param yatl_content: YATL content as a string
    :return: The final context after execution
    """
    compiled_yatl = process_yatl(yatl_content)
    return execute_yatl(compiled_yatl)
