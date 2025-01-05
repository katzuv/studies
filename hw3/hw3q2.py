raw_numbers = input().split(",")
numbers = []
for i in raw_numbers:
    numbers.append(int(i))
target = int(input())

combinations = []

for i in range(len(numbers) - 2):
    for j in range(i + 1, len(numbers) - 1):
        for k in range(j + 1, len(numbers)):
            first, second, third = numbers[i], numbers[j], numbers[k]
            if first == second or second == third or first == third:
                continue
            if first + second + third == target:
                combinations.append(f"{first}{second}{third}")

unique_combinations = []
for first_index in range(len(combinations)):
    for second_index in range(first_index + 1, len(combinations)):
        if combinations[first_index] == combinations[second_index]:
            break
    else:
        unique_combinations.append(combinations[first_index])

for combination in unique_combinations:
    print(combination)
