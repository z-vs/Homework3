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


def main():
    output_file = 'output.json'

    config_lines = []
    print("Введите вашу конфигурацию (нажмите Enter на пустой строке, чтобы закончить ввод):")

    while True:
        line = input()
        if line.strip() == "":
            break
        config_lines.append(line)

    config = '\n'.join(config_lines)

    config_parser = ConfigParser()
    for line in config.splitlines():
        line = line.strip()
        if line:
            config_parser.declare_constant(line)

    result = config_parser.constants

    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
