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

start = time.time()
expression_dict = find_expression_manually()
end = time.time() - start
print(end)

while (True):
    target_value = int(input())
    if (expression_dict.get(target_value) != None):
        print(f"Найденное выражение: {expression_dict.get(target_value)}")
    else:
        print("Решение не найдено.")

