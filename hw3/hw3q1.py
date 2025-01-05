calculation = input()
calculation = calculation.replace("**", "power").replace("*", "multiplication").replace("+", "addition").replace("-", "subtraction")

elements = calculation.split(",")

elements_amount = len(elements)
total = elements_amount // 4
correct = 0

for i in range(0, elements_amount, 4):
    first = int(elements[i])
    second = int(elements[i + 1])
    operator = elements[i + 2]
    result = int(elements[i + 3])

    if operator == "power" and first ** second == result:
        correct += 1
    elif operator == "multiplication" and first * second == result:
        correct += 1
    elif operator == "addition" and first + second == result:
        correct += 1
    elif operator == "subtraction" and first - second == result:
        correct += 1

print(f"{correct}/{total}")
