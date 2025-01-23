def applyPermutation(num_lst, perm_lst):
    list_copy = num_lst[:]
    for i, new_index in enumerate(perm_lst):
        num_lst[new_index] = list_copy[i]
