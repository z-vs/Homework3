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

    def evaluate_expression(self, expr):
        expr = expr.strip()

        if expr.lower() == 'true':
            return True
        elif expr.lower() == 'false':
            return False

        try:
            if '.' in expr:
                return float(expr)
            else:
                return int(expr)
        except ValueError:
            pass

        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]


        if expr.startswith('#(') and expr.endswith(')'):
            inner_values = expr[2:-1].strip()
            if inner_values == '':
                return []

            items = []
            depth = 0
            current_item = []
            for char in inner_values:
                if char == ',' and depth == 0:
                    items.append(''.join(current_item).strip())
                    current_item = []
                else:
                    if char == '(':
                        depth += 1
                    elif char == ')':
                        depth -= 1
                    current_item.append(char)

            if current_item:
                items.append(''.join(current_item).strip())

            return [self.evaluate_expression(item) for item in items]

        raise ValueError(f"Недопустимое выражение: '{expr}'")


