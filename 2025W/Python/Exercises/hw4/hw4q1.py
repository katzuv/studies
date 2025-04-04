def changeToUpper(my_str, char, num):
    new_str = ""
    replaced_characters = 0
    for character in my_str:
        if character == char and character.islower() and replaced_characters < num:
            new_str += character.upper()
            replaced_characters += 1
        else:
            new_str += character

    return new_str


def changeToUpperFromList(lst, char, num):
    for i, string in enumerate(lst):
        lst[i] = changeToUpper(string, char, num)


def main():
    str_list = input()
    char = input()
    num = int(input())

    strings = str_list.split(",")
    changeToUpperFromList(strings, char, num)
    print(strings)


main()
