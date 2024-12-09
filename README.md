# Кофигурационное управление

## Домашнее задание 3

### Общее описание

Разработать инструмент командной строки для учебного конфигурационного языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из входного формата в выходной. Синтаксические ошибки выявляются с выдачей сообщений.
Входной текст на учебном конфигурационном языке принимается из стандартного ввода. Выходной текст на языке json попадает в файл, путь к которому задан ключом командной строки.

Массивы:

#( значение значение значение ... )

Имена:

[a-zA-Z]+

Значения:

• Числа.

• Строки.

• Массивы.

Строки:

"Это строка"

Объявление константы на этапе трансляции:

let имя = значение

Вычисление константы на этапе трансляции:

@{имя}

Результатом вычисления константного выражения является значение.
Все конструкции учебного конфигурационного языка (с учетом ихвозможной вложенности) должны быть покрыты тестами. Необходимо показать 2 примера описания конфигураций из разных предметных областей.

### Классы и функции

### Класс ConfigParser

Класс ConfigParser предназначен для разбора строк конфигураций и сохранения их в виде констант в словаре. Он поддерживает простые типы данных, такие как строки, числа и булевы значения, а также массивы.

##### __init__(self)

Функция инициализирует объект класса ConfigParser.
Создает и настраивает пустой словарь constants, который будет использоваться для хранения всех констант, объявленных в процессе работы.

##### declare_constant(self, line)

Функция принимает строку line, содержащую объявление константы в формате, подобном: let <name> = <value>.
Использует регулярное выражение (re.match) для поиска имени константы и значения в строке.
Регулярное выражение r'let\s+(\w+)\s*=\s*(.+)' ищет шаблон, в котором:
  - let - ключевое слово, указывающее на объявление.
  - \s+ - пробелы между let и именем.
  - (\w+) - имя константы (последовательность букв, цифр и символа подчеркивания).
  - \s*=\s* - знак равенства с пробелами вокруг.
  - (.+) - значение константы.
Если строка соответствует шаблону, имя константы извлекается и передается в метод evaluate_expression для разбора значения.
Значение этой константы сохраняется в словаре constants под указанным именем.
Если строка не соответствует шаблону, возникает исключение ValueError с сообщением об ошибке.

##### evaluate_expression(self, expr)

Функция принимает строку expr, содержащую значение, которое нужно разобрать.
Строка очищается от пробелов с помощью strip().
Проверяет, является ли expr строчным значением 'true' или 'false' (в любом регистре) и возвращает соответственно булево значение.
Попытка преобразования строки в число:
  - Если строка содержит точку, она будет преобразована в число с плавающей точкой (float).
  - Если нет точки, строка будет преобразована в целое число (int).
Если преобразование завершится неудачно, происходит переход к следующей проверке.
Если строка заключена в двойные кавычки ("), возвращает содержимое без кавычек.
Если строка формируется как массив (начинается с #( и заканчивается на )), вызывается специальная логика для разбора массива.
Внутренние значения массива извлекаются и разбиваются по запятой с учетом вложенности.

### Примеры использования

Входной текст на учебном конфигурационном языке:

![image](https://github.com/user-attachments/assets/1243d9ff-4b3d-4230-9bd8-8b6dfce24380)

Выходной текст на языке json:

![image](https://github.com/user-attachments/assets/10eb93ac-206d-4a9d-89ac-7b05bcbab292)

Входной текст на учебном конфигурационном языке:

![image](https://github.com/user-attachments/assets/fddd26d3-408e-4965-b654-72784e3b0362)

Выходной текст на языке json:

![image](https://github.com/user-attachments/assets/52bc8df8-99ae-403e-a8bc-8ff98ef20030)

### Результаты прогона тестов

![image](https://github.com/user-attachments/assets/6dfbe9d0-0dd3-4a11-8103-da778b951d91)


