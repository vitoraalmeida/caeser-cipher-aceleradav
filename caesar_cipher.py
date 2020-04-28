import string

def process_char(char, shift, mode='encode'):
    alphabet = list(string.ascii_lowercase)
    old_index = alphabet.index(char)

    if mode == 'decode':
        new_index = old_index - shift
        if new_index < 0:
            new_index += 26
    else:
        new_index = old_index + shift
        if new_index > 25:
            new_index -= 26

    return alphabet[new_index]


def execute(original_phrase, shift, mode='encode'):
    new_chars = []
    original_phrase = enumerate(original_phrase.lower())

    for _, char in original_phrase:
        if char.isalpha():
            new_chars.append(process_char(char, shift, mode))
        else:
            new_chars.append(char)

    new_phrase = ''.join(new_chars)
    return new_phrase


