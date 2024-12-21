letter1 = input()
letter2 = input()
letter3 = input()
number = int(input())

capital_a_value = ord("A") - 1
letter1_value = ord(letter1) - capital_a_value
letter2_value = ord(letter2) - capital_a_value
letter3_value = ord(letter3) - capital_a_value

values_sum = letter1_value + letter2_value + letter3_value
average = values_sum / 3

if average == letter1_value or average == letter2_value or average == letter3_value:
    print(int(average))
else:
    remainder = values_sum % number
    if remainder == 0:
        print(values_sum)
    else:
        print(remainder)

