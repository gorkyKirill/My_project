import time

def generate_combinations(digits, operators):
    #Создания всех комбинаций
    def generate_helper(current_expr, index):
        if index == len(digits):
            result = eval(current_expr)
            all_combinations[result] = current_expr
            return
        for op in operators:
            generate_helper(current_expr + op + str(digits[index]), index + 1)

    all_combinations = {}
    generate_helper(str(digits[0]), 1)
    return all_combinations

def find_expression_manually():
    digits = list(range(9, 0, -1))
    operators = ['+', '-', '']
    expressions_dict = generate_combinations(digits, operators)
    
    return expressions_dict
#Время работы и выхов функции создания словаря
start = time.time()
expression_dict = find_expression_manually()
end = time.time() - start
print(end)

while (True):
    target_value = int(input())
    if (expression_dict.get(target_value) != None):
        print(f"Найденное выражение: {expression_dict.get(target_value)}")
    else:
        print("Выражение не найдено.")
# Вероятно что существует второе решение, не требущее нахождение всех возможных комбинаций, путем выстраивания
# Генерирубщей функции таким обращом, что вырожения сразу будут упорядочены по значению, в таком случае можно было реализовать
# метод соотносящий искомое число с позицией соотвествующего ему выражения, в крайнем случае метод похожий процессом на бинарный поиск
# Это уличшило бы скорость работы кода в случае одного запроса, в случае нескольких запросов, предпочтительнее будет, вышеизложеный вариант
