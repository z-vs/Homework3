import json
import re


class ConfigParser:
    def __init__(self):
        self.constants = {}

    def declare_constant(self, line):
        match = re.match(r'let\s+(\w+)\s*=\s*(.+)', line)
        if match:
            name = match.group(1)
            if name in self.constants:
                raise ValueError(f"Константа '{name}' уже объявлена.")
            value = self.evaluate_expression(match.group(2).strip())
            self.constants[name] = value
        else:
            raise ValueError(f"Некорректная строка: '{line}'")

    def evaluate_expression(self, expr):
        # Обработка обращения к константам
        expr = self.replace_constants(expr).strip()

        # Проверка на булевы значения
        if expr.lower() == 'true':
            return True
        elif expr.lower() == 'false':
            return False

        # Обработка чисел и строк
        if expr.startswith('"') and expr.endswith('"'):
            return expr[1:-1]

        if expr.startswith('#(') and expr.endswith(')'):
            inner_values = expr[2:-1].strip()
            if inner_values == '':
                return []
            items = [self.evaluate_expression(item.strip()) for item in inner_values.split(',')]
            return items

        # Пробуем привести выражение к числу или вычислить
        try:
            return eval(expr, {}, self.constants)
        except NameError:
            raise ValueError(f"Недопустимое выражение: '{expr}'")
        except Exception as e:
            raise ValueError(f"Ошибка при вычислении: '{expr}' - {str(e)}")

    def replace_constants(self, expr):
        # Заменяем каждое вхождение @{имя} на соответствующее значение константы
        def replacement(match):
            const_name = match.group(1)
            if const_name in self.constants:
                return str(self.constants[const_name])
            raise ValueError(f"Константа '{const_name}' не объявлена.")

        # Сначала заменим обращения к константам
        expr = re.sub(r'@\{(\w+)\}', replacement, expr)

        return expr


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
            try:
                config_parser.declare_constant(line)
            except ValueError as e:
                print(e)

    result = config_parser.constants
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
