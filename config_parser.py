import json
import re


class ConfigParser:
    def __init__(self):
        self.constants = {}

    def declare_constant(self, line):
        match = re.match(r'let\s+(\w+)\s*=\s*(.+)', line)
        if match:
            name = match.group(1)
            value = self.evaluate_expression(match.group(2).strip())
            self.constants[name] = value
        else:
            raise ValueError(f"Некорректная строка: '{line}'")

