import os
import random
import sys


# make a list of words
WORDS = [
    'axiom',
    'bayou',
    'buxom',
    'buzz',
    'cowboy',
    'curacao',
    'dirndl',
    'euouae',
    'fizz',
    'fjord',
    'guffaw',
    'haiku',
    'iatrogenic',
    'jazz',
    'jinx',
    'jiujitsu',
    'kiwi',
    'mnemonic',
    'naphtha',
    'onyx',
    'ostracize',
    'ouija',
    'phlegm',
    'pneumonia',
    'pshaw',
    'quips',
    'quixotic',
    'razzmatazz',
    'rhythm',
    'schizophrenia',
    'shiv',
    'triphthong',
    'twyndyllyng',
    'vellum',
    'wildebeest',
    'wyvern',
    'yoyo',
    'zephyr',
    'zilch'
]


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def draw(wrong_guesses, correct_guesses, secret_word):
    clear()

    print('Strikes: {}/7'.format(len(wrong_guesses)))
    print('\n')
    print("Incorrect letters:", end=' ')

    for letter in wrong_guesses:
        print(letter, end=' ')
    print('\n\n')

    for letter in secret_word:
        if letter in correct_guesses:
            print(letter, end=' ')
        else:
            print('_', end=' ')

    print('\n\n')


def get_guess(guesses):
    while True:
        guess = input("Guess a letter: ").lower()

        if len(guess) != 1:
            print("You can only guess a single letter!")
        elif guess in guesses:
            print("You've already guessed {}.  Try again!".format(guess))
        elif not guess.isalpha():
            print("You can only guess letters!")
        else:
            return guess


def play(done):
    clear()
    # pick a random word
    secret_word = random.choice(WORDS)
    wrong_guesses = set()
    correct_guesses = set()
    word_set = set(secret_word)

    while True:
        draw(wrong_guesses, correct_guesses, secret_word)
        guess = get_guess(wrong_guesses | correct_guesses)

        # print out win / lose
        if guess in word_set:
            correct_guesses.add(guess)
            if not word_set.symmetric_difference(correct_guesses):
                print("You win!")
                print("The secret word was {}.".format(secret_word))
                done = True

        else:
            wrong_guesses.add(guess)
            if len(wrong_guesses) == 7:
                draw(wrong_guesses, correct_guesses, secret_word)
                print("You lost!")
                print("The secret word was {}.".format(secret_word))
                done = True

        if done:
            play_again = input("Play again? Y/n ").lower()

            if play_again != 'n':
                return play(done=False)
            else:
                sys.exit()


def welcome():
    start = input("Press enter / return to start or Q to quit ").lower()
    if start == 'q':
        print("Bye!")
        sys.exit()
    else:
        return True


print('Welcome to Letter Guess!')


done = False


while True:
    clear()
    welcome()
    play(done)
