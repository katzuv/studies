def applyPermutation(num_lst, perm_lst):
    list_copy = num_lst[:]
    for i, new_index in enumerate(perm_lst):
        num_lst[new_index] = list_copy[i]


def getMatrix():
    rows = int(input())
    matrix = []
    for _ in range(rows):
        raw_row = input()
        row = [int(number) for number in raw_row.split(",")]
        matrix.append(row)

    return matrix


def permuteMatrix():
    matrix = getMatrix()
    permutation_input = input()
    permutation_lst = [int(number) for number in permutation_input.split(",")]
    applyPermutation(matrix, permutation_lst)
    print(matrix)


permuteMatrix()