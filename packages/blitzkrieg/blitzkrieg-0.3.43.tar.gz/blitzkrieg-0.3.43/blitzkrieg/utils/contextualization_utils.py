import ast
import inspect
import os
import pyperclip
import sys
from blitzkrieg.ui_management.console_instance import console

def is_click_command(node: ast.FunctionDef) -> bool:
    """Check if a function definition is a Click command."""
    return any(
        isinstance(decorator, ast.Call) and
        isinstance(decorator.func, ast.Attribute) and
        decorator.func.attr == 'command'
        for decorator in node.decorator_list
    )
