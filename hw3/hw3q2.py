raw_numbers = input().split(",")
numbers = []
for i in raw_numbers:
    numbers.append(int(i))
target = int(input())

for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):
        for k in range(j + 1, len(numbers)):
            first, second, third = numbers[i], numbers[j], numbers[k]
            if first == second or second == third or first == third:
                continue
            if first + second + third == target:
                print(f"{first}{second}{third}")
