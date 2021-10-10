import random

NUM_DIGITS = 3
MAX_GUESSES = 10


def main():
    print(f''' Guess the number!
    by Fahad Mirza
    
    I am thinking of a {NUM_DIGITS}-digit number with no repeated digits.
    Try to guess what it is. Here are some clues:
    When I say:        That means:
    pico               One digit is correct but in the wrong position.
    fermi              One digit is correct and in the right position.
    bagels             No digit is correct.
    
    For example, if the secret number was 248 and your guess is 843, the clues would be:
    Fermi Pico.''')

    print('I have thought up a number.')
    print(f'You have {MAX_GUESSES} guesses to get it.')
    secret_number = get_secret_number()

    num_of_guesses = 1
    guessed_number = ''

    while num_of_guesses <= MAX_GUESSES:
        print(f"Guess #{num_of_guesses}")
        guessed_number = input("> ")

        if len(guessed_number) == NUM_DIGITS:
            if guessed_number == secret_number:
                break
            else:
                print(get_clues(guessed_number, secret_number))

        else:
            print(f"Provide a {NUM_DIGITS}-digit number")

        num_of_guesses += 1

    if num_of_guesses <= MAX_GUESSES and guessed_number == secret_number:
        print("You got it!")
    else:
        print(f"You ran out of guesses. The secret number was {secret_number}.")


def get_secret_number():
    number = list("0123456789")
    random.shuffle(number)
    secret_number = number[:NUM_DIGITS]

    return ''.join(secret_number)


def get_clues(guessed_num, secret_number):
    clues = []
    for i in range(NUM_DIGITS):
        if guessed_num[i] == secret_number[i]:
            clues.append("fermi")
        elif guessed_num[i] in secret_number:
            clues.append("pico")

    if not clues:
        clues.append("bagels")

    # Sort alphabetically so that player cannot guess what clue is for what digit
    clues.sort()

    return ' '.join(clues)


if __name__ == "__main__":
    main()
