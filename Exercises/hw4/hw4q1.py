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
